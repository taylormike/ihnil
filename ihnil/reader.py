"""
Python script parsing module.

Description:

    Prounounced "eye-nil"; this tool allows the user to identify and improve
    upon nested "if" loop statements.

Arguments:

    file_name       The target file to parse
    -h, --help      Show help message
    -r, --read      Displays the errors and location in the terminal
    -w, --write     Inserts recommended code changes into the script
"""

import argparse
import os
import ast
import codegen


parser = argparse.ArgumentParser(description="Python 'if' loop optimizer",
                                 epilog="For details see \
                                         https://github.com/forstmeier/ihnil")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="input file for %(prog)s optimization")

output = parser.add_mutually_exclusive_group()
output.add_argument("-r", "--read",
                    action="store_true",
                    help="find and print 'if' loop errors to the terminal")
output.add_argument("-w", "--write",
                    action="store_true",
                    help="write 'if' alternatives to the module and terminal")

args = parser.parse_args()
string_name = str(args.file_name.name)
file_extension = os.path.splitext(string_name)[1]


class MainIHNIL(object):
    def __init__(self, inpt):
        self.inpt = ast.parse(inpt)

    if_list = []
    def if_stmt_sort(self, nodes):
        for node in nodes.body:
            if "body" in node._fields:
                if isinstance(node, ast.If):
                    self.if_list.append(node)
                else:
                    self.if_stmt_sort(node)

    def _read_out(self):
        for itm in instance.if_list:
            print(codegen.to_source(itm) + "\n")

    def _write_out(self):
        for itm in instance.if_list:
            print("WRITE NODE EXAMPLE")

    def _else_out(self):
        for itm in instance.if_list:
            print("Nested 'if': line #{}".format(itm.lineno))


if file_extension == ".py":
    with open(args.file_name.name) as f:
        file_contents = f.read()
    instance = MainIHNIL(file_contents)
    instance.if_stmt_sort(instance.inpt)

    if args.read:
        print("READ")
        instance._read_out()
    elif args.write:
        print("WRITE")
        instance._write_out()
    else:
        print("ELSE")
        instance._else_out()
else:
    print("\nPlease enter a Python file\n")
