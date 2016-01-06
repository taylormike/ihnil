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
    if args.stats:
        print("{} is the STATS version\n".format(string_name))
    elif args.short:
        print("{} is the SHORT version\n".format(string_name))
    elif args.nicer:
        print("{} is the NICER version\n".format(string_name))
    else:
        print("{} is the OTHER version\n".format(string_name))

    print()

    with tokenize._builtin_open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))

    for token in tokens:
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
