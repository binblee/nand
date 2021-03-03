import sys
import os
from enum import Enum


class TOKEN(Enum):
    INVALID = 0
    KEYWORD = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONTENT = 4
    IDENTIFIER = 5


class Tokenizer:
    KEYWORDS = ('class', 'constructor', 'function',
                'method', 'field', 'static', 'var', 'int',
                'char', 'boolean', 'void', 'true', 'false',
                'null', 'this', 'let', 'do', 'if', 'else',
                'while', 'return')
    SYMBOLS = ('{', '}', '(', ')', '[', ']', '.',
               ',', ';', '+', '-', '*', '/', '&',
               '|', '<', '>', '=', '~')

    MARKUPS = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '&': '&amp;',
    }

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.tokens = []
        self.block_comment = False
        self.index = -1
        self.__load()

    def advance(self):
        self.index += 1

    def has_more(self):
        return len(self.tokens) > 0 and self.index < len(self.tokens) - 1

    def get_token(self):
        return self.tokens[self.index]

    def get_token_type(self):
        current = self.get_token()
        token_type = TOKEN.INVALID
        if current in self.KEYWORDS:
            token_type = TOKEN.KEYWORD
        elif current in self.SYMBOLS:
            token_type = TOKEN.SYMBOL
        elif current.isnumeric():
            token_type = TOKEN.INT_CONSTANT
        elif current.isidentifier():
            token_type = TOKEN.IDENTIFIER
        elif len(current) >= 2 and current[0] == '"' and current[-1] == '"':
            s = current[1:len(current) - 1]
            if s.find('"') < 0 and s.find('\n') < 0:
                token_type = TOKEN.STRING_CONTENT
        return token_type

    def get_keyword(self):
        return self.get_token()

    def get_symbol(self):
        return self.get_token()

    # only used for xml markup
    def get_symbol_markup(self):
        token = self.get_token()
        if token in self.MARKUPS:
            token = self.MARKUPS[token]
        return token

    def get_integer_constant(self):
        return self.get_token()

    def get_string_constant(self):
        token = self.get_token()
        return token[1:len(token) - 1]

    def get_identifier(self):
        return self.get_token()

    def get_invalid(self):
        return self.get_token()

    def __load(self):
        with open(self.source_filename, 'r') as reader:
            for line in reader.readlines():
                self.tokens += self.__split(line)

    def __split(self, line):
        result = []
        line_without_comments = self.__remove_comments(line)
        if line_without_comments != '':
            quotes = line_without_comments.split('"')
            q_index = 0
            while q_index < len(quotes):
                if q_index % 2 == 0:
                    # even index, not string constant
                    result += self.__pad_symbol_with_space(quotes[q_index]).split()
                else:
                    # odd index, string constant
                    result += [f'"{quotes[q_index]}"']
                q_index += 1
        return result

    def __pad_symbol_with_space(self, str_input):
        line = str_input
        for s in self.SYMBOLS:
            if line.find(s) >= 0:
                line = line.replace(s, f' {s} ')
        return line

    def __remove_comments(self, line):
        result_line = ''
        if self.block_comment:
            blk_comment_end = line.find('*/')
            if blk_comment_end > 0:
                blk_comment_start = line.find('/*')
                if (blk_comment_start >= 0) and (blk_comment_start < blk_comment_end):
                    # syntax error:
                    sys.exit('block comment syntax error')
                elif blk_comment_start > blk_comment_end:
                    result_line = line[blk_comment_end + 2:blk_comment_start]
                else:
                    result_line = line[blk_comment_end + 2:]
                self.block_comment = False
        else:
            blk_comment_start = line.find('/*')
            if blk_comment_start >= 0:
                blk_comment_end = line.find('*/')
                if blk_comment_end > blk_comment_start:
                    # xxx/*yyy*/zzz
                    result_line = line[0:blk_comment_start] + line[blk_comment_end + 2:]
                elif (blk_comment_end >= 0) and (blk_comment_end < blk_comment_start):
                    # xxx*/yyy/*zzz
                    result_line = line[blk_comment_end + 2:blk_comment_start]
                else:
                    result_line = line[0:blk_comment_start]
                    self.block_comment = True
            else:
                blk_comment_start = line.find('//')
                if blk_comment_start >= 0:
                    result_line = line[0:blk_comment_start]
                else:
                    result_line = line
        return result_line

    def save_xml(self, xml_filename):
        with open(xml_filename, 'w') as writer:
            print('<tokens>', file=writer)
            while self.has_more():
                s = ''
                self.advance()
                token_type = self.get_token_type()
                if token_type == TOKEN.KEYWORD:
                    s = f'<keyword> {self.get_keyword()} </keyword>'
                elif token_type == TOKEN.SYMBOL:
                    s = f'<symbol> {self.get_symbol_markup()} </symbol>'
                elif token_type == TOKEN.INT_CONSTANT:
                    s = f'<integerConstant> {self.get_integer_constant()} </integerConstant>'
                elif token_type == TOKEN.STRING_CONTENT:
                    s = f'<stringConstant> {self.get_string_constant()} </stringConstant>'
                elif token_type == TOKEN.IDENTIFIER:
                    s = f'<identifier> {self.get_identifier()} </identifier>'
                else:
                    s = f'<invalid> {self.get_invalid()} </invalid>'
                print(s, file=writer)
            print('</tokens>', file=writer)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('python tokenizer.py [source.jack | source directory]')
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
            Tokenizer(file).save_xml(file.replace('.jack', '_outT.xml'))
