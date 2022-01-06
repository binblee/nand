import os
import sys

from jack_syntax_parser import SyntaxParser
from jack_vm_translator import VM_Translator

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python jack_compiler.py [source.jack | source directory]')
    else:
        source_path = sys.argv[1]
        files = []
        if os.path.isdir(source_path):
            for file in os.listdir(source_path):
                if file.endswith('.jack'):
                    files.append(os.path.join(source_path, file))
        elif os.path.isfile(source_path):
            files.append(source_path)
        else:
            sys.exit('input file or directory does not exist.')
        for file in files:
            parser = SyntaxParser(file)
            xml_filename = file.replace('.jack', '_out.xml')
            parser.save_as_xml(xml_filename)
            vm_filename = file.replace('.jack', '.vm')
            translator = VM_Translator(parser.get_syntax_tree())
            translator.translate(vm_filename)

# TODO:
# 1. check type of subroutine (function/method) when it is being invoked.