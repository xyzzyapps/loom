from math import sqrt

# animation::start:1
# Go on on the sites I linked to you and will see this (on wolfram)
# <img src="https://i.stack.imgur.com/SPYOU.gif/>

def F(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)) # This one is pretty easy to implement and very, very fast to compute, in Python
