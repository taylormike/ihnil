"""This is the test Python document"""

def multipy(x, y):
    """This is the multipy docstring"""
    print(x * y)

if True:
    print("Only a flesh wound")

def evenpy(num):
    # This is a test comment string
    if num == 0:
        print("Input is zero")
    elif num == 1:
        print("Input is odd")
    elif num % 2 == 0:
        print("Input is even")
    else:
        print("Input is odd")

def manyif(val):
# # -------------------------------------------------------
#     if 3 > val > 0:
#         if val != 2:
# # -------------------------------------------------------
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

def listif(inp, num):
# # -------------------------------------------------------
#     if inp == num % 2:
#         if num != inp + 20 - 10:
#             if inp != num:
#                 if inp in ['1', '2', '3']:
#                     if inp != SPAMELOT:
#                         if 20 > inp > 0 - num:
#                             if num % 2 == 0:
# # -------------------------------------------------------
    if inp + num > 0:                                   # No.1
        if num % 2 == 0:                                # No.2
            if 20 > inp:                                # No.3
                if inp != "SPAMELOT":                   # No.4
                    if inp in [1, 2, 3]:                # No.5
                        if inp != num:                  # No.6
                            if num + 10 != inp + 20:    # No.7
                                if inp == (num % 2):    # No.8
                                    print(inp)

def brutal(val1, val2):
# # -------------------------------------------------------
#     if val1 < val2 != 15 + val1:
#         if 1 < val2 < 10 < val1 < 20:
#             if val1 != 5:
# # -------------------------------------------------------
    if val1 != 5:
        if 1 < val2 < 10 < val1 < 20:
            if val1 < val2 != 15 + val1:
                print("THE HOLY GRAIL")
