---
audio: false
generated: true
lang: zh
layout: post
title: Python面向对象编程指南
translated: true
type: note
---

以下是关于 Python 面向对象编程（OOP）的全面指南。本指南涵盖了核心概念——类、对象、继承、多态、封装和抽象，并通过实际示例逐一阐释。

---

### 1. 类与对象
**类**是创建对象的蓝图，用于定义对象的属性（数据）和方法（函数）。**对象**是类的实例，拥有特定的属性值。

**示例：**
```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} 在汪汪叫！")

# 创建对象
my_dog = Dog("Buddy", "金毛寻回犬")
my_dog.bark()  # 输出：Buddy 在汪汪叫！
```

---

### 2. 继承
**继承**允许类（子类）继承另一个类（父类）的属性和方法，提升代码复用性。

**示例：**
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} 发出汪汪声！"

class Cat(Animal):
    def speak(self):
        return f"{self.name} 发出喵喵声！"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())  # 输出：Buddy 发出汪汪声！
print(cat.speak())  # 输出：Whiskers 发出喵喵声！
```

---

### 3. 多态
**多态**使得不同类的对象可被视为共同超类的实例，实现方法的互换使用。

**示例：**
```python
def animal_sound(animal):
    print(animal.speak())

dog = Dog("Buddy")
cat = Cat("Whiskers")

animal_sound(dog)  # 输出：Buddy 发出汪汪声！
animal_sound(cat)  # 输出：Whiskers 发出喵喵声！
```

---

### 4. 封装
**封装**限制对部分对象组件的直接访问，促进数据隐藏。在 Python 中，私有属性通常以 `_`（约定）或 `__`（名称修饰）作为前缀。

**示例：**
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # 私有属性

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("资金不足")

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
account.deposit(500)
account.withdraw(200)
print(account.get_balance())  # 输出：1300
```

---

### 5. 抽象
**抽象**隐藏复杂的实现细节，仅暴露核心功能。Python 通过 `abc` 模块的抽象基类（ABC）强制实现抽象。

**示例：**
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
print(rect.area())  # 输出：15
```

---

### 6. 特殊方法（魔术方法）
特殊方法（如 `__init__`、`__str__`、`__add__`）为初始化、字符串表示和运算符重载等内置操作定义行为。

**示例：**
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
print(p3)  # 输出：Point(4, 6)
```

---

### 7. 类方法与静态方法
- **类方法**（`@classmethod`）绑定类本身，可访问类级数据
- **静态方法**（`@staticmethod`）是不访问实例或类数据的工具函数

**示例：**
```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def multiply(cls, a, b):
        return a * b

print(MathUtils.add(5, 3))       # 输出：8
print(MathUtils.multiply(5, 3))  # 输出：15
```

---

### 8. 属性（访问器与修改器）
**属性**通过 `@property` 装饰器提供对属性的受控访问，常与访问器和修改器配合使用。

**示例：**
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
            raise ValueError("姓名不能为空")
        self._name = value

p = Person("Alice")
print(p.name)  # 输出：Alice
p.name = "Bob"
print(p.name)  # 输出：Bob
```

---

本指南为理解 Python 面向对象编程奠定了坚实基础，每个概念均配有清晰的实践示例。欲了解更多细节，请参阅官方 Python 文档或探索高阶 OOP 主题。编程愉快！
