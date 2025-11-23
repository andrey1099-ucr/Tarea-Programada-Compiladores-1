# Simple container methods test for the Fangless Python transpiler

# ---- List methods ----
lst = [1, 2, 3]
print(lst)

lst.append(4)
print(lst)

sub = lst.sublist(1, 3)
print(sub)

lst.remove(0)
print(lst)

# ---- Dict methods ----
d = {"x": 10}
d.add("y", 20)

print(d.get("x"))
print(d.get("y"))

d.remove("x")
print(d)

# ---- Set methods ----
s = set([1, 2, 3])
s.add(2)
s.add(4)

print(s.get(2))  # should be True
print(s.get(5))  # should be False

s.remove(2)
print(s)
