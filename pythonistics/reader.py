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

group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--short",
                   action="store_true",
                   help="Temporary SHORT help string")
group.add_argument("-l", "--long",
                   action="store_true",
                   help="Temporary LONG help string")

args = parser.parse_args()
string_name = str(args.file_name.name)
file_extension = os.path.splitext(string_name)[1]

print()

if file_extension == ".py":
    if args.short:
        print("{} is the SHORT version\n".format(string_name))
    elif args.long:
        print("{} is the LONG version\n".format(string_name))
    else:
        print("{} is the PLAIN version\n".format(string_name))

    file_contents = args.file_name.read()
    def_func = str(file_contents.count("def"))
    class_func = str(file_contents.count("class"))

    print("Occurrences of 'def': {}".format(def_func))
    print("Occurrences of 'class': {}".format(class_func))
    print("Occurrences of built in functions:")

    for func in dir(builtins):
        if file_contents.count(func) > 0:
            count_num = str(file_contents.count(func))
            print(" - {} is in the script {} "
                  "times".format(func, count_num))

    print()

    with tokenize._builtin_open(args.file_name.name, "rb") as t_file:
        tokens = list(tokenize.tokenize(t_file.readline))

    for token in tokens:
        token_type = token.type
        if args.exact:
            token_type = token.exact_type
        token_range = "{}-{}".format(token.start, token.end)
        print("{: <20}{: <15}{: <15}".format(token_range,
                                      tokenize.tok_name[token_type],
                                      token.string))

    print()

else:
    print("Please enter a Python file")

print()
