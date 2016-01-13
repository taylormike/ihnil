"""This is the test Python document"""

def multipy(x, y):
    """This is the multipy docstring"""
    print(x * y)

def evenpy(num):
    if num == 0:
        print("Input is zero")
    if num == 1:
        print("Input is odd")
    if num % 2 == 0:
        print("Input is even")
    else:
        print("Input is odd")

def manyif(val):
    if val == "EGGS":
        if True:
            print("Eggs & spam")

class Basic():
    """This is the Basic docstring"""
    def __init__(self):

    def printr(self, val):
        print("The input value is " + str(val))
