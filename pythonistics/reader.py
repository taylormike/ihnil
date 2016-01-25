import argparse
import os
import tokenize
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

    rows = list(set([token.start[0] for token in tokens]))
    row_list = [token.line.rstrip() for token in tokens
                if token.string == "\n"]
    row_list.insert(0, "\n")
    row_list.append("\n")
    token_list = [[(token.string, tokenize.tok_name[token.exact_type])
                  for token in tokens
                  if token.start[0] == row_var]
                  for row_var in rows]

    combo_list = [[i, j, k] for i, j, k in zip(rows, row_list, token_list)]

    for g, i in itertools.groupby(tokens, lambda x: x.start[0]):
        print(g, list(i))

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
