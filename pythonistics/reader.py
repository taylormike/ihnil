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

    if_list = []
    for token in tokens:
        if token.string == "if":
            if_line = token.line.rstrip()
            if_row = token.start[0]
            if_list.append([if_row, if_line])

    b_count = 0
    for if_value in if_list:
        a_count = if_value[0]
        a_value = str(if_value)
        if a_count - b_count == 1:
            print(b_value)
            print(a_value)
        b_count = a_count
        b_value = a_value



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

    if args.read:
        print("{} is the READ version".format(string_name))

    elif args.write:
        print("{} is the WRITE version".format(string_name))

    else:
        print("{} is the OTHER version".format(string_name))

    print()

else:
    print("Please enter a Python file")
