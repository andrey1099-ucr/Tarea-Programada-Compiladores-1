x = 0
y= 0
z = 0
done = False

def foo(a):
    return a > 0

def bar():
    x += 1

def baz():
    y += 2

def add(a, b):
    return a + b

def lookup(d, k):
    return d


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

l5 = a < b  and b < c

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

# Lists, Tuples, Dicts (and calls, grouping)

# --- Lists (with/without trailing comma) ---
xs = []
ys = [1]
zs = [1, 2, 3]
mix = [a, 2, foo(3)]
trail = [1, 2,]        # trailing comma allowed
nested_list = [[1], [2, 3]]

# --- Tuples (must contain a comma to be a tuple) ---
t1 = (a,)             # singleton tuple
t2 = (a, b, c)
t3 = (1 + 2, 3 * 4,)
group = (x)           # grouping, NOT a tuple

# --- Dicts (with/without trailing comma) ---
empty_d = {}
simple_d = {"k": 1}
expr_d = {"a": 1, b: 2 + 3, foo(1): bar(2)}
trail_d = {"x": 1,}   # trailing comma allowed
nested_d = {"inner": {"n": 1}, "lst": [1, 2]}

# --- Use in statements and calls ---
print(xs, ys, zs, mix, nested_list)
use_tuple = add(t1, t2)
use_dict = lookup(expr_d, "a")

# --- In control flow ---
if len(xs) == 0:
    xs = [42]
elif (1,) and {"k": 1}:
    pass
else:
    zs = zs

# --- For with call and list literal ---
for i in range(1, 5):
    print([i, i*i])

# Final line without trailing newline (EOF tolerance)
last = {"p": (1, 2)}

