# animation::start:1
# #Optimized Fibonacci
# This one is pretty easy to implement and very, very fast to compute, in Python
# See <img src="https://i.stack.imgur.com/SPYOU.gif/>

from math import sqrt

def fib(n):
# end::animation

# animation::start:2
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))
# end::animation


