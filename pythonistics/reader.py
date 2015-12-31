import argparse
import os
import builtins


parser = argparse.ArgumentParser(description="File processer",
                                 epilog="This is the end")

parser.add_argument("file_name",
                    type=argparse.FileType(),
                    help="Temporary %(prog)s POSITIONAL help string")

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
        print(string_name + " is the SHORT version")
    elif args.long:
        print(string_name + " is the LONG version")
    else:
        print(string_name + " is the PLAIN version")

    file_contents = args.file_name.read()

    print()

    print("Occurrences of 'def': "
          + str(file_contents.count('def')))
    print("Occurrences of 'class': "
          + str(file_contents.count('class')))
    print("Occurrences of built in functions:")

    for func in dir(builtins):
        if file_contents.count(func) > 0:
            print(" - " + func + " is in the script "
                  + str(file_contents.count(func)) + " times")

else:
    print("Please enter a Python file")

print()
