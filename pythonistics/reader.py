import argparse
import os
import tokenize


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

    line_list = [(token.start, token.line.rstrip())
                 for token in tokens
                 if token.string == "\n"]

    row = 0
    row_list, token_list = [], []
    for token in tokens:
        if token.start[0] == row:
            row_list.append((token.string,
                            tokenize.tok_name[token.exact_type]))
        else:
            token_list.append(row_list)
            row_list = []
            row_list.append((token.string,
                             tokenize.tok_name[token.exact_type]))
            row += 1

    # --------------------------------------------------------------
    # Stacked if conditional loops -> dict lookup
    #   Generate possible dict structures
    # --------------------------------------------------------------
    # Identical code -> functions
    # Identical string -> string variables
    # Triple quotes on three lines -> single line docstring
    # --------------------------------------------------------------
    # Printing out comment lines to the script will require
    #   the file to be opened with 'read' and 'write' permissions
    # Also include code necessary for identifying the
    #   printed comments
    # --------------------------------------------------------------
    # Apply pep8 to each document that is run through pythonistics
    #   This will keep all code looking "pythonic" for analysis
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
