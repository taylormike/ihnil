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
        self.inpt = inpt
        self.module = ast.parse(self.inpt)

    def selector(self, num):
        self.num = num

    def _first1(self):
        print(codegen.to_source(node))

    def _first2(self):
        print(node._fields)

    def _first3(self):
        print("Nested error on line {}".format(node.lineno))

    def _second1(self):
        for itm in node.body:
            if isinstance(itm, ast.If):
                print("Start line {}".format(itm.lineno))
                print(codegen.to_source(itm) + "\n")

    def _second2(self):
        for itm in node.body:
            if isinstance(itm, ast.If):
                print(itm._fields)

    def _second3(self):
        for itm in node.body:
            if isinstance(itm, ast.If):
                print("Nested error on line {}".format(itm.lineno))

    FIRST = {1: _first1, 2: _first2, 3: _first3}
    SECOND = {1: _second1, 2: _second2, 3: _second3}

    def result_out(self):
        for node in self.module.body:
            if isinstance(node, ast.If):
                self.FIRST[self.num](self)
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.SECOND[self.num](self)

if file_extension == ".py":
    with open(args.file_name.name) as f:
        file_contents = f.read()
    instance = MainIHNIL(file_contents)

    if args.read:
        print("READ")
        instance.selector(1)
        instance.result_out()
    elif args.write:
        print("WRITE")
        instance.selector(2)
        instance.result_out()
    else:
        print("ELSE")
        instance.selector(3)
        instance.result_out()
else:
    print("\nPlease enter a Python file\n")
