#!/usr/bin/env python
import sys
import os

SEGMENT_PUSH = {
    'local': '@LCL\nD=M\n@{value}\nA=D+A\nD=M',
    'argument': '@ARG\nD=M\n@{value}\nA=D+A\nD=M',
    'this': '@THIS\nD=M\n@{value}\nA=D+A\nD=M',
    'that': '@THAT\nD=M\n@{value}\nA=D+A\nD=M',
    'temp': '@5\nD=A\n@{value}\nA=D+A\nD=M',
    'static': '@{file}.{value}\nD=M',
    'pointer': '@3\nD=A\n@{value}\nA=D+A\nD=M',
    'constant': '@{value}\nD=A'
}

SEGMENT_POP = {
    'local': '@LCL\nD=M\n@{value}\nD=D+A\n@SP\nA=M\nM=D',
    'argument': '@ARG\nD=M\n@{value}\nD=D+A\n@SP\nA=M\nM=D',
    'this': '@THIS\nD=M\n@{value}\nD=D+A\n@SP\nA=M\nM=D',
    'that': '@THAT\nD=M\n@{value}\nD=D+A\n@SP\nA=M\nM=D',
    'temp': '@5\nD=A\n@{value}\nD=D+A\n@SP\nA=M\nM=D',
    'pointer': '@SP\nAM=M-1\nD=M\n@{value}\nM=D',
    'static': '@SP\nAM=M-1\nD=M\n@{file}.{value}\nM=D'
}

ASMCODE = {
    'push': '\n@SP\nA=M\nM=D\n@SP\nM=M+1',
    'pop': '\n@SP\nA=M-1\nD=M\n@SP\nA=M\nA=M\nM=D\n@SP\nM=M-1',
    'add': '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M',
    'sub': '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D',
    'neg': '@SP\nA=M\nA=A-1\nM=-M',
    'eq': ('@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n' 
           '@{file}_L{l1}\nD;JEQ\nD=0\n@{file}_L{l2}\n0;JMP\n' 
           '({file}_L{l1})\nD=-1\n({file}_L{l2})\n@SP\nA=M\nA=A-1\nM=D'),
    'gt': ('@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n' 
           '@{file}_L{l1}\nD;JGT\nD=0\n@{file}_L{l2}\n0;JMP\n' 
           '({file}_L{l1})\nD=-1\n({file}_L{l2})\n@SP\nA=M\nA=A-1\nM=D'),
    'lt': ('@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n' 
           '@{file}_L{l1}\nD;JLT\nD=0\n@{file}_L{l2}\n0;JMP\n' 
           '({file}_L{l1})\nD=-1\n({file}_L{l2})\n@SP\nA=M\nA=A-1\nM=D'),
    'and': '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M',
    'or': '@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M',
    'not': '@SP\nA=M\nA=A-1\nM=!M'
}

class Command:
    def __init__(self, string):
        self.cmd = string
        self.op = ''
        self.arg1 = ''
        self.arg2 = ''
        self.__tokenize()

    def __tokenize(self):
        tokens = self.cmd.split()
        if len(tokens) > 0:
            self.op = tokens[0]
        if len(tokens) > 1:
            self.arg1 = tokens[1]
        if len(tokens) > 2:
            self.arg2 = tokens[2]

class Parser:
    def __init__(self, source_file):
        self.source_file = source_file
        self.filename = os.path.basename(self.source_file)
        self.commands = []
        self.__load(source_file)

    def __load(self, source_file):
        with open(source_file, 'r') as reader:
            lines = reader.readlines()
            for line in lines:
                formlized_line = self.__formlize(line)
                if formlized_line != '':
                    self.commands.append(Command(formlized_line))
    
    def __formlize(self, text):
        text = text[:text.find('//')]
        return text.strip()

class CodeWriter:
    def __init__(self, vm_files):
        self.vm_files = vm_files
        self.label_index = 0
 
    def write_to(self, asm_file):
        with open(asm_file, 'w') as writer:
            for vm_file in self.vm_files:
                vm_basename = os.path.basename(vm_file)
                for cmd in Parser(vm_file).commands:
                    print(self.__code(cmd, vm_basename), file=writer)

    def __code(self, command, vm_file):
        code_template = ''
        if command.op in ASMCODE:
            code_template = ASMCODE[command.op]
            if command.op == 'push':
                if command.arg1 in SEGMENT_PUSH:
                    segment_template = SEGMENT_PUSH[command.arg1]
                    if command.arg1 == 'static':
                        code_template = segment_template.format(
                            file=vm_file,
                            value=command.arg2
                        ) + code_template
                    else:
                        code_template = segment_template.format(value=command.arg2) + code_template
            elif command.op == 'pop':
                if command.arg1 == 'static':
                    code_template = SEGMENT_POP[command.arg1].format(
                        file=vm_file,
                        value=command.arg2
                    )
                elif command.arg1 == 'pointer':
                    code_template = SEGMENT_POP[command.arg1].format(value=3+int(command.arg2))
                elif command.arg1 in SEGMENT_POP:
                    segment_template = SEGMENT_POP[command.arg1]
                    code_template = segment_template.format(value=command.arg2) + code_template
            elif command.op in ['eq','gt','lt']:
                code_template = code_template.format(
                    file=vm_file,
                    l1=self.label_index,
                    l2=self.label_index+1
                )
                self.label_index = self.label_index + 2
        
        return f'//{command.cmd}\n{code_template}\n'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('translator.py ( <source>.vm | <source directory>)' )
    else:
        source_path = sys.argv[1]
        src_is_dir = False
        vm_files = []
        asm_file = ''
        if os.path.isdir(source_path):
            src_is_dir = True
            for file in os.listdir(source_path):
                if file.endswith('.vm'):
                    vm_files.append(os.path.join(source_path, file))
        elif os.path.isfile(source_path):
            vm_files.append(source_path)

        if len(vm_files) > 0:
            if src_is_dir:
                basename = os.path.basename(source_path) + '.asm'
                asm_file = os.path.join(source_path, basename)
            elif vm_files[0].find(".vm") > 0:
                asm_file = vm_files[0].replace('.vm','.asm')
            else:
                asm_file = vm_files + ".asm"

        CodeWriter(vm_files).write_to(asm_file)
