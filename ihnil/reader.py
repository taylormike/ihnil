"""
IHNIL main parsing module.

Provides the interface for evaluating a given target file
"""

import argparse
import os
import ast
import codegen


parser = argparse.ArgumentParser(description="Python 'if' loop optimizer",
                                 epilog="For details see "
                                 "https://github.com/forstmeier/ihnil")

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
        """Subclassed ast module method."""
        if isinstance(node.body[0], ast.If):
            print("[> Nested 'if' error number {} <]".format(self.count))
            print("[> Error node starts on {} <]\n".format(node.lineno))
            print(codegen.to_source(node) + "\n")
            input("Hit Enter to continue\n")
            self.count += 1


class WriteIHNIL(ast.NodeVisitor):
    """This class allows for comprehensive code optimization."""

    def visit_If(self, node):
        """Subclassed ast module method."""
        if isinstance(node.body[0], ast.If) and node.orelse == []:

            self.next_line(node)

            decider = input("Would you like to:\n"
                            "Accept change  ->  'a'\n"
                            "Edit manually  ->  'e'\n"
                            "Mark complete  ->  'c'\n"
                            "Provide your choice and hit Enter: ")

            if decider == "a":
                self._accept_change()
            elif decider == "e":
                self._edit_manually()
            elif decider == "c":
                self._mark_complete()
            else:
                print("No action taken")

    def next_line(self, line):
        """Node line evaluation function called recursively."""
        if isinstance(line, ast.If) and line.orelse == []:
            self.sort_algo(line)
            self.next_line(line.body[0])

    def sort_algo(self, input_line):
        if isinstance(input_line.body[0], (ast.Call,
                                           ast.NameConstant, ast.Name)):
            # yield input_line
            pass
        elif isinstance(input_line.body[0], ast.If):
            if len(input_line.body[0].test.ops) > 1:
                # yield input_line
                pass
            else:
                # self.eval_left(input_line.body[0].test)
                pass
                # ^ the returned values from this are added to "holder list"
                # ^ this is for each "input_line"
                # ^ the "holder list" is then compared iteratively to
                # ^ -> "final list"

    def eval_left(self, line, store=list()):
        store.insert(0, line.comparators[0])
        store.insert(0, line.ops[0])
        if isinstance(line.left, ast.Name):
            store.insert(0, line.left.id)
            # yield store
        elif isinstance(line, ast.BinOp):
            self.eval_binop(line.left, store)

    def eval_comp(self, line, store=list()):
        store.insert(0, line.left)
        store.insert(0, line.ops[0])
        if isinstance(line, ast.Name):
            store.insert(0, line.comparators[0].id)
            # yield store
        elif isinstance(line, ast.BinOp):
            self.eval_binop(line.left, store)

    def eval_binop(self, line, store):
        if isinstance(line.left, ast.Name):
            op = self.oper_swap(line.op)
            store.append(op)
            store.append(line.right)
            # yield store
        elif isinstance(line.left, ast.BinOp):
            op = self.oper_swap(line.op)
            store.append(op)
            store.append(line.right)
            self.eval_binop(line.left, store)

        if isinstance(line.right, ast.Name):
            op = self.oper_swap(line.op)
            store.append(op)
            store.append(line.left)
            # yield store

    def oper_swap(self, oper):
        OPER_MAP = {"Add()": "-", "Sub()": "+",
                    "Mult()": "/", "Div()": "*",
                    "FloorDiv()": "//", "Mod()": "%", "Pow()": "**",
                    "Gt()": "Lt()", "Lt()": "Gt()",
                    "GtE()": "LtE()", "LtE()": "GtE()",
                    "Eq()": "NotEq()", "NotEq()": "Eq()",
                    "Is()": "IsNot()", "IsNot()": "Is()",
                    "In()": "NotIn()", "NotIn()": "In()"}
        return OPER_MAP[oper]

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
            print("[> Nested 'if' number {} start "
                  "line {}".format(self.count, node.lineno))
            self.end_line(node, self.count)
            self.count += 1

    def end_line(self, node, count):
        """Private recursive method to loop down to the last node line."""
        if isinstance(node, ast.If):
            self.endno = node.lineno
            self.end_line(node.body[0], count)
        else:
            print("[> Nested 'if' number {} end "
                  "line {}".format(count, self.endno))


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
