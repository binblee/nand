import os
import sys

from jack_tokenizer import JackTokenizer, TokenType

INDENT = '  '


def raise_syntax_error(msg):
    sys.exit(msg)


def or_compile(methods):
    node = None
    for method in methods:
        node = method()
        if node:
            return node
    return node


class Node:
    def __init__(self, typename):
        self.typename = typename
        self.children = []

    def add_child(self, child, msg_for_none=''):
        if child:
            self.children.append(child)
        else:
            msg = msg_for_none + '\n' + self.to_xml(0)
            raise_syntax_error(msg)

    def to_xml(self, indent_num) -> str:
        s = f'{INDENT * indent_num}<{self.typename}>\n'
        for child in self.children:
            s += child.to_xml(indent_num+1)
        s += f'{INDENT * indent_num}</{self.typename}>\n'
        return s


class Leaf:
    MARKUPS = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '&': '&amp;',
    }

    def __init__(self, typename, value):
        self.typename = typename
        self.value = value

    def to_xml(self, indent_num) -> str:
        markup = self.value
        if self.value in self.MARKUPS:
            markup = self.MARKUPS[self.value]
        s = f'{INDENT * indent_num}<{self.typename}> {markup} </{self.typename}>\n'
        return s


class CompilationEngine:
    def __init__(self, source_filepath):
        self.source_path = source_filepath
        self.tokenizer = JackTokenizer(self.source_path)
        self.root = self.compile_class()

    def __expect_keyword(self, keywords):
        if self.tokenizer.has_more():
            next_token = self.tokenizer.peek_next()
            if next_token.get_type() == TokenType.KEYWORD:
                tk_value = next_token.get_keyword()
                if tk_value in keywords:
                    self.tokenizer.advance()
                    return Leaf('keyword', tk_value)

    def __expect_identifier(self):
        if self.tokenizer.has_more():
            next_token = self.tokenizer.peek_next()
            if next_token.get_type() == TokenType.IDENTIFIER:
                self.tokenizer.advance()
                return Leaf('identifier', next_token.get_identifier())

    def __expect_symbol(self, symbols):
        if self.tokenizer.has_more():
            next_token = self.tokenizer.peek_next()
            if next_token.get_type() == TokenType.SYMBOL:
                tk_value = next_token.get_symbol()
                if tk_value in symbols:
                    self.tokenizer.advance()
                    return Leaf('symbol', tk_value)

    def __expect_type(self):
        node = self.__expect_keyword(('int', 'char', 'boolean'))
        if not node:
            node = self.__expect_identifier()
        return node

    def __expect_void_or_type(self):
        node = self.__expect_keyword('void')
        if not node:
            node = self.__expect_type()
        return node

    def __expect_op(self):
        # '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        node = self.__expect_symbol(('+', '-', '*', '/', '&', '|', '<', '>', '='))
        return node

    def __expect_unary_op(self):
        return self.__expect_symbol(('-', '~'))

    def compile_class(self):
        # class: 'class' className '{' classVarDec* subroutineDec* '}'
        local_root = Node('class')
        # 'class'
        local_root.add_child(self.__expect_keyword('class'), 'expect keyword class')
        # className
        local_root.add_child(self.__expect_identifier(), 'expect identifier className')
        # '{'
        local_root.add_child(self.__expect_symbol('{'), 'expect {')
        # classVarDec*
        while True:
            node = self.compile_class_var_dec()
            if node:
                local_root.add_child(node)
            else:
                break
        # subroutineDec*
        while True:
            node = self.compile_subroutine()
            if node:
                local_root.add_child(node)
            else:
                break
        # '}'
        local_root.add_child(self.__expect_symbol('}'), 'expect } in class')
        return local_root

    def compile_class_var_dec(self):
        # classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        # ('static' | 'field')
        node = self.__expect_keyword(('static', 'field'))
        if not node:
            return None
        local_root = Node('classVarDec')
        local_root.add_child(node)
        # re.type: 'int' | 'char' | 'boolean' | className
        # re.className: identifier
        local_root.add_child(self.__expect_type(), 'expect type')
        # varName: identifier
        local_root.add_child(self.__expect_identifier(), 'expect varName')
        # (',' varName)*
        while True:
            node = self.__expect_symbol(',')
            if node:
                local_root.add_child(node)
                local_root.add_child(self.__expect_identifier(), 'expect varName after ,')
            else:
                break
        # ';'
        local_root.add_child(self.__expect_symbol(';'), 'expect ; in varDec')
        return local_root

    def compile_subroutine(self):
        # ('constructor' | 'function' | 'method')
        node = self.__expect_keyword(('constructor', 'function', 'method'))
        if not node:
            return None
        local_root = Node('subroutineDec')
        local_root.add_child(node)
        # ('void' | type)
        local_root.add_child(self.__expect_void_or_type(), 'expect void or type')
        # subroutineName
        local_root.add_child(self.__expect_identifier(), 'expect subroutineName')
        # '('
        local_root.add_child(self.__expect_symbol('('), 'expect )')
        # parameterList
        local_root.add_child(self.compile_parameter_list(), 'expect parameterList')
        # ')'
        local_root.add_child(self.__expect_symbol(')'), 'expect )')
        # subroutineBody
        local_root.add_child(self.compile_subroutine_body(), 'expect subroutineBody')
        return local_root

    def compile_parameter_list(self):
        # ((type varName) (',' type varName)*)?
        local_root = Node('parameterList')
        # (type varName)
        node = self.__expect_type()
        if not node:
            return local_root
        local_root.add_child(node)
        local_root.add_child(self.__expect_identifier(), 'expect varName')
        # (',' type varName) *
        while True:
            node = self.__expect_symbol(',')
            if node:
                local_root.add_child(node)
                local_root.add_child(self.__expect_type(), 'expect type')
                local_root.add_child(self.__expect_identifier(), 'expect identifier')
            else:
                break
        return local_root

    def compile_subroutine_body(self):
        # subroutineBody
        # '{' varDec* statements '}'
        local_root = Node('subroutineBody')
        # '{'
        node = self.__expect_symbol('{')
        if not node:
            return None
        local_root.add_child(node)
        # varDesc*
        while True:
            var_desc = self.compile_var_dec()
            if var_desc:
                local_root.add_child(var_desc, 'syntax error in varDesc')
            else:
                break
        # statements
        local_root.add_child(self.compile_statements(), 'expect statements')
        # '}'
        local_root.add_child(self.__expect_symbol('}'), 'expect }')
        return local_root

    def compile_var_dec(self):
        # 'var' type varName (',' varName)* ';'
        node = self.__expect_keyword('var')
        if not node:
            return None
        # 'var' type varName
        local_node = Node('varDec')
        local_node.add_child(node)
        local_node.add_child(self.__expect_type(), 'expect type in varDec')
        local_node.add_child(self.__expect_identifier(), 'expect identifier in varDec')
        # (',' varName)*
        while True:
            node = self.__expect_symbol(',')
            if node:
                local_node.add_child(node)
                local_node.add_child(self.__expect_identifier(), 'expect identifier in varDec')
            else:
                break
        # ;
        local_node.add_child(self.__expect_symbol(';'))
        return local_node

    def compile_statements(self):
        local_root = Node('statements')
        node = or_compile((
            self.compile_do,
            self.compile_let,
            self.compile_while,
            self.compile_return,
            self.compile_if,
            )
        )
        while node:
            local_root.add_child(node)
            node = or_compile((
                self.compile_do,
                self.compile_let,
                self.compile_while,
                self.compile_return,
                self.compile_if,
                )
            )
        return local_root

    def compile_do(self):
        # 'do' subroutineCall ';'
        node = self.__expect_keyword('do')
        if not node:
            return None
        local_root = Node('doStatement')
        local_root.add_child(node)
        nodes = self.__expect_subroutine_call()
        if not nodes:
            raise_syntax_error('missing subroutine call in do statement')
        for node in nodes:
            local_root.add_child(node)
        # ;
        local_root.add_child(self.__expect_symbol(';'), 'expect ; in do')
        return local_root

    def __expect_subroutine_call(self):
        # subroutineCall: subroutineName '(' expressionList ')'
        # | (className | varName) '.' subroutineName '(' expressionList ')'
        nodes = []
        next_token = self.tokenizer.peek_next()
        if next_token.get_type() == TokenType.IDENTIFIER:
            next2_token = self.tokenizer.peek_next(2)
            n2_value = next2_token.get_symbol()
            if n2_value in ('(', '.'):
                # ok, this is a subroutine call
                node = self.__expect_identifier()
                nodes.append(node)
                next_token = self.tokenizer.peek_next()
                if next_token.get_symbol() == '.':
                    nodes.append(self.__expect_symbol('.'))
                    nodes.append(self.__expect_identifier())
                nodes.append(self.__expect_symbol('('))
                nodes.append(self.compile_expression_list())
                nodes.append(self.__expect_symbol(')'))
        return nodes

    def __expect_keyword_constant(self):
        return self.__expect_keyword(('true', 'false', 'null', 'this'))

    def __expect_integer_constant(self):
        next_token = self.tokenizer.peek_next()
        if next_token and next_token.get_type() == TokenType.INT_CONSTANT:
            self.tokenizer.advance()
            return Leaf('integerConstant', next_token.get_integer_constant())

    def __expect_string_constant(self):
        next_token = self.tokenizer.peek_next()
        if next_token and next_token.get_type() == TokenType.STRING_CONSTANT:
            self.tokenizer.advance()
            return Leaf('stringConstant', next_token.get_string_constant())

    def compile_let(self):
        # 'let' varName ('[' expression ']')? '=' expression ';'
        node = self.__expect_keyword('let')
        if not node:
            return None
        local_root = Node('letStatement')
        local_root.add_child(node)
        local_root.add_child(self.__expect_identifier(), 'expect varName in let')
        if not self.tokenizer.has_more():
            raise_syntax_error('EOF, but expect more')
        next_token = self.tokenizer.peek_next()
        if next_token.get_symbol() == '[':
            local_root.add_child(self.__expect_symbol('['), 'expect [')
            local_root.add_child(self.compile_expression(), 'expect expression in let statement')
            local_root.add_child(self.__expect_symbol(']'), 'expect ]')
        local_root.add_child(self.__expect_symbol('='), 'expect = in let')
        local_root.add_child(self.compile_expression(), 'expect expression in let statement')
        # ;
        local_root.add_child(self.__expect_symbol(';'), 'expect ; in let')
        return local_root

    def compile_while(self):
        # 'while' '(' expression ')' '{' statements '}'
        node = self.__expect_keyword('while')
        if not node:
            return None
        local_root = Node('whileStatement')
        local_root.add_child(node)
        local_root.add_child(self.__expect_symbol('('), 'expect ( in while')
        local_root.add_child(self.compile_expression(), 'expect expression in while')
        local_root.add_child(self.__expect_symbol(')'), 'expect ) in while')
        local_root.add_child(self.__expect_symbol('{'), 'expect { in while')
        local_root.add_child(self.compile_statements(), 'expect statements in while')
        local_root.add_child(self.__expect_symbol('}'), 'expect } in while')
        return local_root

    def compile_return(self):
        # 'return' expression? ';'
        node = self.__expect_keyword('return')
        if not node:
            return None
        local_root = Node('returnStatement')
        local_root.add_child(node)
        node = self.compile_expression()
        if node:
            local_root.add_child(node)
        local_root.add_child(self.__expect_symbol(';'))
        return local_root

    def compile_if(self):
        # 'if' '(' expression ')' '{' statements '}'
        # ('else' '{' statements '}')?
        node = self.__expect_keyword('if')
        if not node:
            return None
        local_root = Node('ifStatement')
        local_root.add_child(node)
        local_root.add_child(self.__expect_symbol('('), 'expect ( in if')
        local_root.add_child(self.compile_expression(), 'expect expression in if')
        local_root.add_child(self.__expect_symbol(')'), 'expect ) in if')
        local_root.add_child(self.__expect_symbol('{'), 'expect { in if')
        local_root.add_child(self.compile_statements(), 'expect statements in if')
        local_root.add_child(self.__expect_symbol('}'), 'expect } in if')
        if self.tokenizer.has_more():
            next_token = self.tokenizer.peek_next()
            if next_token.get_keyword() == 'else':
                local_root.add_child(self.__expect_keyword('else'))
                local_root.add_child(self.__expect_symbol('{'), 'expect { in else')
                local_root.add_child(self.compile_statements(), 'expect statements in else')
                local_root.add_child(self.__expect_symbol('}'), 'expect } in else')
        return local_root

    def compile_expression(self):
        # term (op term)*
        node = self.compile_term()
        if not node:
            return None
        local_root = Node('expression')
        local_root.add_child(node)
        while True:
            node = self.__expect_op()
            if node:
                local_root.add_child(node)
                local_root.add_child(self.compile_term())
            else:
                break
        return local_root

    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant |
        # varName | varName '[' expression ']' |
        # subroutineCall | '(' expression ')' |
        # unaryOp term
        local_root = Node('term')

        # integerConstant | stringConstant | keywordConstant
        node = or_compile((
            self.__expect_integer_constant,
            self.__expect_string_constant,
            self.__expect_keyword_constant,
        ))
        if node:
            local_root.add_child(node)
            return local_root

        # subroutineCall
        nodes = self.__expect_subroutine_call()
        if len(nodes) > 0:
            for node in nodes:
                local_root.add_child(node)
            return local_root

        next_token = self.tokenizer.peek_next()

        # varName | varName '[' expression ']'
        if next_token and next_token.get_type() == TokenType.IDENTIFIER:
            local_root.add_child(self.__expect_identifier())
            next2 = self.tokenizer.peek_next()
            if next2 and next2.get_symbol() == '[':
                local_root.add_child(self.__expect_symbol('['))
                local_root.add_child(self.compile_expression(), 'expect expression after [ in term')
                local_root.add_child(self.__expect_symbol(']'), 'expect ] in term')
            return local_root

        # '(' expression ')'
        if next_token and next_token.get_symbol() == '(':
            local_root.add_child(self.__expect_symbol('('))
            local_root.add_child(self.compile_expression(), 'expect expression after ( in term')
            local_root.add_child(self.__expect_symbol(')'), 'expect ) in term')
            return local_root

        # unaryOp term
        node = self.__expect_unary_op()
        if node:
            local_root.add_child(node)
            local_root.add_child(self.compile_term(), 'expect term after unary op in term')
            return local_root

        return None

    def compile_expression_list(self):
        # (expression (',' expression)* )?
        local_root = Node('expressionList')
        node = self.compile_expression()
        if node:
            local_root.add_child(node)
            # (',' expression)*
            while True:
                node = self.__expect_symbol(',')
                if node:
                    local_root.add_child(node)
                    local_root.add_child(self.compile_expression(), 'expect expression in exp list')
                else:
                    break
        return local_root

    def save_xml(self, xml_path):
        with open(xml_path, 'w') as writer:
            xml = self.root.to_xml(indent_num=0)
            print(xml, file=writer, end='')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python compile_engine.py [source.jack | source directory]')
    else:
        source_path = sys.argv[1]
        files = []
        if os.path.isdir(source_path):
            for file in os.listdir(source_path):
                if file.endswith('.jack'):
                    files.append(os.path.join(source_path, file))
        elif os.path.isfile(source_path):
            files.append(source_path)
        else:
            sys.exit('input file or directory does not exist.')
        for file in files:
            xml_filename = file.replace('.jack', '_out.xml')
            CompilationEngine(file).save_xml(xml_filename)
