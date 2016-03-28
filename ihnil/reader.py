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


binops = ["Add()", "Sub()",
          "Mult()", "Div()",
          "FloorDiv()", "Mod", "Pow()"]

ops = ["Gt()", "Lt()",
       "GtE()", "LtE()",
       "Eq()", "NotEq()",
       "Is()", "IsNot()",
       "In()", "NotIn()"]


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

            segment = list()
            variables = list()

            self.next_line(node, segment, variables)

            variables = list(set(variables))

            segment.sort(key=lambda x: (self._ops_find(x), self._var_find(x)))

            print(segment)
            print(variables)

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

    def next_line(self, node, seg_list, var_list):
        """Node line evaluation function called recursively."""
        if isinstance(node, ast.If) and node.orelse == []:
            seg_list.append(node)

            self._var_list(node, "left", var_list)
            self._var_list(node, "comparators", var_list)

            self.next_line(node.body[0], seg_list, var_list)

    def _var_list(self, node, option, var_list):
        """List building method for use in the lambda sorting."""
        if option == "left":
            if isinstance(node.test, ast.Call):
                var_list.append(node.test.func.id)
            else:
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
            self._var_list(inp, "bin_left", var_list)
            self._var_list(inp, "bin_right", var_list)

    def _ops_find(self, item):
        """First method for lambda sorting according to operator list."""
        return ops.index(ast.dump(item.test.ops[0]))

    def _var_find(self, item):
        """Second method for lambda sorting according to variable names."""
        if isinstance(item.test, ast.Call):
            return item.text.func.id
        else:
            inp = item.test.left
            if isinstance(inp, ast.Name):
                return inp.id
            elif isinstance(inp, ast.BinOp):
                return self._binop_find(inp)
            else:
                return self._comp_find(item)

    def _binop_find(self, item, side_choice="left"):
        """
        First sub-method called by the variable sorting algorithm.

        Used in parsing binary operator statements.
        """
        if side_choice == "left":
            inp = item.left
        elif side_choice == "right":
            inp = item.right

        if isinstance(inp, ast.Name):
            return inp.id
        elif isinstance(inp, ast.BinOp):
            self._binop_find(inp, side_choice="left")
        else:
            self._binop_find(item, side_choice="right")

    def _comp_find(self, item):
        """
        Second sub-method called by the variable sorting algorithm.

        Used in running through the items in the right-side comparators list.
        """
        for itm in item.test.comparators:
            if isinstance(itm, ast.Name):
                return itm.id
            else:
                self._binop_find(itm)

            # TODO: built out algebraic optimization for binops nodes
            # TODO: algorithm to compare nodes within the node list
            # TODO: delete redundancies in the compared nodes
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
