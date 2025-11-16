def hola(a, b):
    return a + b

print(hola(1, 2))

a = 4
print(a)
b = 5
a = "hola"
b = a + str(b)
print(b)

def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

print(fib(5))
