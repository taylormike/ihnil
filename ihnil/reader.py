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


BINOPS = ["Add()", "Sub()", "Mult()", "Div()", "FloorDiv()", "Mod", "Pow()"]

ops = ["Gt()", "Lt()", "GtE()", "LtE()", "Eq()", "NotEq()",
       "Is()", "IsNot()", "In()", "NotIn()"]


class ReadIHNIL(ast.NodeVisitor):
    """This class provides simple error node code print out."""

    count = 1

    def visit_If(self, node):
        """Subclassed ast module method."""
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' error number {} <]".format(self.count))
            print(codegen.to_source(node) + "\n")
            self.count += 1


class WriteIHNIL(ast.NodeVisitor):
    """This class allows for comprehensive code optimization."""

    def visit_If(self, node):
        """Subclassed ast module method."""
        if isinstance(node.body[0], ast.If) and node.orelse == []:

            segment = list()
            variables = list()

            self.next_line(node, segment, variables)

            variables = list(set(variables))

            segment.sort(key=lambda x: (self.ops_find(x), self.var_find(x)))

            print(segment)
            print(variables)

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
                print("No action taken")

    def next_line(self, node, seg_list, var_list):
        """Node line evaluation function called recursively."""
        if isinstance(node, ast.If) and node.orelse == []:
            seg_list.append(node)

            self.evaluator(node, "left", var_list)
            self.evaluator(node, "comparators", var_list)

            self.next_line(node.body[0], seg_list, var_list)

    def evaluator(self, node, option, var_list):
        if option == "left":
            inp = node.test.left
        elif option == "comparators":
            inp = node.test.comparators[0]
        elif option == "bin_left":
            inp = node.left
        elif option == "bin_right":
            inp = node.right

        if isinstance(inp, ast.Name):
            var_list.append(inp.id)
        elif isinstance(inp, ast.BinOp):
            self.evaluator(inp, "bin_left", var_list)
            self.evaluator(inp, "bin_right", var_list)

    def ops_find(self, item):
        return ops.index(ast.dump(item.test.ops[0]))

    def var_find(self, item, option="left"):
        if option == "left":
            inp = item.test.left
        elif option == "comparators":
            inp = item.test.comparators[0]
        elif option == "bin_left":
            inp = item.left
        elif option == "bin_right":
            inp = item.right

        if isinstance(inp, ast.Name):
            return inp.id
            self.var_find(item, "comparators")
        elif isinstance(inp, ast.BinOp):
            self.var_find(inp, "bin_left")
            self.var_find(inp, "bin_right")

            # TODO: lambda function to sort by variables
            # TODO: algorithm to optimize structure for if test
            # TODO: store optimized loops in separate variables
            # TODO: reestablish user choice & next node option

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
        """Subclassed ast module method."""
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
