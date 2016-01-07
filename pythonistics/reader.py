import argparse
import os
import builtins
import tokenize


parser = argparse.ArgumentParser(description="File processer",
                                 epilog="This is the end")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="Temporary %(prog)s POSITIONAL help string")

output = parser.add_mutually_exclusive_group()
output.add_argument("--stats",
                    action="store_true",
                    help="Temporary STATS help string")
output.add_argument("--short",
                    action="store_true",
                    help="Temporary SHORT help string")
output.add_argument("--nicer",
                    action="store_true",
                    help="Temporary NICER help string")

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

    if args.stats:
        print("{} is the STATS version\n".format(string_name))

        tokener()

        print()

        print("Strings: {}".format(sum([1 for token in tokens if
              tokenize.tok_name[token.exact_type] == "STRING"])))

        print("'def': {}".format(sum([1 for token in tokens if
              token.string == "def"])))

        print("'class': {}".format(sum([1 for token in tokens if
              token.string == "class"])))

        print()

    elif args.short:
        print("{} is the SHORT version\n".format(string_name))
        # Insert specific code tags (start/end, enumerated)
        # Print out specific lines of code
        # Yes / No / Edit / Quit
        # Yes --> Make changes, move to next line
        # No --> No changes, move to next line
        # Edit --> Open file in editor
        # Quit --> Exit
    elif args.nicer:
        print("{} is the NICER version\n".format(string_name))
        # See above - similar structure
    else:
        print("{} is the OTHER version\n".format(string_name))
        # Basic catch-all

else:
    print("Please enter a Python file")
