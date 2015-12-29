import argparse


parser = argparse.ArgumentParser(description="File processer",
                                 epilog="This is the end")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="Temporary %(prog)s help string")

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
    print(str(args.file_name.name) + " is the SHORT version")
elif args.long:
    print(str(args.file_name.name) + " is the LONG version")
else:
    print(str(args.file_name.name) + " is the PLAIN version")

file_contents = args.file_name.read()

print(file_contents)
print("\nOccurrences of 'JOHN': " + str(file_contents.count('JOHN')))

# https://docs.python.org/3/library/io.html
