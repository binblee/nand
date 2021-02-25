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
    'not': '@SP\nA=M\nA=A-1\nM=!M',
    'label': '({f}${label})',
    'goto': '@{f}${label}\n0;JMP',
    'if-goto': '@SP\nM=M-1\nA=M\nD=M\n@{f}${label}\nD;JNE\n',
    'call' : ('//call f n\n'
                '//push return address\n'
                '@{file}_L{l1}\n'
                'D=A\n'
                '@SP\n' 
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
                '// push LCL\n'
                '@LCL\n'
                'D=M\n'
                '@SP\n'
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
                '// push ARG\n'
                '@ARG\n'
                'D=M\n'
                '@SP\n'
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
                '// push THIS\n'
                '@THIS\n'
                'D=M\n'
                '@SP\n'
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
                '// push THAT\n'
                '@THAT\n'
                'D=M\n'
                '@SP\n'
                'A=M\n'
                'M=D\n'
                '@SP\n'
                'M=M+1\n'
                '// ARG = SP - n - 5\n'
                '@SP\n'
                'D=M\n'
                '//@n\n'
                '@{n}\n'
                'D=D-A\n'
                '@5\n'
                'D=D-A\n'
                '@ARG\n'
                'M=D\n'
                '// LCL=SP\n'
                '@SP\n'
                'D=M\n'
                '@LCL\n'
                'M=D\n'
                '//@f\n'
                '@{f}\n'
                '0;JMP\n'
                '({file}_L{l1})'
    ),
    'function' : ('//function f m\n'
                    '({f})\n'
                    '@{m}\n'
                    'D=A\n'
                    '@{f}.m\n'
                    'M=D\n'
                    '({file}_L{l2})\n'
                    '@{f}.m\n'
                    'D=M\n'
                    '@{file}_L{l1}\n'
                    'D;JEQ\n'
                    '@SP\n'
                    'A=M\n'
                    'M=0\n'
                    '@SP\n'
                    'M=M+1\n'
                    '@{f}.m\n'
                    'M=M-1\n'
                    '@{file}_L{l2}\n'
                    '0;JMP\n'
                    '({file}_L{l1})\n'
    ),
    'return' : ('//frame = LCL\n'
                '@LCL\n'
                'D=M\n'
                '@{f}.frame\n'
                'M=D\n'
                '//ret = *(frame-5)\n'
                '@{f}.frame\n'
                'D=M\n'
                '@5\n'
                'D=D-A\n'
                'A=D\n'
                'D=M\n'
                '@{f}.ret\n'
                'M=D\n'
                '// *ARG = pop()\n'
                '@SP\n'
                'AM=M-1\n'
                'D=M\n'
                '@ARG\n'
                'A=M\n'
                'M=D\n'
                '// SP = ARG+1\n'
                '@ARG\n'
                'D=M+1\n'
                '@SP\n'
                'M=D\n'
                '// THAT=*(frame-1)\n'
                '@{f}.frame\n'
                'AM=M-1\n'
                'D=M\n'
                '@THAT\n'
                'M=D\n'
                '// THIS=*(frame-2)\n'
                '@{f}.frame\n'
                'AM=M-1\n'
                'D=M\n'
                '@THIS\n'
                'M=D\n'
                '// ARG=*(frame-3)\n'
                '@{f}.frame\n'
                'AM=M-1\n'
                'D=M\n'
                '@ARG\n'
                'M=D\n'
                '// LCL=*(frame-4)\n'
                '@{f}.frame\n'
                'AM=M-1\n'
                'D=M\n'
                '@LCL\n'
                'M=D\n'
                '// goto return address\n'
                '@{f}.ret\n'
                'A=M\n'
                '0;JMP\n'
    )
}

BOOTSTRAP_INIT=(
        '//bootstrap\n'
        '//SP=256\n'
        '@256\n'
        'D=A\n'
        '@SP\n'
        'M=D\n'
        '@LCL\n'
        'D=-A\n'
        'M=D\n'
        '@ARG\n'
        'D=-A\n'
        'M=D\n'
        '@THIS\n'
        'D=-A\n'
        'M=D\n'
        '@THAT\n'
        'D=-A\n'
        'M=D\n'
)

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
        index = text.find('//')
        if index >= 0:
            text = text[:index]
        return text.strip()

class CodeWriter:
    def __init__(self, vm_files):
        self.vm_files = vm_files
        self.label_index = 0
 
    def write_to(self, asm_file):
        with open(asm_file, 'w') as writer:
            self.__bootstrap(writer)
            for vm_file in self.vm_files:
                vm_filebasename = os.path.basename(vm_file)
                current_function = ''
                for cmd in Parser(vm_file).commands:
                    if cmd.op == 'function':
                        current_function = cmd.arg1
                    print(self.__code(cmd, vm_filebasename, current_function), file=writer)

    def __bootstrap(self, writer):
        print(BOOTSTRAP_INIT, file=writer)
        cmd = Command('call Sys.init 0')
        print(self.__code(cmd, '__bootstrap__', ''), file=writer)

    def __code(self, command, vm_file, current_function):
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
            elif command.op in ['label', 'goto', 'if-goto']:
                code_template = code_template.format(f=current_function, label=command.arg1)
            elif command.op == 'call':
                code_template = code_template.format(
                    file=vm_file,
                    l1=self.label_index,
                    f=command.arg1,
                    n=command.arg2
                )
                self.label_index = self.label_index + 1
            elif command.op == 'function':
                code_template = code_template.format(
                    file=vm_file,
                    l1=self.label_index,
                    l2=self.label_index+1,
                    f=command.arg1,
                    m=command.arg2
                )
                self.label_index = self.label_index + 2
            elif command.op == 'return':
                code_template = code_template.format(
                    f=current_function
                )

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
