# With yield

def F():
    a,b = 0,1
    while True:
        yield a
        a, b = b, a + b
