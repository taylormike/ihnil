import argparse


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
name = str(args.file_name.name)

print()

if args.short:
    print(name + " is the SHORT version")
elif args.long:
    print(name + " is the LONG version")
else:
    print(name + " is the PLAIN version")

file_contents = args.file_name.read()

bi_funcs = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray',
            'bytes', 'callable', 'chr', 'classmethod', 'compile',
            'complex', 'delattr', 'dict', 'dir', 'divmod',
            'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
            'help', 'hex', 'id', 'input', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'len', 'list', 'locals',
            'map', 'max', 'memoryview', 'min', 'next', 'object',
            'oct', 'open', 'ord', 'pow', 'print', 'property',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
            'tuple', 'type', 'vars', 'zip', '__import__']

print()

print("Occurrences of 'def': " + str(file_contents.count('def')))
print("Occurrences of 'class': " + str(file_contents.count('class')))
print("Occurrences of built in functions:")

for func in bi_funcs:
    if file_contents.count(func) > 0:
        print(" - " + func + " is in the script "
              + str(file_contents.count(func)) + " times")

print()
