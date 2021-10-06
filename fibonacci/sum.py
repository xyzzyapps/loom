# animation::start:3
# In programming, infinite doesn't exist. You can use a recursive form translating the math form directly in your language, for example in Python it becomes:

def basic(n):
# end::animation

# animation::start:4
    if n == 0: return 0
    elif n == 1: return 1
    else: return F(n-1)+F(n-2)
# end::animation



