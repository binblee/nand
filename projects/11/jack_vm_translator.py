import sys
from typing import Tuple
from jack_syntax_tree import SyntaxTreeNode
from jack_symbol_tables import ChainedSymbolTable, SymbolTableEntry

class VM_Translator:
    def __init__(self, root:SyntaxTreeNode) -> None:
        self.root = root
        self.class_name = None
        self.symbol_table = ChainedSymbolTable()
        self.label_counter = 0

    def __get_and_inc_label_counter(self) -> str:
        label = f'L{self.label_counter}'
        self.label_counter += 1
        return label

    def translate(self, vm_filename) -> None:
        with open(vm_filename, 'w') as writer:
            vm_code = self.__generate_class(self.root)
            print(vm_code, file=writer, end='')

    def __generate_class(self, node:SyntaxTreeNode):
        assert node.typename == 'class', 'class node required'
        assert node.children[1].typename == 'identifier'
        self.class_name = node.children[1].value
        s = ''
        for child in node.children:
            if child.typename == 'subroutineDec':
                s += self.__generate_subroutineDec(child)
        return s

    def __generate_subroutineDec(self, node:SyntaxTreeNode) -> str:
        assert node.children[0].value == 'function','missing keyword function'
        assert node.children[1].value in ('void','int'), 'fn return type, place holder'
        assert node.children[2].typename == 'identifier', 'missing identifier fn_name'
        self.symbol_table.new_scope()
        fn_name = node.children[2].value
        fn_return = node.children[1].value
        fn_body = ''
        tmp_paramlist = ''
        for child in node.children:
            if child.typename == 'parameterList':
                tmp_paramlist += self.__generate_parameterList(child)
            elif child.typename == 'subroutineBody':
                fn_body += self.__generate_subroutineBody(child)
        fn_local_num = self.symbol_table.var_count()
        fn_dec = f'function {self.class_name}.{fn_name} {fn_local_num}\n'
        self.symbol_table.close_scope()
        return f'{fn_dec}{tmp_paramlist}{fn_body}'

    def __generate_parameterList(self, node:SyntaxTreeNode) -> str:
        s = '//parameterList:\n'
        for i in range(0, len(node.children), 3):
            param_type = node.children[i].value
            param_name = node.children[i+1].value
            self.symbol_table.add(param_name, param_type, 'argument') 
            s += f'//{param_name} as {param_type}\n'           
        return s

    def __generate_subroutineBody(self, node:SyntaxTreeNode) -> str:
        s = ''
        for child in node.children:
            if child.typename == 'varDec':
                self.__generate_varDec(child)
            elif child.typename == 'statements':
                s += self.__generate_statements(child)
        return s

    # 'var' type varName (',' varName)* ';'
    def __generate_varDec(self, node:SyntaxTreeNode) -> None:
        assert node.typename == 'varDec', 'varDec'
        var_type = node.children[1].value
        for i in range(2, len(node.children), 2):
            var_name = node.children[i].value
            self.symbol_table.add(var_name, var_type, 'var')


    def __generate_statements(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'statements', 'missing statements'
        s = ''
        for child in node.children:
            if child.typename == 'doStatement':
                s += self.__generate_doStatement(child)
            elif child.typename == 'letStatement':
                s += self.__generate_letStatement(child)
            elif child.typename == 'whileStatement':
                s += self.__generate_whileStatement(child)
            elif child.typename == 'returnStatement':
                s += self.__generate_returnStatement(child)
            elif child.typename == 'ifStatement':
                s += self.__generate_ifStatement(child)
        return s

    def __generate_ifStatement(self, node:SyntaxTreeNode) -> str:
        s = ''
        # VM code for computing ~(cond)
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
                s += 'not\n'
                break
        # if-goto L1
        L1 = self.__get_and_inc_label_counter()
        s += f'if-goto {L1}\n'
        # VM code for executing s1
        for child in node.children:
            if child.typename == 'statements':
                s += self.__generate_statements(child)
                break
        # goto L2
        L2 = self.__get_and_inc_label_counter()
        s += f'goto {L2}\n'
        # label L1
        s += f'label {L1}\n'
        # VM code for executing s2
        for index in range(0, len(node.children)):
            if node.children[index].value == 'else':
                expr = node.children[index+2]
                if expr.typename == 'statements':
                    s += self.__generate_statements(expr)
        # label L2
        s += f'label {L2}\n'
        return s


    def __generate_whileStatement(self, node:SyntaxTreeNode) -> str:
         
        # label L1
        #   VM code for computing ~(cond)
        #   if-goto L2
        #   VM code for executing s1
        #   goto L1
        # label L2
        L1 = self.__get_and_inc_label_counter()
        s = f'label {L1}\n'
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
                s += 'not\n'
                break
        L2 = self.__get_and_inc_label_counter()
        s += f'if-goto {L2}\n'
        for child in node.children:
            if child.typename == 'statements':
                s += self.__generate_statements(child)
                s += f'goto {L1}\n'
                break
        s += f'label {L2}\n'
        return s

    def __generate_doStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'doStatement', 'doStatement'
        # need to request 1 local variable to hold (and ignore) return value
        var_name = '__do_return_hold_and_return'
        self.symbol_table.add(var_name, 'int', 'var')
        index = self.symbol_table.get(var_name).index
        for child in node.children:
            if child.typename == 'subroutineCall':
                fn_to_call = self.__generate_subroutineCall(child)
                s = f'{fn_to_call}pop local {index}\n'
        return s

    def __generate_subroutineCall(self, node:SyntaxTreeNode) -> str:
        assert node.children[1].value in ('(', '.'), f'{node.to_xml(0)}subroutine call miss ( or .'
        # expression list
        s = ''
        exp_list = ''
        exp_count = -1
        for child in node.children:
            if child.typename == 'expressionList':
                exp_list, exp_count = self.__generate_expressionList(child)
        # call subroutine
        fn_to_call = ''
        if node.children[1].value == '(':
            # subroutineName
            sub_name = node.children[0].value
            fn_to_call = f'call {sub_name} {exp_count}\n'
            assert False, 'subroutineName call to be handled'
        elif node.children[1].value == '.':
            # (className | varName) '.' subroutineName
            var_desc = self.symbol_table.get(node.children[0])
            if var_desc:
                # varName) '.' subroutineName
                var_name = node.children[0].value
                sub_name = node.children[2].value
                assert False, 'varName.subroutineName call to be handled'
            else:
                class_name = node.children[0].value
                sub_name = node.children[2].value
                fn_to_call = f'call {class_name}.{sub_name} {exp_count}\n'
        s = f'{exp_list}{fn_to_call}'
        return s

    def __generate_letStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'letStatement', 'letStatement'
        var_name = node.children[1].value
        var_dec = self.symbol_table.get(var_name)
        var_assignment_code = f'pop {self.__util_get_seg_index(var_dec)}\n'
        s = ''
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
        s += var_assignment_code
        return s

    def __util_get_seg_index(self, entry:SymbolTableEntry):
        if not entry:
            return None
        if entry.kind == 'var':
            return f'local {entry.index}'
        elif entry.kind == 'argument':
            return f'argument {entry.index}'
        else:
            assert False, f'dont know how to translate {entry}'


    def __generate_returnStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'returnStatement', 'returnStatement'
        s = ''
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
                break
        s += 'return\n'
        return s

    def __generate_expressionList(self, node:SyntaxTreeNode) -> Tuple[str,int]:
        assert node.typename == 'expressionList', 'expressionList'
        s = ''
        expression_count = int(len(node.children)/2)+1 # count out `,` in parameter
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
        return s,expression_count

    def __generate_expression(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'expression', 'expression'
        s = ''
        parsed = -1
        for i in range(len(node.children)):
            if i != parsed:
                if node.children[i].typename == 'term':
                    s += self.__generate_term(node.children[i])
                elif self.__is_op(node.children[i]):
                    assert node.children[i+1], f'child {i+1} of {node.typename} should exist'
                    assert node.children[i+1].typename == 'term', f'child {i+1} of {node.typename} should be term'
                    s += self.__generate_term(node.children[i+1])
                    s += self.__generate_op(node.children[i])
                    parsed = i+1
            else:
                parsed = -1
        return s

    def __is_op(self, node:SyntaxTreeNode) -> bool:
        op_list = ('+', '-', '*', '/', '&', '|', '<', '>', '=')
        return node.typename == 'symbol' and node.value in op_list

    def __is_unaryOp(self, node:SyntaxTreeNode) -> bool:
        unaryOp_list = ('-', '~')
        return node.typename == 'symbol' and node.value in unaryOp_list

    # integerConstant | stringConstant | keywordConstant | 
    # varName | varName '[' expression ']' | 
    # subroutineCall | '(' expression ')' | unaryOp term
    def __generate_term(self, node:SyntaxTreeNode) -> str:
        s = ''
        parsed = -1
        for i in range(len(node.children)):
            if i != parsed:
                if self.__is_unaryOp(node.children[i]):
                    assert node.children[i+1], f'child {i+1} of {node.typename} should exist'
                    assert node.children[i+1].typename == 'term', f'child {i+1} of {node.typename} should be term'
                    s += self.__generate_term(node.children[i+1])
                    parsed = i+1
                    s += self.__generate_unaryOp(node.children[i])
                elif node.children[i].typename == 'integerConstant':
                    s += self.__generate_constant(node.children[i])
                elif node.children[i].typename == 'expression':
                    s += self.__generate_expression(node.children[i])
                elif node.children[i].typename == 'subroutineCall':
                    s += self.__generate_subroutineCall(node.children[i])
                elif node.children[i].typename == 'identifier':
                    identifier = node.children[i].value
                    sym = self.symbol_table.get(identifier)
                    if sym:
                        s += f'push {self.__util_get_seg_index(sym)}\n'
                elif node.children[i].typename == 'keyword':
                    kw = node.children[i].value
                    if kw == 'true':
                        s += f'push constant 1\nneg\n'
                    elif kw == 'false':
                        s += f'push constant 0\n'
                    else:
                        assert False, f'keyword unknown: {kw}'
            else:
                parsed = -1
        return s

    def __generate_op(self, node:SyntaxTreeNode) -> str:
        # '+'|'-'|'*'|'/'|'&'|'|'|'<'|'>'|'='
        sym_code = {
            '+': 'add\n',
            '-': 'sub\n',
            '*': 'call Math.multiply 2\n',
            '/': 'call Math.divide 2\n',
            '&': 'and\n',
            '|': 'or\n',
            '<': 'lt\n',
            '>': 'gt\n',
            '=': 'eq\n'
        }
        op = node.value
        assert op in sym_code.keys(), f'{op} not in sym_code keys()'
        s = sym_code[node.value]
        return s

    def __generate_unaryOp(self, node:SyntaxTreeNode) -> str:
        s = ''
        if node.value == '-':
            s += 'neg\n'
        elif node.value == '~':
            s += 'not\n'
        return s

    def __generate_constant(self, node:SyntaxTreeNode) -> str:
        s = ''
        if node.typename == 'integerConstant':
            s = f'push constant {node.value}\n'
        return s