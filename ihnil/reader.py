"""
IHNIL main parsing module.

Provides the interface for evaluating a given target file

"""

import argparse
import os
import ast
import codegen


parser = argparse.ArgumentParser(description="Python 'if' loop optimizer",
                                 epilog="For details see " \
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


additive = ["Add()", "Sub()"]
productive = ["Mult()", "Div()"]
others = ["FloorDiv()", "Mod", "Pow()"]
binops = [additive, productive, others]

strict = ["Gt()", "Lt()"]
loose = ["GtE()", "LtE()"]
equal = ["Eq()", "NotEq()"]
identity = ["Is()", "IsNot()"]
inclusion = ["In()", "NotIn()"]
operators = [strict, loose, equal, identity, inclusion]


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
        if len(input_line.body[0].test.ops) > 1:
            pass
        elif isinstance(input_line.body[0].test, ast.Call):
            pass
        elif isinstance(input_line.body[0].test, ast.NameConstant):
            pass
        elif isinstance(input_line.body[0].test, ast.Name):
            pass
        else:
            pass  # function calls go here

    def eval_left(self, line, store=list()):
        # Note: ^ argument input -> left.body[0].test
        left = line.left
        if isinstance(left, ast.Name):
            # self.eval_oper(left)
            store.insert(0, line.body[0].test.comparators[0])
            store.insert(0, line.body[0].test.ops[0])
            store.insert(0, left.id)
        elif isinstance(left, ast.BinOp):
            self.eval_binop(line, store)
        else:
            pass

    def eval_oper(self, line):  # decomission -> not likely needed
        oper = line.body[0].test.ops[0]
        return oper

    def eval_comp(self, line):  # only called on eval_left -> else
        comp = line.body[0].test.comparators[0]

    def eval_binop(self, line, store):
        # Note: ^ argument input -> left.body[0].test
        if isinstance(line.left, ast.Name):
            store_l = store
            store_l.append(line.op)  # TODO: insert operator swap function
            store_l.append(line.right)
        elif isinstance(line.left, ast.BinOp):
            pass

        if isinstance(line.right, ast.Name):
            store_r = store
            store_r.append(line.op)  # TODO: insert operator swap function
            store_r.append(line.left)
        elif isinstance(line.right, ast.BinOp):
            pass



        bin_left = line.left
        bin_oper = line.op
        bin_right = line.right









# TODO: idea 1:
#
# definitions:
# error node        -> group of nested if statements
# error lineno      -> each individual if statement line
# fixed list        -> collection of temporarily optimized lines
# holder list       -> temporary holder for unmatched optimized lines
#
# structure:
# look at each error line of the error node
# check if there is one than more comparator operator in the error line
# ^ if there is then append the error node to the fixed list
# ^ else run the full parsing operation
# if the fixed list is empty
# ^ if there is only one optimized (one variable) line
# ^ ^ add the optimized line to the fixed list
# ^ else add all possible optimizations (multiple variables) to a holder list
# ^ add the holder list to the fixed list
# else if the fixed list is not empty
# ^ compare each possible optimized alternative (one/more variables)
# ^ to each of the items within fixed list
# ^ ^ if the item in fixed list is a holder list
# ^ ^ ^ compare each of the optimzed alternatives to each holder list item
# ^ ^ if the comparision fits 1. variable and 2. operator family
# ^ ^ ^ merge the two lines together
# ^ ^ ^ if the compared item was in a holder list
# ^ ^ ^ ^ delete the holder list
# ^ ^ ^ delete all optimized alternatives for the current error line
# return a fully optimzied list

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
            print("[> Nested 'if' number {} start " \
                  "line {}".format(self.count, node.lineno))
            self._end_line(node, self.count)
            self.count += 1

    def _end_line(self, node, count):
        """Private recursive method to loop down to the last node line."""
        if isinstance(node, ast.If):
            self.endno = node.lineno
            self._end_line(node.body[0], count)
        else:
            print("[> Nested 'if' number {} end " \
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
