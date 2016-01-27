import argparse
import os
import tokenize
import operator
import itertools


parser = argparse.ArgumentParser(description="Python code shortener",
                                 epilog="This is the end")

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

print()

if file_extension == ".py":
    with tokenize._builtin_open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))

    full_list = [(g, list(i))
                 for g, i in itertools.groupby(tokens, lambda x: x.start[0])]

    if_rows = [i[0] for i in full_list if "if" in [j.string for j in i[1]]]
    
    if_nest = [list(map(operator.itemgetter(1), i))
               for g, i in itertools.groupby(enumerate(if_rows),
               lambda ix: ix[0] - ix[1])]

    # --------------------------------------------------------------
    # Printing out comment lines to the script will require
    #   the file to be opened with 'read' and 'write' permissions
    # Also include code necessary for identifying the
    #   printed comments
    # --------------------------------------------------------------

    if args.read:
        print("{} is the READ version".format(string_name))
    elif args.write:
        print("{} is the WRITE version".format(string_name))
    else:
        print("{} is the OTHER version".format(string_name))

    print()

else:
    print("Please enter a Python file")
