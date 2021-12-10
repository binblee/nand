class SymbolTableEntry:
    def __init__(self, name, type, kind, index) -> None:
        self.name = name
        self.type = type # int, boolean, char, void, or classname
        self.kind = kind # static, field for class scope 
                       # or argument, var for subroutine scope
        self.index = index # 

    def __str__(self) -> str:
        return f'{self.name} - {self.type} - {self.kind} - {self.index}'

class SymbolTable:
    def __init__(self, class_scope=True) -> None:
        self.entries = {}
        self.class_scope = class_scope
        if class_scope:
            self.static_index = -1
            self.field_index = -1
        else:
            self.argument_index = -1
            self.var_index = -1

    def add(self, name, type, kind) -> bool:
        if name in self.entries.keys():
            print(f'duplicate entry requested: {name}')
            return False
        else:
            index = -1
            if kind == 'var':
                assert not self.class_scope, 'should not be global'
                self.var_index = self.var_index + 1
                index = self.var_index
            elif kind == 'argument':
                assert not self.class_scope, 'should not be global'
                self.argument_index = self.argument_index + 1
                index = self.argument_index
            elif kind == 'static':
                assert self.class_scope, 'should be global scope'
                self.static_index = self.static_index + 1
                index = self.static_index
            entry = SymbolTableEntry(name, type, kind, index)
            self.entries[name] = entry
            return True

    def has_entry(self, name) -> bool:
        return name in self.entries.keys()

    def get(self, name) -> SymbolTableEntry:
        return self.entries[name]

    def var_count(self) -> int:
        var_count = 0
        for v in self.entries.values():
            if v.kind == 'var':
                var_count += 1
        return var_count

class ChainedSymbolTable:
    def __init__(self, debug_info=True) -> None:
        self.tables = [SymbolTable()]
        self.debug_info = debug_info

    def new_scope(self):
        self.tables.append(SymbolTable(class_scope=False))
        if self.debug_info:
            print('new scope')

    def close_scope(self):
        assert len(self.tables) > 1, 'want to close global scope?'
        self.tables.pop()
        if self.debug_info:
            print('close scope')

    def add(self, name, type, kind):
        added = self.tables[-1].add(name, type, kind)
        if added and self.debug_info:
            entry = self.tables[-1].get(name)
            print(f'added: {entry}')

    def get(self, name) -> SymbolTableEntry:
        for i in range(len(self.tables) -1, -1, -1):
            if self.tables[i].has_entry(name):
                return self.tables[i].get(name)
        return None

    def var_count(self) -> int:
        return self.tables[-1].var_count()

# test only
if __name__ == '__main__':
    st = ChainedSymbolTable()
    st.add('static_var1', 'int', 'static')
    st.new_scope()
    st.add('__tmp_do_return', 'int', 'var')
    st.add('another_var', 'int', 'var')
    st.add('another_var', 'int', 'var')
    print(st.get('__tmp_do_return'))
    print(st.get('another_var'))
    print(st.get('static_var1'))
    print(st.var_count())
    st.close_scope()
    print(st.get('__tmp_do_return'))
    print(st.get('static_var1'))
