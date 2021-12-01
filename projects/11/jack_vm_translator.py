from typing import Tuple
from jack_syntax_tree import SyntaxTreeNode
from jack_symbol_tables import ChainedSymbolTable

class VM_Translator:
    def __init__(self, root:SyntaxTreeNode) -> None:
        self.root = root
        self.class_name = None
        self.symbol_table = ChainedSymbolTable()


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
        assert node.children[1].value == 'void', 'void, place holder'
        assert node.children[2].typename == 'identifier', 'missing identifier fn_name'
        self.symbol_table.new_scope()
        fn_name = node.children[2].value
        fn_return = node.children[1].value
        fn_body = ''
        for child in node.children:
            if child.typename == 'subroutineBody':
                fn_body += self.__generate_subroutineBody(child)
        fn_local_num = self.symbol_table.var_count()
        fn_dec = f'function {self.class_name}.{fn_name} {fn_local_num}\n'
        self.symbol_table.new_scope()
        return f'{fn_dec}{fn_body}'

    def __generate_subroutineBody(self, node:SyntaxTreeNode) -> str:
        s = ''
        for child in node.children:
            if child.typename == 'statements':
                s += self.__generate_statements(child)
        return s

    def __generate_statements(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'statements', 'missing statements'
        s = ''
        for child in node.children:
            if child.typename == 'doStatement':
                s += self.__generate_doStatement(child)
            if child.typename == 'returnStatement':
                s += self.__generate_returnStatement(child)
        return s

    def __generate_doStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'doStatement', 'doStatement'
        # need to request 1 local variable to hold (and ignore) return value
        var_name = '__do_return_hold_and_return'
        self.symbol_table.add(var_name, 'int', 'var')
        index = self.symbol_table.get(var_name).index
        expression_list_code = ''
        parameter_count = 0
        for child in node.children:
            if child.typename == 'expressionList':
                expression_list_code, parameter_count = self.__generate_expressionList(child)
        fn_to_call = f'call {node.children[1].value}{node.children[2].value}{node.children[3].value} {parameter_count}\n'
        s = f'{expression_list_code}{fn_to_call}pop local {index}\n'
        return s

    def __generate_returnStatement(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'returnStatement', 'returnStatement'
        s = 'return\n'
        return s

    def __generate_expressionList(self, node:SyntaxTreeNode) -> Tuple[str, int]:
        assert node.typename == 'expressionList', 'expressionList'
        s = ''
        expression_count = len(node.children)
        for child in node.children:
            if child.typename == 'expression':
                s += self.__generate_expression(child)
        return s,expression_count

    def __generate_expression(self, node:SyntaxTreeNode) -> str:
        assert node.typename == 'expression', 'expression'
        s = ''
        skip = -1
        for i in range(len(node.children)):
            if i != skip:
                if node.children[i].typename == 'term':
                    s += self.__generate_term(node.children[i])
                elif node.children[i].typename == 'symbol':
                    assert node.children[i+1], f'child {i+1} of {node.typename} should exist'
                    assert node.children[i+1].typename == 'term', f'child {i+1} of {node.typename} should be term'
                    s += self.__generate_term(node.children[i+1])
                    s += self.__generate_op(node.children[i])
                    skip = i+1
            else:
                skip = -1
        return s

    def __generate_term(self, node:SyntaxTreeNode) -> str:
        s = ''
        for child in node.children:
            if child.typename == 'integerConstant':
                s += self.__generate_constant(child)
            elif child.typename == 'expression':
                s += self.__generate_expression(child)
        return s

    def __generate_op(self, node:SyntaxTreeNode) -> str:
        s = ''
        if node.value == '+':
            s += 'add\n'
        elif node.value == '*':
            s += 'call Math.multiply 2\n'
        return s

    def __generate_constant(self, node:SyntaxTreeNode) -> str:
        s = ''
        if node.typename == 'integerConstant':
            s = f'push constant {node.value}\n'
        return s