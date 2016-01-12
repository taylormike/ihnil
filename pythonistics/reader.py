import argparse
import os
import builtins
import tokenize
import keyword


parser = argparse.ArgumentParser(description="File processer",
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

    if args.read:
        print("{} is the READ version".format(string_name))

    elif args.write:
        print("{} is the WRITE version".format(string_name))
        # Look for areas where lines can be removed from the code
        # Insert specific code tags (start/end, enumerated)
        # Print out specific lines of code
        # Yes / No / Edit / Quit
        # Yes --> Make changes, move to next line
        # No --> No changes, move to next line
        # Edit --> Open file in editor
        # Quit --> Exit
    else:
        print("{} is the OTHER version".format(string_name))
        # Basic catch-all

else:
    print("Please enter a Python file")
