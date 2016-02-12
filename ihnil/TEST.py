"""This is the test Python document"""

def multipy(x, y):
    """This is the multipy docstring"""
    print(x * y)

def evenpy(num):
    # This is a test comment string
    if num == 0:
        print("Input is zero")
    if num == 1:
        print("Input is odd")
    if num % 2 == 0:
        print("Input is even")
    else:
        print("Input is odd")

def manyif(val):
    if val > 0:
        if val != 2:
            if val < 3:
                print("Eggs & spam")

class Basic():
    """This is the Basic docstring"""
    def __init__(self, val):
        self.val = val
    
    # Here is another comment
    def printr(self):
        print("The input value is " + str(self.val))

def listif(inp):
    if inp % 2 == 0:
        if inp in [1, 2, 3, 4, 5]:
            print(inp)
