import sys
class SyntaxTreeNode:
    MARKUPS = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '&': '&amp;',
    }

    def __init__(self, typename, value=None):
        self.typename = typename
        self.value = value # leaf
        self.children = [] # node with children

    def add_child(self, child, msg_for_none=''):
        if child:
            self.children.append(child)
        elif msg_for_none:
            msg = msg_for_none + '\n' + self.to_xml(0)
            sys.exit(msg)

    def add_many(self, method):
        while True:
            node = method()
            if node:
                self.add_child(node)
            else:
                break

    def to_xml(self, indent_num) -> str:
        INDENT = '  '
        s = ''
        if self.value:
            markup = self.value
            if self.value in self.MARKUPS:
                markup = self.MARKUPS[self.value]
            s = f'{INDENT * indent_num}<{self.typename}> {markup} </{self.typename}>\n'
        else:
            s = f'{INDENT * indent_num}<{self.typename}>\n'
            for child in self.children:
                s += child.to_xml(indent_num+1)
            s += f'{INDENT * indent_num}</{self.typename}>\n'
        return s
