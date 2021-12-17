import sys
from typing import Tuple
from jack_syntax_tree import SyntaxTreeNode
from jack_symbol_tables import ChainedSymbolTable, SymbolTableEntry

class VM_Translator:
    def __init__(self, root:SyntaxTreeNode) -> None:
        self.root = root
        self.class_name = None
        self.symbol_tables = ChainedSymbolTable()
        self.label_counter = 0

    def __next_label_counter(self) -> str:
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
            if child.typename == 'classVarDec':
                s += self.__generate_classVarDec(child)
            if child.typename == 'subroutineDec':
                s += self.__generate_subroutineDec(child)
        return s

    def __generate_classVarDec(self, node:SyntaxTreeNode) -> str:
        s = ''
        assert node.children[0].typename == 'keyword', f'unknown typename {node.children[0].typename}'
        assert node.children[0].value in ('static', 'field'), f'unknow classVarDec: {node.children[0].value}'
        class_var_kind = node.children[0].value
        class_var_type = node.children[1].value
        for i in range(2, len(node.children), 2):
            assert node.children[i].typename == 'identifier', f'unknown typename {node.children[1].typename}'
            class_var_name = node.children[i].value
            self.symbol_tables.add(class_var_name, class_var_type, class_var_kind)
        return s


    def __generate_subroutineDec(self, node:SyntaxTreeNode) -> str:
        fn_type = node.children[0].value
        assert fn_type in ('function' ,'constructor', 'method'), f'subroutineDec missing keyword'
        fn_rtn_dec_valid = node.children[1].value in ('void','int') or node.children[1].typename == 'identifier'
        assert fn_rtn_dec_valid, 'fn return type, place holder'
        assert node.children[2].typename == 'identifier', 'missing identifier fn_name'
        self.symbol_tables.new_scope()
        fn_name = node.children[2].value
        fn_return = node.children[1].value
        fn_body = ''
        tmp_paramlist = ''
        if fn_type == 'method':
            fn_body = 'push argument 0\npop pointer 0\n'
            # object method param 0 is this pointer, declared param 0 should be 1, etc
            self.symbol_tables.add('__this_placeholder', 'int', 'argument')
        elif fn_type == 'constructor':
            field_count = self.symbol_tables.get_field_count()
            assert field_count > 0, 'no field in class but require to allocate memory'
            fn_body = f'push constant {field_count}\ncall Memory.alloc 1\npop pointer 0\n'
        for child in node.children:
            if child.typename == 'parameterList':
                tmp_paramlist += self.__generate_parameterList(child)
            elif child.typename == 'subroutineBody':
                fn_body += self.__generate_subroutineBody(child)
        fn_local_num = self.symbol_tables.get_var_count()
        fn_dec = f'function {self.class_name}.{fn_name} {fn_local_num}\n'
        self.symbol_tables.close_scope()
        return f'{fn_dec}{tmp_paramlist}{fn_body}'

    def __generate_parameterList(self, node:SyntaxTreeNode) -> str:
        s = ''
        for i in range(0, len(node.children), 3):
            param_type = node.children[i].value
            param_name = node.children[i+1].value
            self.symbol_tables.add(param_name, param_type, 'argument') 
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
            self.symbol_tables.add(var_name, var_type, 'var')


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
        L1 = self.__next_label_counter()
        s += f'if-goto {L1}\n'
        # VM code for executing s1
        for child in node.children:
            if child.typename == 'statements':
                s += self.__generate_statements(child)
                break
        # goto L2
        L2 = self.__next_label_counter()
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
        L1 = self.__next_label_counter()
        s = f'label {L1}\n'
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
                s += 'not\n'
                break
        L2 = self.__next_label_counter()
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
        for child in node.children:
            if child.typename == 'subroutineCall':
                fn_to_call = self.__generate_subroutineCall(child)
                s = f'{fn_to_call}pop temp 0\n'
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
            exp_list = 'push pointer 0\n' + exp_list
            fn_to_call = f'call {self.class_name}.{sub_name} {exp_count+1}\n'
        elif node.children[1].value == '.':
            # (className | varName) '.' subroutineName
            var_desc = self.symbol_tables.get(node.children[0].value)
            if var_desc:
                # varName) '.' subroutineName
                class_name = var_desc.type
                sub_name = node.children[2].value
                seg_index = self.__util_get_seg_index(var_desc)
                exp_list = f'push {seg_index}\n' + exp_list
                fn_to_call = f'call {class_name}.{sub_name} {exp_count+1}\n'
            else:
                class_name = node.children[0].value
                sub_name = node.children[2].value
                fn_to_call = f'call {class_name}.{sub_name} {exp_count}\n'
        s = f'{exp_list}{fn_to_call}'
        return s

    def __generate_letStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'letStatement', 'letStatement'
        var_name = node.children[1].value
        var_dec = self.symbol_tables.get(var_name)
        var_assignment_code = ''
        if node.children[2].typename == 'arrayAccess':
            var_assignment_code = f'push {self.__util_get_seg_index(var_dec)}\n'
            var_assignment_code += self.__generate_array_access(node.children[2])
            var_assignment_code += 'pop that 0\n'
        else:
            var_assignment_code = f'pop {self.__util_get_seg_index(var_dec)}\n'
        s = ''
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
        s += var_assignment_code
        return s


    def __generate_array_access(self, node:SyntaxTreeNode) -> str:
        s = ''
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
        s += 'add\npop pointer 1\n'
        return s

    def __util_get_seg_index(self, entry:SymbolTableEntry):
        if not entry:
            return None
        if entry.kind == 'var':
            return f'local {entry.index}'
        elif entry.kind == 'argument':
            return f'argument {entry.index}'
        elif entry.kind == 'field':
            return f'this {entry.index}'
        elif entry.kind == 'static':
            return f'static {entry.index}'
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
        expression_count = 0
        if len(node.children) > 0:
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
                    sym = self.symbol_tables.get(identifier)
                    if sym:
                        s += f'push {self.__util_get_seg_index(sym)}\n'
                        if i < len(node.children)-1 and node.children[i+1].typename == 'arrayAccess':
                            parsed = i+1
                            s += self.__generate_array_access(node.children[i+1])
                            s += 'push that 0\n'
                elif node.children[i].typename == 'keyword':
                    kw = node.children[i].value
                    if kw == 'true':
                        s += f'push constant 1\nneg\n'
                    elif kw in ('false', 'null'):
                        s += f'push constant 0\n'
                    elif kw == 'this':
                        s += f'push pointer 0\n'
                    else:
                        assert False, f'keyword unknown: {kw}'
                elif node.children[i].typename == 'stringConstant':
                    s += self.__generate_stringConstrant(node.children[i])
            else:
                parsed = -1
        return s

    def __generate_stringConstrant(self, node:SyntaxTreeNode) -> str:
        s = ''
        assert len(node.value) > 0, 'null string found'
        string_length = len(node.value)
        s += f'push constant {string_length}\ncall String.new 1\n'
        for ch in node.value:
            s += f'push constant {ord(ch)}\ncall String.appendChar 2\n'
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