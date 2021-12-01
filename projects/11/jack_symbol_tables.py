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
    def __init__(self) -> None:
        self.entries = {}
        self.static_index = -1
        self.field_index = -1
        self.argument_index = -1
        self.var_index = -1

    def add(self, name, type, kind) -> None:
        if name in self.entries.keys():
            print(f'duplicate entry requested: {name}')
        else:
            index = -1
            if kind == 'var':
                self.var_index = self.var_index + 1
                index = self.var_index
            elif kind == 'static':
                self.static_index = self.static_index + 1
                index = self.static_index
            entry = SymbolTableEntry(name, type, kind, index)
            self.entries[name] = entry

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
    def __init__(self) -> None:
        self.tables = [SymbolTable()]

    def new_scope(self):
        self.tables.append(SymbolTable())

    def close_scope(self):
        self.tables.pop()

    def add(self, name, type, kind):
        self.tables[-1].add(name, type, kind)

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
