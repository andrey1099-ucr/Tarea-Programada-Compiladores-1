def fibonacci(n):
    if n <= 1:
        return n
    
    return fibonacci(n - 1) + fibonacci(n - 2)

times = []
for i in range(1, 51):
    print(fibonacci(i))
