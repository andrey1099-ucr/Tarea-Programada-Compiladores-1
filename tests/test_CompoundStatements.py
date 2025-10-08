# --- Top-level simple statements ---
flag = True
done = False
x = 1; y = 2; z += 3
msg = "Hello\nWorld"
print(x, y, 42, msg)

# --- Class with attribute and a method using if/elif/else, while, for, calls ---
class Foo:
    # empty line below (should parse as empty stmt)

    
    pass
    value = 1

    def method(self, n, m):
        # if / elif / else with a comparison and a pure logical expr
        if n < 0:
            return
        elif True and self:   # logical expression (no comparisons here)
            pass
        else:
            while m > 0:      # comparison condition
                m -= 1
                continue

        # for with a function call as iterable (range is an ID)
        for i in range(3):
            print(i); break   # semicolon separates two simple statements

        return self

# --- Function with params and a small body (assignments + return) ---
def add(a, b):
    result = a
    result += b
    return result

# Nested call in assignment (grouped)
nested = (add(1, 2))

# --- if / elif / else at top level ---
if flag:               # pure expression condition (ID)
    foo()
elif func(1, 2) and True:
    bar()
else:
    pass

# --- for at top level using range ---
for k in range(5, 20, 5):
    print(k)

# --- while at top level with NOT ---
while not done:
    done = True

# Final simple statement without trailing NEWLINE (EOF tolerance)
end_val = add(x, y)
