def fibonacci(n):
    if n <= 1:
        return n
    
    a = 0
    b = 1
    for _ in range(n - 1):
        t = a + b
        a = b
        b = t
    
    return b

for i in range(1, 51):
    print(fibonacci(i))
