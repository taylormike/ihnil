"""
IHNIL main parsing module.

Provides the interface for evaluating a given target file.
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
            print("[> Error node starts on line {} <]".format(node.lineno))
            print("-" * 55)
            print(codegen.to_source(node))
            print("-" * 55)
            input("Hit Enter to continue\n")
            ReadIHNIL.count += 1


class WriteIHNIL(ast.NodeVisitor):
    """This class allows for comprehensive code optimization."""

    with open(args.file_name.name, "r") as f:
        contents = f.readlines()
    contents = list(enumerate(contents))
    results = []

    count = 1

    def visit_If(self, node):
        """Subclassed ast module method."""
        if isinstance(node.body[0], ast.If) and node.orelse == []:

            print("[> Nested 'if' error number {} corrected "
                  "syntax <]".format(WriteIHNIL.count))

            collector = list()

            line_val = node.lineno
            col_val = node.col_offset
            new_node = self.next_line(node, collector)
            new_node = self.compare_algo(new_node)
            new_node = self.combine_algo(new_node)
            out_node = self.result_format(new_node, col_val)
            new_node = self.comment_out(out_node)

            for item in out_node:
                print(item[:-2])

            WriteIHNIL.results.append(self.apply_enumeration(new_node,
                                                             line_val))

            WriteIHNIL.count += 1

            # input("Hit Enter to continue\n")


    def next_line(self, line, collector):
        """Pull apart the error node recursively into individual lines."""
        if isinstance(line, ast.If) and line.orelse == []:
            collector.append(self.sort_algo(line))
            self.next_line(line.body[0], collector)
        return collector

    def sort_algo(self, input_line):
        """Perform various sorting functions as the input line dictates."""
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
        """Evaluate left side of the comparison argument line."""
        left_holder = list()
        left_bin = list()
        left_holder.append(self.oper_clean(input_line.test.ops[0]))
        if isinstance(input_line.test.comparators[0], ast.BinOp):
            if ast.dump(input_line.test.comparators[0].op) == "Mod()":
                left_holder.append(input_line.test.comparators[0].left.id)
                left_holder.append(self.oper_clean(input_line.test
                                                   .comparators[0].op))
                left_holder.append(self.var_clean(input_line.test
                                                  .comparators[0].right))
            else:
                left_holder.extend(self.binop_clean(input_line.test
                                                    .comparators[0], left_bin))
        else:
            left_holder.append(self.var_clean(input_line.test.comparators[0]))

        if isinstance(input_line.test.left, ast.Name):
            left_holder.insert(0, input_line.test.left.id)
            line_holder.append(left_holder)
        elif isinstance(input_line.test.left, ast.BinOp):
            if ast.dump(input_line.test.left.op) == "Mod()":
                left_holder.insert(0, input_line.test.left.left.id)
                left_holder.insert(1, self.oper_clean(input_line.test.left.op))
                left_holder.insert(2, self.var_clean(input_line.test
                                                     .left.right))
                line_holder.append(left_holder)
            else:
                self.eval_binop(input_line.test.left, left_holder, line_holder)
        return line_holder

    def eval_comp(self, input_line, line_holder):
        """Evaulate right side of the comparison argument line."""
        comp_holder = list()
        comp_bin = list()
        comp_holder.append(self.oper_flip(self.oper_clean(input_line
                                                          .test.ops[0])))
        if isinstance(input_line.test.left, ast.BinOp):
            comp_holder.extend(self.binop_clean(input_line.test.left,
                                                comp_bin))
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
        """Umbrella method to handle recursively parsing binary operators."""
        if isinstance(input_line.left, ast.Name):
            left_holder = alt_holder[:]
            left_holder.append(self.oper_flip(self.oper_clean(input_line.op)))
            left_holder.append(self.var_clean(input_line.right))
            left_holder.insert(0, input_line.left.id)
            line_holder.append(left_holder)
            del(left_holder)
        elif isinstance(input_line.left, ast.BinOp):
            self.eval_binop(input_line.left, left_holder, line_holder)

        if isinstance(input_line.right, ast.Name):
            right_holder = alt_holder[:]
            right_holder.append(self.oper_flip(self.oper_clean(input_line.op)))
            right_holder.append(self.var_clean(input_line.left))
            right_holder.insert(0, input_line.right.id)
            line_holder.append(right_holder)
            del(right_holder)

    def oper_clean(self, oper):
        """Translate AST nodes into text equivalents."""
        oper = ast.dump(oper)
        OPER_DICT = {"Add()": "+", "Sub()": "-",
                     "Mult()": "*", "Div()": "/",
                     "FloorDiv()": "//", "Mod()": "%", "Pow()": "**",
                     "Gt()": ">", "Lt()": "<",
                     "GtE()": ">=", "LtE()": "<=",
                     "Eq()": "==", "NotEq()": "!=",
                     "Is()": "is", "IsNot()": "is not",
                     "In()": "in", "NotIn()": "not in"}
        return OPER_DICT[oper]

    def oper_flip(self, oper):
        """Convert text operator into opposite operand."""
        OPER_ONE = {"+": "-", "-": "+", "*": "/", "/": "*"}
        OPER_TWO = {">": "<", "<": ">", ">=": "<=", "<=": ">="}
        OPER_THREE = {"==": "==", "!=": "!="}
        OPER_FOUR = {"is": "is", "is not": "is not",
                     "in": "in", "not in": "not in"}

        if oper in OPER_ONE:
            return OPER_ONE[oper]
        elif oper in OPER_TWO:
            return OPER_TWO[oper]
        elif oper in OPER_THREE:
            return OPER_THREE[oper]
        elif oper in OPER_FOUR:
            return OPER_FOUR[oper]

    def var_clean(self, const):
        """Transformation specific node elements into text items."""
        if isinstance(const, ast.Num):
            return str(const.n)
        elif isinstance(const, ast.Str):
            return const.s
        elif isinstance(const, (ast.List, ast.Set)):
            new_list = list()
            for element in const.elts:
                new_list.append(self.var_clean(element))
            return str(new_list)
        elif isinstance(const, ast.NameConstant):
            return const.value
        elif isinstance(const, ast.Name):
            return const.id

    def binop_clean(self, chunk, temp_list):
        """Recursively translate binary operation segments."""
        temp_list.append(self.oper_clean(chunk.op))
        temp_list.append(self.var_clean(chunk.right))
        if isinstance(chunk.left, ast.BinOp):
            self.binop_clean(chunk.left, temp_list)
        else:
            temp_list.insert(0, self.var_clean(chunk.left))
        return temp_list

    def bulk_clean(self, bulk):
        """Parse and translate complex, multi-operator segments."""
        bulk_hold = list()
        if isinstance(bulk.test.left, ast.BinOp):
            for piece in self.bulk_bin_clean(bulk.test.left, list()):
                bulk_hold.append(piece)
        else:
            bulk_hold.append(self.var_clean(bulk.test.left))
        bulker = zip(bulk.test.ops, bulk.test.comparators)
        for item in bulker:
            bulk_hold.append(self.oper_clean(item[0]))
            if isinstance(item[1], ast.BinOp):
                for piece in self.bulk_bin_clean(item[1], list()):
                    bulk_hold.append(piece)
            else:
                bulk_hold.append(self.var_clean(item[1]))
        return bulk_hold

    def bulk_bin_clean(self, bulk_bin, bulk_list):
        """Call to handle binary operations in multi-operator segments."""
        bulk_list.append(self.oper_clean(bulk_bin.op))
        bulk_list.append(self.var_clean(bulk_bin.right))
        if isinstance(bulk_bin.left, ast.BinOp):
            self.bulk_bin_clean(bulk_bin.left, bulk_list)
        else:
            bulk_list.insert(0, self.var_clean(bulk_bin.left))
        return bulk_list

    def compare_algo(self, comp_node):
        """Find all related segments and group results."""
        sorted_list = list()
        comp_elem = comp_node.pop()
        while len(comp_node) > 0:
            for ce in comp_elem:
                for node_elem in comp_node:
                    for ne in node_elem:
                        if ce[0] == ne[0] and self.oper_flip(ce[1]) == ne[1]:
                            sorted_list.append([ce, ne])
                            del comp_node[comp_node.index(node_elem)]
                            comp_elem = comp_node.pop()
                            break
                        else:
                            sorted_list.append([comp_elem[0]])
                            comp_elem = comp_node.pop()
                            break
                        break
                    break
        else:
            sorted_list.append([comp_elem[0]])
        return sorted_list

    def combine_algo(self, comp_list):
        """Couple segments in each group and return optimzed results."""
        result_list = list()
        for elem in comp_list:
            if len(elem) > 1:
                elem[0].reverse()
                oper = self.oper_flip(elem[0][-2])
                complete_segment = elem[0][:-2]
                complete_segment.append(oper)
                complete_segment.extend(elem[1])
                result_list.append(complete_segment)
            else:
                result_list.append(elem[0])
        return result_list

    def result_format(self, line_collection, column):
        """Transform optimized lists into strings encased with line markers."""
        finished_node = list()
        for line in line_collection:
            white_space = " " * column
            finished_node.append(white_space + "if " + " ".join(line) + ":\n")
            column += 4
        marker_line = "# " + "-" * 55
        finished_node.insert(0, marker_line)
        finished_node.append(marker_line)
        return finished_node

    def comment_out(self, unmarked_list):
        """Apply comments to the target code block; input must be a list."""
        marked_list = ["# " + item for item in unmarked_list]
        return marked_list

    def apply_enumeration(self, input_list, line_start):
        """Enumerate optimized line list to allow targeted insertion."""
        output_list = [(number, line) for number, line
                       in enumerate(input_list, line_start)]
        return output_list

    def insert_fixes(self):
        for item in WriteIHNIL.results[::-1]:
            WriteIHNIL.contents[item[0][0]:item[0][0]] = item
        with open("TEST.txt", "w") as f:
            f.writelines(WriteIHNIL.contents)


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
