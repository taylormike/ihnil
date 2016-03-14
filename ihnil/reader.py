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


BINOPS = {"Add()": "+", "Sub()": "-",
          "Mult()": "*", "Div()": "/",
          "FloorDiv()": "//", "Mod": "%",
          "Pow()": "**"}

STRICT = {"Gt()": ">", "Lt()": "<"}
LOOSE = {"GtE()": ">=", "LtE()": "<="}
EQUALITY = {"Eq()": "==", "NotEq()": "!="}
IDENTITY = {"Is()": "is", "IsNot()": "is not"}
INCLUSION = {"In()": "in", "NotIn()": "not in"}


class ReadIHNIL(ast.NodeVisitor):
    """This class provides simple error node code print out."""

    count = 1

    def visit_If(self, node):
        """Overridden ast module method."""
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' error number {} <]".format(self.count))
            print(codegen.to_source(node) + "\n")
            self.count += 1


class WriteIHNIL(ast.NodeVisitor):
    """This class allows for comprehensive code optimization."""

    def visit_If(self, node):
        """Overridden ast module method."""
        if isinstance(node.body[0], ast.If):

            segment = list()

            self.next_line(node, segment)

            print(segment)

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

    def next_line(self, node, holder):
        """Parse nodes and provide optimized code."""
        if ("test" in node._fields and isinstance(node.test, ast.Compare)
            and node.orelse == []):

            variable = str()
            items = list()
            counter = 0

            def _evaluator(inpt, choice, comps=0):
                if choice == "left":
                    inp = inpt.test.left
                elif choice == "comp":
                    inp = inpt.test.comparators[comps]
                elif choice == "nest_left":
                    inp = inpt.left
                elif choice == "nest_right":
                    inp = inpt.right

                if isinstance(inp, ast.Name):
                    items.append("#" + inp.id)
                    nonlocal counter
                    counter += 1
                elif isinstance(inp, ast.Num):
                    items.append(inp.n)
                elif isinstance(inp, ast.Str):
                    items.append(inp.s)
                elif isinstance(inp, (ast.List, ast.Dict, ast.Tuple, ast.Set)):
                    items.append(ast.dump(inp))
                elif isinstance(inp, ast.BinOp):
                    items.append("(")
                    _evaluator(inp, "nest_left")
                    items.append(ast.dump(inp.op))
                    _evaluator(inp, "nest_right")
                    items.append(")")

            _evaluator(node, "left")
            for oper in node.test.ops:
                items.append(ast.dump(oper))
            num_of_comps = len(node.test.comparators)
            if num_of_comps == 0:
                _evaluator(node, "comp")
            else:
                for number in range(num_of_comps):
                    _evaluator(node, "comp", comps=number)

#            if counter == 1:
#                print("=" * 40 + " # 1")
#            elif counter == 2:
#                print("=" * 40 + " # 2")
#            else:
#                print("=" * 40 + " # MORE")

            if holder:
                holder.append(" and ")
                holder.append(items)
            else:
                holder.append(items)

            self.next_line(node.body[0], holder)

            # TODO: algorithm to optimize structure for if test
            # TODO: store optimized loops in separate variables

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
        """Overridden ast module method."""
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
