# animation::start:1
# #Optimized Fibonacci
# This one is pretty easy to implement and very, very fast to compute, in Python
# See <img src="https://i.stack.imgur.com/SPYOU.gif/>

from math import sqrt

# animation::start:2

def fib(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

