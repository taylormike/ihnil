import argparse


parser = argparse.ArgumentParser()
parser.add_argument("file", type=IOBase)

args = parser.parse_args()

print(args.file + " is the result of the test code")
