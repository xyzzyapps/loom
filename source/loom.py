# animation::quine:1
# Welcome!
# imports

from flexicon import Lexer
import tempfile
from operator import itemgetter
import re
import time
import sys
import os
import sqlite3
from sqlite3 import Error

# animation::quine:2
# globals

conn = None

# animation::quine:3
# basic sql

def execute(conn, query, args):
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    return cur.lastrowid

# animation::quine:4
# basic sql

def select_query(conn, query, params, mapper):
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        mapper(row)

# animation::quine:5

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# animation::quine:6

sql_create_codebase_table = """
CREATE TABLE IF NOT EXISTS codebase (
    file_path text NOT NULL,
    array_index integer NOT NULL,
    type text NOT NULL,
    line text NOT NULL
);
"""

# animation::quine:6

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

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

# animation::quine:7

def parse(st, print_wrapper, code_wrapper, with_fence=True):
    lexer = Lexer().simple(
        (r'(\n[\n ]*)', lambda _1: ('NL', _1)),
        (r'^#(.+\n)', lambda _1: ('COMMENT', _1)),
        (r'(\s*)(.+?)#(.+\n)', lambda _1, _2, _3: ('PARTIAL_COMMENT', _1, _2, _3)),
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
    sequence_index = 0

    for token in tokens:
        if line_count > 1:
            is_program_beginning = False

        if token[0] == "COMMENT":
            current_comment_sequence += token[1]
            line_count += 1
        if token[0] == "PARTIAL_COMMENT":
            if len(token[2]) > 0:
                current_code_sequence += token[1]
            current_code_sequence += token[2]
            current_comment_sequence += token[3]
            line_count += 1
        if token[0] == "LINE":
            current_code_sequence += token[1]
            current_code_sequence += token[2]
            if len(token[1]) == 0:
                if current_code_sequence != "" and current_comment_sequence != "":
                    code_sequences.append(current_code_sequence)
                    comment_sequences.append(current_comment_sequence)
                    sequence_index += 1
                    current_code_sequence = ""
                    current_comment_sequence = ""

            line_count += 1
        else:
            line_count += 1

    if current_code_sequence != "" and current_comment_sequence != "":
        code_sequences.append(current_code_sequence)
        comment_sequences.append(current_comment_sequence)

    for comment in comment_sequences:
        print_wrapper(comment)
    if with_fence:
        code_wrapper("\n```")
    for code in code_sequences:
        code_wrapper(code)
    if with_fence:
        print_wrapper("\n```")

    return [code_sequences, comment_sequences]


if __name__ == "__main__":

    arg1 = sys.argv[1]

    if arg1 == "--clean-source":
        parse(sys.stdin.read(), null_printer, output_printer, with_fence=False)

    if arg1 == "--generate-docs":

        os.system("safe-rm codedb.db")
        conn = create_connection("codedb.db")
        create_table(conn, sql_create_codebase_table)

        arg2 = sys.argv[2]
        output_dir = ends_with_slash(sys.argv[3])

        def run_parser(file_name):
            global conn
            file_contents = open(file_name).read()
            file_printer = file_printer_prototype(output_dir, file_name)
            sequences = parse(file_contents, file_printer, file_printer)
            sql = ''' INSERT INTO codebase(file_path, array_index, type, line)
                VALUES(?,?,?,?) '''
            for i, e in enumerate(sequences[0]):
                execute(conn, sql, [file_name, i, "code", e])
            for i, e in enumerate(sequences[1]):
                execute(conn, sql, [file_name, i, "comment", e])


        dir_walk(arg2, run_parser)

    if arg1 == "--generate-index":

        arg2 = sys.argv[2]

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

    if arg1 == "--generate-terminal-show":

        show = {}
        arg2 = sys.argv[2]
        output_dir = ends_with_slash(sys.argv[3])
        slide_delay = int(sys.argv[4])
        animation_name = sys.argv[5]

        def run_parser(file_name):
            global conn
            global show
            file_contents = open(file_name).read()
            file_printer = file_printer_prototype(output_dir, file_name)
            sequences = parse(file_contents, file_printer, file_printer)
            sql = '''INSERT INTO codebase(file_path, array_index, type, line)
                VALUES(?,?,?,?)'''

            for i, e in enumerate(sequences[1]):
                if "animation::" in e:
                    lines = e.split("\n")
                    first_line =  lines.pop(0)
                    clean_comment = "\n".join(lines)
                    name, no = first_line.split("::")[1].split(":")

                    if name in show:
                        code = sequences[0][i]
                        if "," in no:
                            ns = no.split(",")
                            for n in ns:
                                show[name].append([n, clean_comment, code])
                        else:
                            show[name].append([no, clean_comment, code])
                    else:
                        if "," in no:
                            ns = no.split(",")
                        code = sequences[0][i]
                        show[name] = [[no, clean_comment, code]]

        dir_walk(arg2, run_parser)

        for slide in sorted(show[animation_name], key=itemgetter(0)):
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(slide[1].encode())
                temp.flush()
                os.system("cowsay -W 72 <" + temp.name)
                time.sleep(slide_delay)
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(slide[2].encode())
                temp.flush()
                os.system("cowsay -W 72 <" + temp.name)
                time.sleep(slide_delay)

    if arg1 == "--comment-stats":

        comments_count = 0
        code_count = 0

        def comment_counter(row):
            global comments_count
            comments_count += len(row[3].split("\n"))

        def code_counter(row):
            global code_count
            code_count += len(row[3].split("\n"))

        conn = create_connection("codedb.db")
        sql = """ SELECT * FROM codebase WHERE type=? """
        select_query(conn, sql, ["comment"], comment_counter)
        select_query(conn, sql, ["code"], code_counter)
        print("comments loc: " + str(comments_count))
        print("code loc: " + str(code_count))
        print("ratio (higher is better): " + str(comments_count / code_count))





