a = [1, 2, 3]
a.append(4)
print(a)

d = {}
d.add("x", 10)
print(d.get("x"))
d.remove("x")
print(len(d))

s = set([1, 2, 2, 3])
print(len(s))
s.add(4)
print(s.get(2))
s.remove(1)
print(len(s))
