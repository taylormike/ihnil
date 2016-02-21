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


class ReadIHNIL(ast.NodeVisitor):
    count = 1

    def visit_If(self, node):
        print("### If error number {} ###".format(self.count))
        print(codegen.to_source(node) + "\n")
        self.count += 1


class WriteIHNIL(ast.NodeVisitor):
    def visit_If(self, node):
        print("Write node {} {}".format(node.lineno, node))
        self.generic_visit(node)


class ElseIHNIL(ast.NodeVisitor):
    count = 0

    def visit_If(self, node):
        if isinstance(node.body[0], ast.If):
            self.count += 1
            print("Nested 'if' node {} start line {}".format(self.count,
                                                             node.lineno))
            self.endline(node, self.count)

    def endline(self, node, count):
        if isinstance(node, ast.If):
            self.endno = node.lineno
            node = node.body[0]
            self.endline(node, count)
        else:
            print("Nested 'if' node {} end line {}".format(count, self.endno))
            


#        start = node.lineno
#        if isinstance(node.body[0], ast.If):
#            end = node.body[0].lineno
#            print(start, end)
#            self.generic_visit(node)


if file_extension == ".py":
    with open(args.file_name.name) as f:
        file_contents = f.read()
    module = ast.parse(file_contents)

    if args.read:
        ReadIHNIL().visit(module)
    elif args.write:
        WriteIHNIL().visit(module)
    else:
        ElseIHNIL().visit(module)
else:
    print("\nPlease enter a Python file\n")
