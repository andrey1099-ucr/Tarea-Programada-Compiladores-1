# tests/test_OOP.py
# Small OOP-style program to test:
# - Class inheritance
# - Default / optional parameters in functions and methods
# - General expression/statement parsing

class Animal:
    def __init__(self, name, age = 0):
        self.name = name
        self.age = age

    def speak(self):
        # Base class: does nothing
        pass


class Dog(Animal):
    def __init__(self, name, age = 0, breed = "mixed"):
        # Call parent constructor
        Animal.__init__(self, name, age)
        self.breed = breed

    def speak(self):
        print("Woof!")


def make_dog(name, breed = "mixed"):
    dog = Dog(name, 0, breed)
    return dog


def add_three(a, b = 2, c = 3):
    return a + b + c


# --- Top-level code (will also appear in the AST) ---

d1 = make_dog("Firulais")
d2 = make_dog("Kaiser", "Doberman")

x = add_three(5)
y = add_three(1, 10, 20)

if x > y:
    print("x is greater")
else:
    print("y is greater")
