import argparse
import os
import builtins
import tokenize


parser = argparse.ArgumentParser(description="File processer",
                                 epilog="This is the end")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="Temporary %(prog)s POSITIONAL help string")
parser.add_argument("-e", "--exact",
                    action="store_true",
                    help="Temporary EXACT help string")

# Command line operations for what the program should output
process = parser.add_mutually_exclusive_group()
process.add_argument("--stats",
                     action="store_true",
                     help="Temporary STATS help string")
process.add_argument("--short",
                     action="store_true",
                     help="Temporary SHORT help string")
process.add_argument("--nicer",
                     action="store_true",
                     help="Temporary NICER help string")

# Command line operations for where the results should display
output = parser.add_mutually_exclusive_group()
output.add_argument("--toprint",
                    action="store_true",
                    help="Temporary SHORT help string")
output.add_argument("--tofile",
                    action="store_true",
                    help="Temporary LONG help string")

args = parser.parse_args()
string_name = str(args.file_name.name)
file_extension = os.path.splitext(string_name)[1]

print()

if file_extension == ".py":
    if args.toprint:
        print("{} is the PRINT version\n".format(string_name))
    elif args.tofile:
        print("{} is the FILE version\n".format(string_name))
    else:
        print("{} is the OTHER version\n".format(string_name))

    file_contents = args.file_name.read()
    def_func = str(file_contents.count("def"))
    class_func = str(file_contents.count("class"))

    print()

    with tokenize._builtin_open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))

    for token in tokens:
        token_type = token.type
        if args.exact:
            token_type = token.exact_type
        token_name = tokenize.tok_name[token_type]
        token_range = "{}-{}".format(token.start, token.end)
        print("{: <20}{: <15}{: <15}".format(token_range,
                                             str(token_name),
                                             str(token.string)))

    print()

else:
    print("Please enter a Python file")

print()
