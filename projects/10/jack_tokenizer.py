import sys
import os
from enum import Enum


class TokenType(Enum):
    INVALID = 0
    KEYWORD = 1
    SYMBOL = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTIFIER = 5


class JackToken:
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

    def __init__(self, token_string):
        self.token_string = token_string
        self.token_type = self.__set_type()

    def __set_type(self):
        ts = self.token_string
        token_type = TokenType.INVALID
        if ts in self.KEYWORDS:
            token_type = TokenType.KEYWORD
        elif ts in self.SYMBOLS:
            token_type = TokenType.SYMBOL
        elif ts.isnumeric():
            token_type = TokenType.INT_CONSTANT
        elif ts.isidentifier():
            token_type = TokenType.IDENTIFIER
        elif len(ts) >= 2 and ts[0] == '"' and ts[-1] == '"':
            s = ts[1:len(ts) - 1]
            if s.find('"') < 0 and s.find('\n') < 0:
                token_type = TokenType.STRING_CONSTANT
        return token_type

    def get_type(self):
        return self.token_type

    def get_keyword(self):
        return self.token_string

    def get_symbol(self):
        return self.token_string

    # only used for xml markup
    def get_symbol_markup(self):
        token_markup = self.token_string
        if token_markup in self.MARKUPS:
            token_markup = self.MARKUPS[token_markup]
        return token_markup

    def get_integer_constant(self):
        return self.token_string

    def get_string_constant(self):
        token = self.token_string
        return token[1:len(token) - 1]

    def get_identifier(self):
        return self.token_string

    def get_invalid(self):
        return self.token_string


class JackTokenizer:

    def __init__(self, source_filename):
        self.source_filename = source_filename
        self.tokens = []
        self.block_comment = False
        self.index = -1
        self.SYMBOLS = JackToken.SYMBOLS
        self.__load()

    def advance(self):
        if self.has_more():
            self.index += 1
            return JackToken(self.tokens[self.index])

    def has_more(self):
        return len(self.tokens) > 0 and self.index < len(self.tokens) - 1

    def peek_next(self, inc=1):
        if self.has_more():
            return JackToken(self.tokens[self.index+inc])

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
                tk = self.advance()
                token_type = tk.get_type()
                if token_type == TokenType.KEYWORD:
                    s = f'<keyword> {tk.get_keyword()} </keyword>'
                elif token_type == TokenType.SYMBOL:
                    s = f'<symbol> {tk.get_symbol_markup()} </symbol>'
                elif token_type == TokenType.INT_CONSTANT:
                    s = f'<integerConstant> {tk.get_integer_constant()} </integerConstant>'
                elif token_type == TokenType.STRING_CONSTANT:
                    s = f'<stringConstant> {tk.get_string_constant()} </stringConstant>'
                elif token_type == TokenType.IDENTIFIER:
                    s = f'<identifier> {tk.get_identifier()} </identifier>'
                else:
                    s = f'<invalid> {tk.get_invalid()} </invalid>'
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
            JackTokenizer(file).save_xml(file.replace('.jack', '_outT.xml'))
