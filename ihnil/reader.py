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


binops = ["Add()", "Sub()", "Mult()", "Div()", "FloorDiv()", "Mod", "Pow()"]

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

    def next_line(self, node, seg_list=list()):
        """Node line evaluation function called recursively."""
        if isinstance(node, ast.If) and node.orelse == []:
            seg_list.append(node)

            self.next_line(node.body[0], seg_list)
            # TODO: return the list of error node lines

    def sort_algo(self, start_list, end_list):
        # Note: start_list  -> input list of unordered error node lines
        # Note: end_list    -> returned list of sorted/optimized node lines
        for line in start_list:
            if len(line.body[0].test.ops) > 1:
                end_list.append(line)
            else:
                # TODO:
                # include "isinstance" handling -> ast.Call
                # include "True/False" handling -> ast.NameConstant
                # include variable handline     -> ast.Name
                pass
                # TODO: various function call operations here

    def find_vars(self, input_line, side_choice):
        if side_choice == "left":
            eval_value = input_line.body[0].test.left
        elif side_choice == "comp":
            eval_value = input_line.body[0].test.comparators[0]

        if isinstance(eval_value, ast.Name):
            pass
            # TODO: call sorter function
        elif isinstance(eval_value, ast.BinOp):
            find_binop(eval_value, bin_choice="left")
        else:
            find_vars(input_line, side_choice="comp")

    def find_binop(self, input_value, bin_choice):
        if bin_choice == "left":
            bin_value = input_value.left
        elif bin_choice == "right":
            bin_value = input_value.right

        if isinstance(bin_value, ast.Name):
            sorter(found_in="binop")
        elif isinstance(bin_value, ast.BinOp):
            find_binop(bin_value, bin_choice="left")
        else:
            find_binop(input_value, bin_choice="right")

    def sorter(self, found_in):
        if found_in == "left":
            pass
        elif found_in == "binop":
            pass
        elif found_in == "comp":
            pass

    # TODO: needed functions:
    # find variables        -> takes the left side of error line
    # parse binops          -> activated if needed
    # parse comparators     -> activated if needed
    # sort function         -> called following each parser

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
            print("[> Nested 'if' number {} start \
                  line {}".format(self.count, node.lineno))
            self._end_line(node, self.count)
            self.count += 1

    def _end_line(self, node, count):
        """Private recursive method to loop down to the last node line."""
        if isinstance(node, ast.If):
            self.endno = node.lineno
            self._end_line(node.body[0], count)
        else:
            print("[> Nested 'if' number {} end \
                  line {}".format(count, self.endno))


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
