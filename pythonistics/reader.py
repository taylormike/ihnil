import argparse
import io


parser = argparse.ArgumentParser()
parser.add_argument("square",
                    type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity",
                    action="count",
                    default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2

if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)


# parser = argparse.ArgumentParser()
# parser.add_argument("file_name",
#                     type=io.IOBase,
#                     help="Temporary file error string")
# parser.add_argument("--short",
#                     help="Temporary short error")
# parser.add_argument("--long",
#                     help="Temporary long error")
# 
# args = parser.parse_args()
# 
# print(args.file_name)
