import argparse


parser = argparse.ArgumentParser(prog="Pythonistics",
                                 description="File processer",
                                 epilog="This is the end")

parser.add_argument("file_name",
                    type=str,
                    help="Temporary FILE help string")

group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--short",
                   action="store_true",
                   help="Temporary SHORT help string")
group.add_argument("-l", "--long",
                   action="store_true",
                   help="Temporary LONG help string")

args = parser.parse_args()

print()

if args.short:
    print(str(args.file_name) + " is the SHORT version")
elif args.long:
    print(str(args.file_name) + " is the LONG version")
else:
    print(str(args.file_name) + " is the PLAIN version")

with open(args.file_name, 'r') as fn:
    print()
    print(fn.name)
    print()
    print(fn.read())

# https://docs.python.org/3/library/io.html
