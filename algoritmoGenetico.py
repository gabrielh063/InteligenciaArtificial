import math

def f(x,y):
    return abs(x*y*math.sin(y*math.pi/4))

def g(x,y):
    return 1 + f(x,y)

g(4,3)