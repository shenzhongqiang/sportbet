import numpy as np
from numpy.linalg import inv, solve

def find_best_bet(a, b, c):
    x = b*c
    y = a*c
    z = a*b
    x = x/(x+y+z)
    y = y/(x+y+z)
    z = z/(x+y+z)
    profit = 1/(1/a+1/b+1/c) - 1
    return (x, y, z, profit)

if __name__ == "__main__":
    a = 1.25
    b = 7
    c = 23
    result = find_best_bet(a, b, c)
    print(result)
