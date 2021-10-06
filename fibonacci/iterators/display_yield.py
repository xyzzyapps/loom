# animation::start:5
# In most languages you can do something like:

#def SubFib(startNumber, endNumber):
#    n = 0
#    cur = f(n)
#    while cur <= endNumber:
#        if startNumber <= cur:
#            print cur
#        n += 1
#        cur = f(n)
# end::animation

# animation::start:6

def SubFib(startNumber, endNumber):
    for cur in F():
        if cur > endNumber: return
        if cur >= startNumber:
            yield cur

# end::animation

# animation::start:6

for i in SubFib(10, 200):
    print i

# end::animation

