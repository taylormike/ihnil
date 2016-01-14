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

    def tokener():
        for token in tokens:
            token_name = tokenize.tok_name[token.exact_type]
            token_range = "{}-{}".format(token.start, token.end)
            print("{: <20}{: <15}{: <15}".format(token_range,
                                                 token_name,
                                                 token.string))

    next_position = 0
    temporary = ()
    for token in tokens:
        if token.string == "if":
            print_length = len(token.line)
            if token.start[0] - next_position == 1:
                print(" * " * print_length)
                print("Nested 'if' statements")
                print(temporary[0], temporary[1].rstrip())
                print(token.start, token.line.rstrip())
                print(" * " * print_length)
            next_position = token.start[0]
            temporary = (token.start, token.line)
    # Multiple nested if loops -> list comprehension
    #   Generate different results based on
    #   what conditionals are used (e.g. "!=" or "==")

    # TODO (1/14/16) - add in the token collection list

    for token in tokens:
        if token.string == "if":
            position = token.start
            if position[1] - next_position == 0:
                print("Stacked 'if' statements")
            next_position = position[1]
    # Stacked if conditional loops -> dict lookup
    #   Generate possible dict structures

    # Identical code -> functions
    # Identical string -> string variables
    # Triple quotes on three lines -> single line docstring

    # Printing out comment lines to the script will require
    #   the file to be opened with 'read' and 'write' permissions
    # Also include code necessary for identifying the
    #   printed comments

    if args.read:
        print("{} is the READ version".format(string_name))

    elif args.write:
        print("{} is the WRITE version".format(string_name))

    else:
        print("{} is the OTHER version".format(string_name))

    print()

else:
    print("Please enter a Python file")
