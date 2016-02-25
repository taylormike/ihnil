"""
IHNIL main parsing module.

Provides the interface for evaluating a given target file

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
    """This class provides simple error node code print out."""

    count = 1

    def visit_If(self, node):
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' error number {} <]".format(self.count))
            print(codegen.to_source(node) + "\n")
            self.count += 1


class WriteIHNIL(ast.NodeVisitor):
    """This class allows for comprehensive code optimization."""

    def visit_If(self, node):
        if isinstance(node.body[0], ast.If):
            global node_vars
            global node_oprs
            node_vars = set()
            node_oprs = set()
            print(self.next_line(node))

    def next_line(self, node):
        if "test" in node._fields and isinstance(node.test, ast.Compare):
            if isinstance(node.test.left, ast.Name):
                node_vars.add(node.test.left.id)
                node_oprs.add(ast.dump(node.test.ops[0]))
#            print("1 {}".format(ast.dump(node.test)))
#            print("2 {}".format(ast.dump(node.test.left)))
#            print("3 {}".format(node._fields))
#            print("4 {}".format(node.orelse))
            self.next_line(node.body[0])
        return (node_vars, node_oprs)


class ElseIHNIL(ast.NodeVisitor):
    """This class is the default error node line number identifier."""

    count = 1

    def visit_If(self, node):
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' number {} start line {}".format(self.count,
                                                                  node.lineno))
            self.endline(node, self.count)
            self.count += 1

    def endline(self, node, count):
        if isinstance(node, ast.If):
            self.endno = node.lineno
            self.endline(node.body[0], count)
        else:
            print("[> Nested 'if' number {} end line {}".format(count,
                                                                self.endno))


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
