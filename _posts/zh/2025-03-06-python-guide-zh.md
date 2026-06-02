---
audio: false
generated: true
lang: zh
layout: post
title: Python指南
translated: true
type: note
---

这是一份简洁的Python指南，涵盖字符串操作、数学运算、文本处理、输入输出、文件处理、网络通信、集合类型和多线程编程。每个章节都包含简要概述和实用示例，帮助您快速入门或复习知识。

---

## Python指南：核心主题

### 1. 字符串操作
Python中的字符串是不可变的字符序列。您可以执行连接、重复、切片等操作，并使用内置方法进行字符串处理。

**示例：**
```python
# 连接与重复
s1 = "Hello"
s2 = "World"
print(s1 + " " + s2)  # 输出：Hello World
print(s1 * 3)         # 输出：HelloHelloHello

# 切片操作
print(s1[1:4])        # 输出：ell

# 内置方法
print(s1.upper())     # 输出：HELLO
print(s2.lower())     # 输出：world
print("  hi  ".strip())  # 输出：hi
print("a,b,c".split(','))  # 输出：['a', 'b', 'c']
print(','.join(['a', 'b', 'c']))  # 输出：a,b,c

# f-strings字符串格式化
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")  # 输出：My name is Alice and I am 30 years old.
```

---

### 2. 数学运算
`math`模块为常见计算提供数学函数和常量。

**示例：**
```python
import math

print(math.sqrt(16))    # 输出：4.0
print(math.pow(2, 3))   # 输出：8.0
print(math.sin(math.pi / 2))  # 输出：1.0
print(math.pi)          # 输出：3.141592653589793
```

---

### 3. 文本处理（正则表达式）
`re`模块支持使用正则表达式进行模式匹配和文本处理。

**示例：**
```python
import re

text = "The rain in Spain"
match = re.search(r"rain", text)
if match:
    print("Found:", match.group())  # 输出：Found: rain

# 查找所有4字母单词
print(re.findall(r"\b\w{4}\b", text))  # 输出：['rain', 'Spain']
```

---

### 4. 输入输出
基础输入输出操作支持与用户交互。

**示例：**
```python
name = input("请输入您的姓名：")
print("Hello, " + name + "!")
```

---

### 5. 文件处理
Python通过`open()`函数简化文件读写操作，推荐使用`with`语句实现自动文件关闭。

**示例：**
```python
# 写入文件
with open("example.txt", "w") as f:
    f.write("Hello, World!\n")

# 读取文件
with open("example.txt", "r") as f:
    content = f.read()
    print(content)  # 输出：Hello, World!
```

---

### 6. 网络通信
`requests`库（通过`pip install requests`安装）可简化HTTP请求操作。

**示例：**
```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)  # 输出：200
print(response.json())       # 输出：GitHub API返回的JSON数据
```

---

### 7. 集合类型
`collections`模块提供专用数据结构，如`Counter`、`deque`、`namedtuple`等。以下是`Counter`的示例。

**示例：**
```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry"]
word_count = Counter(words)
print(word_count)  # 输出：Counter({'apple': 2, 'banana': 1, 'cherry': 1})
```

**其他集合类型：**
- `namedtuple`：创建包含命名字段的元组子类
- `deque`：支持两端高效添加/弹出的双端队列
- `OrderedDict`：记录插入顺序的字典
- `defaultdict`：为缺失键提供默认值的字典

---

### 8. 多线程编程
`threading`模块支持并发任务执行，特别适用于I/O密集型操作。

**示例：**
```python
import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(1)

# 创建并启动线程
t = threading.Thread(target=print_numbers)
t.start()

# 主线程继续执行
print("主线程执行完毕")
```

---

本指南通过实用示例为每个主题提供入门指导。如需深入学习，请查阅官方Python文档或专业资源。编程愉快！
