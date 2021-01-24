#!/usr/bin/env python
import sys

OPSCODE = {
    '0': '0101010',
    '1': '0111111',
    '-1' : '0111010',
    'D'  : '0001100',
    'A'  : '0110000',
    'M'  : '1110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '!M' : '1110001',
    '-D' : '0001111',
    '-A' : '0110011',
    '-M' : '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

DSTCODE = {
    ''   : '000',
    'M'  : '001',
    'D'  : '010',
    'MD' : '011',
    'A'  : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD': '111'
}

JMPCODE = {
    ''   : '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

# TODO: private methods
class Instruction:
    def __init__(self, str):
        self.src = str
        self.dst = ''
        self.opcode = ''
        self.jmp = ''
        self.a_value = ''   # this attribute will be modified later if it is not an integer
        self.tokenize()

    def tokenize(self):
        if self.is_c_instruction():
            self.tokenize_c_instruction()
        else:
            self.tokenize_a_instruction()

    def is_c_instruction(self):
        return self.src[0] != '@'
    
    def is_a_instruction(self):
        return self.src[0] == '@'

    def tokenize_c_instruction(self):
        idx = self.src.find('=')
        if idx > 0:
            self.dst = self.src[0:idx]
            self.opcode = self.src[idx+1:]
        else:
            self.opcode = self.src
        idx = self.opcode.find(';')
        if idx > 0:
            self.jmp = self.opcode[idx+1:]
            self.opcode = self.opcode[0:idx]

    def tokenize_a_instruction(self):
        idx = self.src.find('@')
        if idx == 0:
            self.a_value = self.src[idx+1:]
        else:
            self.a_value = self.src

# TODO: rename Parser, private methods
class Parser:
    def __init__(self, source_file, binary_file):
        self.init_symbols()
        self.source_file = source_file
        self.binary_file = binary_file
        self.instructions = []
        self.lineno = 0
        self.next_variable_index = 16

    def init_symbols(self):
        self.symbols = {
            'R0'    : '0',
            'R1'    : '1',
            'R2'    : '2',
            'R3'    : '3',
            'R4'    : '4',
            'R5'    : '5',
            'R6'    : '6',
            'R7'    : '7',
            'R8'    : '8',
            'R9'    : '9',
            'R10'   : '10',
            'R11'   : '11',
            'R12'   : '12',
            'R13'   : '13',
            'R14'   : '14',
            'R15'   : '15',
            'SCREEN': '16384',
            'KBD'   : '24576',
            'SP'    : '0',
            'LCL'   : '1',
            'ARG'   : '2',
            'THIS'  : '3',
            'THAT'  : '4'
        }

    def parse(self):
        self.load()
        self.map_values()
        self.save_binary()

    # first pass
    def load(self):
        with open(self.source_file,'r') as reader:
            lines = reader.readlines()
            for line in lines:
                line = self.formlize(line)
                if line != '':
                    if self.is_label(line):
                        self.new_label(line)
                    else:
                        self.instructions.append(Instruction(line))
                        self.lineno = self.lineno + 1
    
    def is_label(self, line):
        return line.find('(') >= 0

    def new_label(self, line):
        left_parenthesis = line.find('(')
        right_parenthesis = line.find(')')
        if left_parenthesis >= 0 and right_parenthesis > 0:
            label_name = line[left_parenthesis+1:right_parenthesis]
            # last label declaration works
            self.symbols[label_name] = str(self.lineno)
        else:
            # TODO: syntax error
            pass


    # 2nd pass
    def map_values(self):
        for inst in self.instructions:
            if inst.is_a_instruction():
                if not inst.a_value.isnumeric():
                    # symbol or variable
                    if not inst.a_value in self.symbols:
                        # add symbol, this should be a variable
                        self.symbols[inst.a_value] = str(self.next_variable_index)
                        self.next_variable_index = self.next_variable_index + 1
                    inst.a_value = self.symbols[inst.a_value]
    
    def code(self, inst):
        code = ''
        if inst.is_c_instruction():
            code = '111' + OPSCODE[inst.opcode] + DSTCODE[inst.dst] + JMPCODE[inst.jmp]
        else:
            # a-instruction
            if inst.a_value.isnumeric():
                code = f'{int(inst.a_value):016b}'
            else:
                # should not be here
                code = inst.a_value
        return code

    def save_binary(self):
        with open(self.binary_file, 'w') as writer:
            for instruction in self.instructions:
                print(self.code(instruction), file=writer)

    def formlize(self, text):
        text = text[:text.find('//')]
        return text.strip()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('assembler.py <source>.asm')
    else:
        source_file = sys.argv[1]
        binary_file = ''
        if source_file.find(".asm") > 0:
            binary_file = source_file.replace('.asm','.hack')
        else:
            binary_file = source_file + ".hack"
        Parser(source_file,binary_file).parse()
