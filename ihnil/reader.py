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
            # this is where the sorting/combining method will go
            # it will take "self.next_line(node)" as its argument

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

            print(self.sort_algo(line))

            self.next_line(line.body[0])

    def sort_algo(self, input_line):
        line_holder = list()
        if isinstance(input_line.test, ast.Compare):
            if len(input_line.test.ops) > 1:
                line_holder.append(self.bulk_clean(input_line))
            else:
                self.eval_left(input_line, line_holder)
                self.eval_comp(input_line, line_holder)
        else:
            line_holder.append(self.bulk_clean(input_line))
        return line_holder

    def eval_left(self, input_line, line_holder):
        left_holder = list()
        left_bin = list()
        left_holder.append(self.oper_clean(ast.dump(input_line.test.ops[0])))
        if isinstance(input_line.test.comparators[0], ast.BinOp):
            for element in self.left_binop_clean(input_line.test
                                                 .comparators[0], left_bin):
                left_holder.append(element)
        else:
            left_holder.append(self.var_clean(input_line.test.comparators[0]))

        if isinstance(input_line.test.left, ast.Name):
            left_holder.insert(0, input_line.test.left.id)
            line_holder.append(left_holder)
        elif isinstance(input_line.test.left, ast.BinOp):
            self.eval_binop(input_line.test.left, left_holder, line_holder)
        return line_holder

    def eval_comp(self, input_line, line_holder):
        comp_holder = list()
        comp_bin = list()
        comp_holder.append(self.oper_swap(ast.dump(input_line.test.ops[0])))
        if isinstance(input_line.test.left, ast.BinOp):
            for element in self.right_binop_clean(input_line.test.left,
                                                  comp_bin):
                comp_holder.append(element)
        else:
            comp_holder.append(self.var_clean(input_line.test.left))

        if isinstance(input_line.test.comparators[0], ast.Name):
            comp_holder.insert(0, input_line.test.comparators[0].id)
            line_holder.append(comp_holder)
        elif isinstance(input_line.test.comparators[0], ast.BinOp):
            self.eval_binop(input_line.test.comparators[0],
                            comp_holder, line_holder)
        return line_holder

    def eval_binop(self, input_line, alt_holder, line_holder):
        if isinstance(input_line.left, ast.Name):
            left_holder = alt_holder[:]
            left_holder.append(self.oper_swap(ast.dump(input_line.op)))
            left_holder.append(self.var_clean(input_line.right))
            left_holder.insert(0, input_line.left.id)
            line_holder.append(left_holder)
            del(left_holder)
        elif isinstance(input_line.left, ast.BinOp):
            self.eval_binop(input_line.left, left_holder, line_holder)

        if isinstance(input_line.right, ast.Name):
            right_holder = alt_holder[:]
            right_holder.append(self.oper_swap(ast.dump(input_line.op)))
            right_holder.append(self.var_clean(input_line.left))
            right_holder.insert(0, input_line.right.id)
            line_holder.append(right_holder)
            del(right_holder)

    def oper_clean(self, oper):
        OPER_ALL = {"Add()": "+", "Sub()": "-",
                    "Mult()": "*", "Div()": "/",
                    "FloorDiv()": "//", "Mod()": "%", "Pow()": "**",
                    "Gt()": ">", "Lt()": "<",
                    "GtE()": ">=", "LtE()": "<=",
                    "Eq()": "==", "NotEq()": "!=",
                    "Is()": "Is", "IsNot()": "Is Not",
                    "In()": "In", "NotIn()": "Not In"}
        return OPER_ALL[oper]

    def oper_swap(self, oper):
        OPER_DICT = {"Add()": "-", "Sub()": "+",
                     "Mult()": "/", "Div()": "*",
                     "FloorDiv()": "//", "Mod()": "%", "Pow()": "**",
                     "Gt()": "<", "Lt()": ">",
                     "GtE()": "<=", "LtE()": ">=",
                     "Eq()": "==", "NotEq()": "!=",
                     "Is()": "Is", "IsNot()": "Is Not",
                     "In()": "In", "NotIn()": "Not In"}
        return OPER_DICT[oper]

    def var_clean(self, const):
        if isinstance(const, ast.Num):
            return const.n
        elif isinstance(const, ast.Str):
            return const.s
        elif isinstance(const, (ast.List, ast.Set)):
            new_list = list()
            for element in const.elts:
                new_list.append(self.var_clean(element))
            return new_list
        elif isinstance(const, ast.NameConstant):
            return const.value
        elif isinstance(const, ast.Name):
            return const.id

    def left_binop_clean(self, chunk, temp_list):
        temp_list.append(self.oper_clean(ast.dump(chunk.op)))
        temp_list.append(self.var_clean(chunk.right))
        if isinstance(chunk.left, ast.BinOp):
            self.left_binop_clean(chunk.left, temp_list)
        else:
            temp_list.insert(0, self.var_clean(chunk.left))
        return temp_list

    def right_binop_clean(self, chunk, temp_list):
        temp_list.append(self.oper_clean(ast.dump(chunk.op)))
        temp_list.append(self.var_clean(chunk.right))
        if isinstance(chunk.left, ast.BinOp):
            self.right_binop_clean(chunk.left, temp_list)
        else:
            temp_list.insert(0, self.var_clean(chunk.left))
        return temp_list

    def bulk_clean(self, bulk):
        bulk_hold = list()
        if isinstance(bulk.test.left, ast.BinOp):
            for piece in self.bulk_bin_clean(bulk.test.left, list()):
                bulk_hold.append(piece)
        else:
            bulk_hold.append(self.var_clean(bulk.test.left))
        bulker = zip(bulk.test.ops, bulk.test.comparators)
        for item in bulker:
            bulk_hold.append(self.oper_clean(ast.dump(item[0])))
            if isinstance(item[1], ast.BinOp):
                for piece in self.bulk_bin_clean(item[1], list()):
                    bulk_hold.append(piece)
            else:
                bulk_hold.append(self.var_clean(item[1]))
        return bulk_hold

    def bulk_bin_clean(self, bulk_bin, bulk_list):
        bulk_list.append(self.oper_clean(ast.dump(bulk_bin.op)))
        bulk_list.append(self.var_clean(bulk_bin.right))
        if isinstance(bulk_bin.left, ast.BinOp):
            self.bulk_bin_clean(bulk_bin.left, bulk_list)
        else:
            bulk_list.insert(0, self.var_clean(bulk_bin.left))
        return bulk_list

    def compare_algo(self, comp_list):
        result_list = list()
        while len(comp_list) > 0:
            cur_elem = comp_list.pop()
            combo = [(x, y) for x in cur_elem for y in comp_list
                     if x[0] == y[0]]



            # if len(cur_elem) > 1 and len(comp_list) > 1:
            #     temp_name1 = [(x, y) if x[0] == y[0]
            #                   for x in cur_elem
            #                   for y in comp_list]
            # elif len(cur_elem) > 1 and len(comp_list) == 1:
            #     temp_name2 = [(x, comp_list[0]) if x[0] == comp_list[0]
            #                   for x in cur_elem]
            # elif len(comp_list) > 1 and len(cur_elem) == 1:
            #     temp_name3 = [(y, cur_elem[0]) if y[0] == cur_elem[0]
            #                   for y in comp_list[0]]
            # else:
            #     if cur_elem[0] == comp_list[0]:
            #         temp_name4 = (cur_elem[0], comp_list[0])

    def _accept_change(self):
        """Private method to automatically apply optimized code."""
        pass
        # this will simply add the code into the document
        # either 1. replace completely or 2. add in surrounded with lines

    def _edit_manually(self):
        """Private method to allow for manual code adjustments."""
        pass
        # this will alllow the user to edit as needed

    def _mark_complete(self):
        """Private method to mark and ignore non-optimized code."""
        pass
        # add the location/content of the code node to an additional
        # external file and ignore it


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
