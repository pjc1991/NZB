import math
import time

x = 1

print("hello, world!")

def test():
    global x
    x += 1
    print(x)

for t in range(100):
    test()

