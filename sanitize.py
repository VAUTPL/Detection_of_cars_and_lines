#library to sanitize data converting all the doubles in tuple to integers
__author__ = 'utpl'

def double_tuple_2_int(t):
    l = []
    print t
    for d in t:
        l.append(int(d))
    return tuple(l)
