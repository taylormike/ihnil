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


class MainIHNIL(object):
    def __init__(self, tk):
        self.tk = tk
        self.if_dict = {g: list(i)
                        for g, i in itertools.groupby(self.tk,
                                                      lambda x: x.start[0])}
        self.rows = [token.start[0] for token in self.tk
                     if token.string == "if"]
        self.nest = [lst for lst in
                     [list(map(operator.itemgetter(1), i))
                      for g, i in itertools.groupby(enumerate(self.rows),
                                                    lambda ix: ix[0] - ix[1])]
                     if len(lst) > 1]
        self.toks = [self.if_dict[row] for n in self.nest for row in n
                     if row in self.if_dict.keys()]
        self.blt_in = [x for x in dir(__builtins__) if x[0].islower()
                       or x == "True" or x == "False"]

    def _read_out(self):
        for n in self.nest:
            print("Nested error number {}".format(self.nest.index(n) + 1))
            print("Start row: {}, end row: {}\n".format(min(n), max(n)))
            for row in n:
                if row in self.if_dict.keys():
                    print("[>   {}".format(self.if_dict[row][0].line.rstrip()))

    def _write_out(self):
        for e in self.toks:
            for r in e:
                if (tokenize.tok_name[r.type] == "NAME"
                    and r.string not in self.blt_in
                        and r.string not in keyword.kwlist):
                    print(r.string)

if file_extension == ".py":
    with open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))
else:
    print("Please enter a Python file\n")

if args.write:
    instance = MainIHNIL(tokens)
    instance._write_out()
    print("\n{} is the WRITE version\n".format(string_name))
else:
    instance = MainIHNIL(tokens)
    instance._read_out()
    print("\n{} is the READ version\n".format(string_name))
