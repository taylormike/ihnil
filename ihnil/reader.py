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

            self.next_line(node)

            decider = input("Would you like to:\n"
                            "Accept change  ->  'a'\n"
                            "Edit manually  ->  'e'\n"
                            "Mark complete  ->  'c'\n"
                            "Provide your choice and hit 'enter': ")

            if decider == "a":
                self._accept_change()
            elif decider == "e":
                self._edit_manually()
            elif decider == "c":
                self._mark_complete()
            else:
                print("Skipped")

    def next_line(self, node):
        """Parse nodes and provide optimized code."""
        if "test" in node._fields and isinstance(node.test, ast.Compare):
            if isinstance(node.test.left, ast.Name):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("1. NAME: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.Str):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("2. STR: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.Num):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("3. NUM: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.List):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("4. LIST: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.Tuple):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("5. TUPLE: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.Set):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("6. SET: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.Dict):
                left = ast.dump(node.test.left)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("6. DICT: {} {} {}".format(left, ops, comp))
            elif isinstance(node.test.left, ast.BinOp):
                left = ast.dump(node.test.left.left)
                op = ast.dump(node.test.left.op)
                right = ast.dump(node.test.left.right)
                ops = ast.dump(node.test.ops[0])
                comp = ast.dump(node.test.comparators[0])
                print("7. BINOP: {} {} {} {} {}".format(left, op, right,
                                                        ops, comp))
#            print("8. {}".format(ast.dump(node.test)))

            # TODO: algorithm to optimize structure for if test
            # TODO: store optimized loops in separate variables

            self.next_line(node.body[0])

    def _accept_change(self):
        """Private method to automatically apply optimized code."""
        # TODO: identify and remove error loops from module
        # TODO: take associated optimized loop and print into module
        pass

    def _edit_manually(self):
        """Private method to allow for manual code adjustments."""
        # TODO: mark off error loops in module
        pass

    def _mark_complete(self):
        """Private method to mark and ignore non-optimized code."""
        # TODO: take down error code line information
        # TODO: print into a separate file that holds data
        pass


class ElseIHNIL(ast.NodeVisitor):
    """This class is the default error node line number identifier."""

    count = 1

    def visit_If(self, node):
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' number {} start line {}".format(self.count,
                                                                  node.lineno))
            self._end_line(node, self.count)
            self.count += 1

    def _end_line(self, node, count):
        """Private recursive method to loop down to the last node line."""
        if isinstance(node, ast.If):
            self.endno = node.lineno
            self._end_line(node.body[0], count)
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
