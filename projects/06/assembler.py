#!/usr/bin/env python
import sys

Opscode = {
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

Dstcode = {
    ''   : '000',
    'M'  : '001',
    'D'  : '010',
    'MD' : '011',
    'A'  : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD': '111'
}

Jmpcode = {
    ''   : '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

Symbols = {
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

class Instruction:
    def __init__(self, str):
        self.src = str
        self.dst = ''
        self.opcode = ''
        self.jmp = ''
        self.c_instruction = False
        self.set_type()
        if self.c_instruction:
            self.parse_c_instruction()
        else:
            self.parse_a_instruction()

    def __str__(self):
        return self.code()

    def set_type(self):
        if self.src[0] == '@':
            self.c_instruction = False
        else:
            self.c_instruction = True


    def parse_c_instruction(self):
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

    def parse_a_instruction(self):
        idx = self.src.find('@')
        if idx == 0:
            self.a_value = self.src[idx+1:]
        else:
            self.a_value = self.src
    
    def code(self):
        if self.c_instruction:
            return '111' + Opscode[self.opcode] + Dstcode[self.dst] + Jmpcode[self.jmp]
        else:
            if self.a_value.isnumeric():
                return f'{int(self.a_value):016b}'
            else:
                return self.a_value

class Parser:
    def __init__(self, source_file, binary_file):
        self.source_file = source_file
        self.binary_file = binary_file
        self.instructions = []
        self.lineno = 0
        self.next_variable = 16

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
                    left_parenthesis = line.find('(')
                    if left_parenthesis >= 0:
                        # label
                        right_parenthesis = line.find(')')
                        if right_parenthesis > 0:
                            label_name = line[left_parenthesis+1:right_parenthesis]
                            Symbols[label_name] = str(self.lineno)
                        else:
                            # TODO: syntax error
                            pass
                    else:
                        self.instructions.append(Instruction(line))
                        self.lineno = self.lineno + 1

    # 2nd pass
    def map_values(self):
        for instruction in self.instructions:
            if not instruction.c_instruction:
                # a-instruction
                if not instruction.a_value.isnumeric():
                    if not instruction.a_value in Symbols:
                        # add symbol, this should be a variable
                        Symbols[instruction.a_value] = str(self.next_variable)
                        self.next_variable = self.next_variable + 1
                    instruction.a_value = Symbols[instruction.a_value]

    def save_binary(self):
        with open(self.binary_file, 'w') as writer:
            for instruction in self.instructions:
                print(instruction, file=writer)

    def formlize(self, str):
        str = str[:str.find('//')]
        return str.strip()

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
        parser = Parser(source_file,binary_file)
        parser.parse()
