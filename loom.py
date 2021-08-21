from flexicon import Lexer
import re
import sys
import os

def dir_walk(dir, mapper):
    for root, dirs, files in os.walk(dir):
        for file in files:
            mapper( root + '/' + file)

def ends_with_slash(dir_name):
    if dir_name.endswith("/"):
        return dir_name
    else:
        return dir_name + "/"


def output_printer(x):
    print(x, end="")

def null_printer(x):
    None

def file_printer_prototype(output_dir, file_name):
    parent_dir = os.path.dirname(output_dir + file_name)
    os.system("mkdir -p "  + parent_dir)

    def printer(text):
        nonlocal output_dir
        nonlocal file_name
        with open(output_dir + file_name + ".md", "a") as myfile:
            myfile.write(text)

    return printer

def string_state():
    final_str = ""

    def getter():
        nonlocal final_str
        return final_str

    def setter(x):
        nonlocal final_str
        final_str += x

    return [getter, setter]

def parse(st, print_wrapper, code_wrapper):
    lexer = Lexer().simple(
        (r'(\n[\n ]*)', lambda _1: ('NL', _1)),
        (r'^(#.+\n)', lambda _1: ('COMMENT', _1)),
        (r'(\s*)(.+)(#.+\n)', lambda _1, _2, _3: ('PARTIAL_COMMENT', _1, _2, _3)),
        (r'^(\s*)(.+\n)', lambda _1, _2: ('LINE', _1, _2)),
    )

    tokens = lexer.lex(st)
    stack = []

    line_count = 1
    in_middle = []
    is_program_beginning = True

    comment_sequences = []
    code_sequences = []

    current_code_sequence = ""
    current_comment_sequence = ""

    for token in tokens:
        if line_count > 1:
            is_program_beginning = False

        if token[0] == "COMMENT":
            print_wrapper(token[1])
            current_comment_sequence += token[1]
            line_count += 1
        if token[0] == "PARTIAL_COMMENT":
            print_wrapper(token[3])
            current_code_sequence += token[1]
            current_code_sequence += token[2]
            code_wrapper(token[1] + token[2])
            current_comment_sequence += token[3]
            line_count += 1
        if token[0] == "LINE":
            current_code_sequence += token[2]
            if len(token[1]) == 0:
                code_sequences.append(current_code_sequence)
                comment_sequences.append(current_comment_sequence)
                current_code_sequence = ""
                current_comment_sequence = ""
            code_wrapper(token[2])
            line_count += 1
        else:
            line_count += 1

    code_sequences.append(current_code_sequence)
    comment_sequences.append(current_comment_sequence)


if __name__ == "__main__":

    arg1 = sys.argv[1]

    if arg1 == "--test":
        parse(sys.stdin.read(), null_printer, output_printer)


    if arg1 == "--generate-docs":

        output_dir = ends_with_slash(sys.argv[3])

        def run_parser(file_name):
            file_contents = open(file_name).read()
            file_printer = file_printer_prototype(output_dir, file_name)
            parse(file_contents, file_printer, output_printer)

        dir_walk(arg2, run_parser)

    if arg1 == "--generate-index":
        print("""Welcome
=======

.. toctree::
    :caption: Table of Contents
    :maxdepth: 5
    :glob:
    :includehidden:

""")

        def run_parser(file_name):
            print("    " + re.sub(arg2 + "/", "", file_name))

        dir_walk(arg2, run_parser)

