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
    """Core object for code parsing and output methods."""

    def __init__(self, inp):
        """
        Establish necessary variables.

        self.inp        : tokenized input module code list
        self.ordr       : dictionary of rows and associated tokens
        self.rows       : row values of "if" statement tokens
        self.nest       : list of consecutive row value lists
        self.toks       : (not used yet)
        self.blt_in     : (not used yet)
        """
        self.inp = inp
        self.ordr = {grp: list(itm)
                     for grp, itm in itertools.groupby(self.inp,
                                                       lambda x: x.start[0])}
        self.rows = [tkn.start[0] for tkn in self.inp
                     if tkn.string == "if"]
        self.nest = [lst for lst in
                     [list(map(operator.itemgetter(1), i))
                      for g, i in itertools.groupby(enumerate(self.rows),
                                                    lambda ix: ix[0] - ix[1])]
                     if len(lst) > 1]
        self.toks = [self.ordr[row] for nst in self.nest for row in nst
                     if row in self.ordr.keys()]
        self.blt_in = [blt for blt in dir(__builtins__) if blt[0].islower()
                       or blt == "True" or blt == "False"]

    def _read_out(self):
        for nst in self.nest:
            spaces = 2
            print("Nested error number {}".format(self.nest.index(nst) + 1))
            print("Start row: {}, end row: {}\n".format(min(nst), max(nst)))
            for row in nst:
                if row in self.ordr.keys():
                    print("[>{}{}".format(" " * spaces,
                                          self.ordr[row][0]
                                          .line.lstrip().rstrip()))
                spaces += 4

    def _write_out(self):
        for lst in self.toks:
            for row in lst:
                if (tokenize.tok_name[row.type] == "NAME"
                    and row.string not in self.blt_in
                        and row.string not in keyword.kwlist):
                    print(row.string)

if file_extension == ".py":
    with open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))
    if args.write:
        instance = MainIHNIL(tokens)
        instance._write_out()
        print("\n{} is the WRITE version\n".format(string_name))
    else:
        instance = MainIHNIL(tokens)
        instance._read_out()
        print("\n{} is the READ version\n".format(string_name))
else:
    print("Please enter a Python file\n")
