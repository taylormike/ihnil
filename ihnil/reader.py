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

    def output(self):
        module = ast.parse(self.inpt)

if file_extension == ".py":
    with open(args.file_name.name) as fn:
        file_contents = fn.read()
    instance = MainIHNIL(file_contents)

    if args.read:
        print("READ")
    elif args.write:
        print("WRITE")
    else:
        print("ELSE")
else:
    print("\nPlease enter a Python file\n")
