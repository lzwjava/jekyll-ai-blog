---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: google/gemini-2.5-flash
title: Python代码示例入门
translated: true
type: note
---

好的，“一些Python代码”可以涵盖很多内容！Python的用途极其广泛。我将为你提供几个常见示例，从非常基础到稍复杂一些，涵盖不同的概念。

---

### 1. Hello World（经典入门）

这是最简单的Python程序。

```python
# 这是一个注释。Python会忽略注释。
print("Hello, World!")
```

**解释：**
*   `print()` 是一个内置函数，将给定的参数输出到控制台。
*   `"Hello, World!"` 是一个字符串（文本）。

---

### 2. 变量、基础算术和用户输入

这段代码演示了如何将数据存储在变量中、执行简单的数学运算以及获取用户输入。

```python
# 用于存储数据的变量
name = input("What is your name? ") # 获取用户输入
age_str = input("How old are you? ")

# 将年龄从字符串转换为整数以进行计算
age = int(age_str)

# 基础算术
year_of_birth = 2023 - age # 为简化起见，假设当前年份是2023
# 你也可以使用：import datetime; year_of_birth = datetime.date.today().year - age

# 使用 f-string（格式化字符串字面值）打印格式化的输出
print(f"Hello, {name}! You are {age} years old.")
print(f"You were likely born in {year_of_birth}.")

# 一个简单的条件检查
if age < 18:
    print("You are a minor.")
else:
    print("You are an adult.")
```

**解释：**
*   `input()`: 提示用户输入文本，并将其作为字符串返回。
*   `name`, `age_str`, `age`, `year_of_birth`: 这些是存储不同类型数据（字符串、整数）的变量。
*   `int()`: 将字符串转换为整数。这是必要的，因为 `input()` 总是返回字符串，不能直接用字符串进行数学运算。
*   `f-strings`: 一种在字符串字面值中嵌入表达式的便捷方法。注意开头的引号前的 `f`。
*   `if/else`: 控制流语句，根据条件执行不同的代码块。

---

### 3. 列表和循环

列表是有序的项目集合。循环用于重复执行一段代码多次。

```python
# 一个水果列表
fruits = ["apple", "banana", "cherry", "date"]

print("\nMy favorite fruits:")

# 使用 'for' 循环遍历列表
for fruit in fruits:
    print(f"- {fruit.capitalize()}") # .capitalize() 使首字母大写

# 通过索引访问元素（列表是零索引的）
print(f"\nThe first fruit is: {fruits[0]}")
print(f"The last fruit is: {fruits[-1]}") # 负索引从末尾开始访问

# 添加一个元素
fruits.append("elderberry")
print(f"Updated list: {fruits}")

# 移除一个元素
fruits.remove("banana")
print(f"List after removing banana: {fruits}")

# 使用 'range' 循环获取索引
print("\nFruits with their indices:")
for i in range(len(fruits)): # len() 给出列表中的项目数量
    print(f"Index {i}: {fruits[i]}")
```

**解释：**
*   `[]`: 用于定义列表。
*   `for ... in ...`: 一个 `for` 循环，遍历序列（如列表）中的每个项目。
*   `fruit.capitalize()`: 一个字符串方法，返回字符串的副本，并将其首字母大写。
*   `fruits[0]`: 访问第一个元素（索引 0）。
*   `fruits[-1]`: 访问最后一个元素。
*   `list.append()`: 向列表末尾添加一个项目。
*   `list.remove()`: 移除指定项目的第一个出现项。
*   `range(len(fruits))`: 生成一个从 0 到（但不包括）列表长度的数字序列，用于通过索引访问元素。

---

### 4. 函数

函数是执行特定任务的可重用代码块。

```python
# 定义一个接受参数的函数
def greet_person(name, age):
    """
    This function greets a person and tells them their age.
    It's a good practice to include a docstring like this.
    """
    return f"Hello, {name}! You are {age} years old."

# 调用函数
message1 = greet_person("Alice", 30)
print(message1)

# 使用不同的参数再次调用它
message2 = greet_person("Bob", 25)
print(message2)

# 定义一个带有默认参数的函数
def calculate_area(length, width=10):
    """Calculates the area of a rectangle."""
    return length * width

print(f"\nArea of a 5x10 rectangle: {calculate_area(5)}") # 使用默认宽度
print(f"Area of a 5x7 rectangle: {calculate_area(5, 7)}") # 覆盖默认宽度
```

**解释：**
*   `def`: 用于定义函数的关键字。
*   `greet_person(name, age)`: 函数名及其参数（输入）。
*   `return`: 从函数返回一个值。
*   文档字符串（`"""文档字符串写在这里"""`）: 解释函数的功能。对文档编写很有好处。
*   `calculate_area(length, width=10)`: 展示了一个默认参数。如果在调用函数时未提供 `width`，则默认为 10。

---

### 5. 字典

字典以键值对的形式存储数据。它们是无序的（在较旧的 Python 版本中，Python 3.7+ 中是有序的）。

```python
# 一个表示人物的字典
person = {
    "first_name": "Charlie",
    "last_name": "Smith",
    "age": 40,
    "city": "London",
    "occupations": ["Engineer", "Teacher"] # 列表可以作为值
}

print("\nPerson's details:")

# 通过键访问值
print(f"Name: {person['first_name']} {person['last_name']}")
print(f"Lives in: {person.get('city', 'Unknown')}") # .get() 更安全，如果键未找到则返回 None/默认值
print(f"First occupation: {person['occupations'][0]}")

# 修改一个值
person["age"] = 41
print(f"New age: {person['age']}")

# 添加一个新的键值对
person["email"] = "charlie.smith@example.com"
print(f"Email: {person['email']}")

# 遍历字典
print("\nAll keys:")
for key in person: # 默认遍历键
    print(key)

print("\nAll values:")
for value in person.values():
    print(value)

print("\nAll key-value pairs:")
for key, value in person.items():
    print(f"{key}: {value}")
```

**解释：**
*   `{}`: 用于定义字典。
*   `"key": value`: 键值对。键必须是唯一且不可变的（如字符串或数字）。值可以是任何数据类型。
*   `person['key']`: 访问与 `key` 关联的值。
*   `person.get('key', 'default_value')`: 一种更安全的访问方式，如果键不存在，可以避免 `KeyError`，而是返回 `default_value`。
*   `dict.values()`: 返回一个视图对象，该对象显示字典中所有值的列表。
*   `dict.items()`: 返回一个视图对象，该对象显示字典的键值对元组列表。

---

这只是浅尝辄止，但这些示例涵盖了你将经常使用的许多基本 Python 概念！
