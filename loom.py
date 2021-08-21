from flexicon import Lexer
import re
import sys
import os

def output_printer(x):
    print(x, end="\n")

def parse(st, print_wrapper):
    lexer = Lexer().simple(
        (r'(\n[\n ]*)', lambda x: ('NL', x)),
        (r'^(#.+)\n', lambda x: ('COMMENT', x)),
        (r'(\s*)(.+)(#.+)\n', lambda x: ('PARTIAL_COMMENT', x)),
        (r'^(.+)\n', lambda x: ('LINE', x)),
    )

    tokens = lexer.lex(st)
    stack = []

    count = 1
    line_count = 1
    in_middle = []
    is_program_beginning = True

    for token in tokens:
        if count > 1:
            is_program_beginning = False

        if token[0] == "COMMENT":
            print_wrapper(token[1])
            line_count += 1
        if token[0] == "PARTIAL_COMMENT":
            print_wrapper(token[1])
            line_count += 1
        else:
            # print_wrapper(e[1])
            line_count += 1

if __name__ == "__main__":
    parse(sys.stdin.read(), output_printer)

