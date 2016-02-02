"""
Python script parsing module.

Description:

    Prounounced "eye-nil"; this tool allows the user to identify and improve
    upon nested "if" loop statements.

Arguments:

    file_name       The target file to parse
    -h, --help      Show help message
    -r, --read      Displays the errors and location in the terminal
    -w, --write     Inserts recommended code changes into the script

"""

import argparse
import os
import tokenize
import operator
import itertools
import keyword


parser = argparse.ArgumentParser(description="Python 'if' loop improver",
                                 epilog="For details see \
                                         https://github.com/forstmeier/ihnil")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="Temporary %(prog)s POSITIONAL help string")

output = parser.add_mutually_exclusive_group()
output.add_argument("-r", "--read",
                    action="store_true",
                    help="Temporary READ help string")
output.add_argument("-w", "--write",
                    action="store_true",
                    help="Temporary WRITE help string")

args = parser.parse_args()
string_name = str(args.file_name.name)
file_extension = os.path.splitext(string_name)[1]

COND = {"<", ">", "<=", ">=", "!=", "==", "in", "not in", "is", "is not"}

print()

if file_extension == ".py":
    with open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))

    full_dict = {g: list(i)
                 for g, i in itertools.groupby(tokens, lambda x: x.start[0])}

    if_rows = [token.start[0] for token in tokens if token.string == "if"]

    if_nest = [list(map(operator.itemgetter(1), i))
               for g, i in itertools.groupby(enumerate(if_rows),
                                             lambda ix: ix[0] - ix[1])]

    nest_list = []
    for row_nums in if_nest:
        if len(row_nums) > 1:
            front = min(row_nums) - 1
            back = max(row_nums) + 1
            row_nums.insert(0, front)
            row_nums.append(back)
            nest_list.append(row_nums)

    for nest in nest_list:
        print("Nested loop error number {}".format(nest_list.index(nest) + 1))
        print("Start line: {}, end line: {}\n".format(min(nest), max(nest)))
        for row in nest:
            if row in full_dict.keys():
                print("[>   {}".format(full_dict[row][0].line.rstrip()))

    if args.write:
        print("{} is the WRITE version".format(string_name))

        eval_list = [full_dict[row] for nest in nest_list for row in nest
                     if row in full_dict.keys()]

        built_in = [x for x in dir(__builtins__) if x[0].islower()
                    or x == "True" or x == "False"]

        for e in eval_list:
            for r in e:
                if (tokenize.tok_name[r.type] == "NAME"
                    and r.string not in built_in
                        and r.string not in keyword.kwlist):
                    print(r.string)

    # TEST.py problem:
    # def manyif(val):
    #    if val > 0:
    #       if val != 2:
    #          if val < 3:
    #             print("Eggs & spam")

    # TEST.py solution:
    # if 3 > val > 0 and val != 2:
    #    print("Eggs & spam")

    # greater       >
    # less          <
    # greaterequal  >=
    # lessequal     <=
    # notequal      !=
    # equal         ==

    else:
        print("{} is the READ version".format(string_name))

    print()

else:
    print("Please enter a Python file\n")
