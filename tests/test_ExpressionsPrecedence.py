# Expression workout: arithmetic precedence, comparisons, logical ops, calls

# --- Arithmetic precedence ---
a = 2 + 3 * 4          # + lower than *
b = 2 * 3 + 4          # * higher than +
c = 2 ** 3 ** 2        # ** is right-associative
d = -2 ** 3            # unary minus binds looser than **
e = (-2) ** 3          # grouping changes the base
f = 2 + -3 * +4        # unary +/- inside
g = (1 + 2) * 3        # grouping before *
h = 10 // 3 % 2        # left-assoc among // and %
i = 8 / 4 / 2          # left-assoc among /
j = 2 ** 3 * 4         # ** higher than *

# --- Binary comparisons (no chaining) ---
c1 = 2 + 3 * 4 == 14
c2 = 2 ** 3 > 7
c3 = -2 < 0
c4 = (1 + 2) >= 3
c5 = 10 // 3 != 3

# --- Logical ops with precedence: not > and > or ---
l1 = not 2 + 2 == 5
l2 = a < b and c >= d
l3 = x == y or not z
l4 = (1 + 2 < 4) and not (2 * 2 != 4) or True

# --- Use expressions inside control-flow ---
if a + 1 < b * 2 and not done:
    pass
elif foo(1) and True:
    bar()
else:
    baz()

while not done or a == b:
    a += 1
    if a >= 10:
        break

# --- for with call (range is an ID now) and semicolon-separated simple stmts ---
for i in range(1, 10, 2):
    print(i); continue

# --- Function using arithmetic/precedence and return ---
def powsum(x, y, z):
    return x ** y + -z * 2

result = powsum(2, 3, 4)
