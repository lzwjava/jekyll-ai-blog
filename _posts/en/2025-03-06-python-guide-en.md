---
audio: false
generated: true
lang: en
layout: post
title: Python Guide
translated: false
type: note
---

Here is a concise Python guide covering string operations, math, text processing, I/O, file handling, networking, collections, and multithreading. Each section includes a brief overview and practical examples to help you get started or refresh your knowledge.

---

## Python Guide: Essential Topics

### 1. String Operations

Strings in Python are immutable sequences of characters. You can perform operations like concatenation, repetition, slicing, and use built-in methods for manipulation.

**Examples:**

```python
# Concatenation and repetition
s1 = "Hello"
s2 = "World"
print(s1 + " " + s2)  # Output: Hello World
print(s1 * 3)         # Output: HelloHelloHello

# Slicing
print(s1[1:4])        # Output: ell

# Built-in methods
print(s1.upper())     # Output: HELLO
print(s2.lower())     # Output: world
print("  hi  ".strip())  # Output: hi
print("a,b,c".split(','))  # Output: ['a', 'b', 'c']
print(','.join(['a', 'b', 'c']))  # Output: a,b,c

# String formatting with f-strings
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")  # Output: My name is Alice and I am 30 years old.
```

---

### 2. Math

The `math` module provides mathematical functions and constants for common calculations.

**Example:**

```python
import math

print(math.sqrt(16))    # Output: 4.0
print(math.pow(2, 3))   # Output: 8.0
print(math.sin(math.pi / 2))  # Output: 1.0
print(math.pi)          # Output: 3.141592653589793
```

---

### 3. Text Processing (Regular Expressions)

The `re` module enables pattern matching and text manipulation using regular expressions.

**Example:**

```python
import re

text = "The rain in Spain"
match = re.search(r"rain", text)
if match:
    print("Found:", match.group())  # Output: Found: rain

# Find all 4-letter words
print(re.findall(r"\b\w{4}\b", text))  # Output: ['rain', 'Spain']
```

---

### 4. I/O (Input and Output)

Basic input and output operations allow interaction with the user.

**Example:**

```python
name = input("Enter your name: ")
print("Hello, " + name + "!")
```

---

### 5. File Handling

Python simplifies reading from and writing to files using the `open()` function, with the `with` statement recommended for automatic file closure.

**Example:**

```python
# Writing to a file
with open("example.txt", "w") as f:
    f.write("Hello, World!\n")

# Reading from a file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)  # Output: Hello, World!
```

---

### 6. Networking

The `requests` library (install with `pip install requests`) makes HTTP requests straightforward.

**Example:**

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)  # Output: 200
print(response.json())       # Output: JSON data from GitHub API
```

---

### 7. Collections

The `collections` module offers specialized data structures like `Counter`, `deque`, `namedtuple`, etc. Here’s an example with `Counter`.

**Example:**

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry"]
word_count = Counter(words)
print(word_count)  # Output: Counter({'apple': 2, 'banana': 1, 'cherry': 1})
```

**Other Collections:**

- `namedtuple`: Creates tuple subclasses with named fields.
- `deque`: Double-ended queue for efficient appends/pops from both ends.
- `OrderedDict`: Dictionary that remembers insertion order.
- `defaultdict`: Dictionary with a default value for missing keys.

---

### 8. Multithreading

The `threading` module enables concurrent task execution, ideal for I/O-bound operations.

**Example:**

```python
import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(1)

# Create and start a thread
t = threading.Thread(target=print_numbers)
t.start()

# Main thread continues
print("Main thread finished")
```

---

This guide provides a starting point for each topic with practical examples. For more in-depth learning, consult the official Python documentation or specialized resources. Happy coding!
