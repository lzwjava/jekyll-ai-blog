---
audio: false
generated: true
lang: en
layout: post
title: Python OOP Guide
translated: false
type: note
---

Here's a comprehensive guide to Object-Oriented Programming (OOP) in Python. This guide covers the fundamental concepts—classes, objects, inheritance, polymorphism, encapsulation, and abstraction—along with practical examples to illustrate each one.

---

### 1. Classes and Objects
A **class** is a blueprint for creating objects, defining their attributes (data) and methods (functions). An **object** is an instance of a class, with its own specific values for the attributes.

**Example:**
```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says woof!")

# Creating an object
my_dog = Dog("Buddy", "Golden Retriever")
my_dog.bark()  # Output: Buddy says woof!
```

---

### 2. Inheritance
**Inheritance** allows a class (child class) to inherit attributes and methods from another class (parent class), promoting code reuse.

**Example:**
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())  # Output: Buddy says woof!
print(cat.speak())  # Output: Whiskers says meow!
```

---

### 3. Polymorphism
**Polymorphism** enables objects of different classes to be treated as instances of a common superclass, allowing methods to be used interchangeably.

**Example:**
```python
def animal_sound(animal):
    print(animal.speak())

dog = Dog("Buddy")
cat = Cat("Whiskers")

animal_sound(dog)  # Output: Buddy says woof!
animal_sound(cat)  # Output: Whiskers says meow!
```

---

### 4. Encapsulation
**Encapsulation** restricts direct access to some object components, promoting data hiding. In Python, private attributes are typically prefixed with `_` (convention) or `__` (name mangling).

**Example:**
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())  # Output: 1300
```

---

### 5. Abstraction
**Abstraction** hides complex implementation details and exposes only essential features. In Python, abstract base classes (ABCs) from the `abc` module enforce abstraction.

**Example:**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

rect = Rectangle(5, 3)
print(rect.area())  # Output: 15
```

---

### 6. Special Methods (Magic Methods)
Special methods (e.g., `__init__`, `__str__`, `__add__`) define behavior for built-in operations like initialization, string representation, and operator overloading.

**Example:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2
print(p3)  # Output: Point(4, 6)
```

---

### 7. Class and Static Methods
- **Class methods** (`@classmethod`) are bound to the class and can access class-level data.
- **Static methods** (`@staticmethod`) are utility functions that don’t access instance or class data.

**Example:**
```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def multiply(cls, a, b):
        return a * b

print(MathUtils.add(5, 3))       # Output: 8
print(MathUtils.multiply(5, 3))  # Output: 15
```

---

### 8. Properties (Getters and Setters)
**Properties** provide controlled access to attributes using the `@property` decorator, often with getters and setters.

**Example:**
```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

p = Person("Alice")
print(p.name)  # Output: Alice
p.name = "Bob"
print(p.name)  # Output: Bob
```

---

This guide provides a solid foundation for understanding OOP in Python. Each concept is demonstrated with clear, practical examples. For more details, refer to the official Python documentation or explore advanced OOP topics. Happy coding!
