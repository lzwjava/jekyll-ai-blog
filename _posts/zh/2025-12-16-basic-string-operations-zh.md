---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Python 字符串基本操作
translated: true
type: note
---

问题：Python 中字符串的基本操作有哪些？

答案：

Python 中的字符串是不可变的字符序列。它们支持各种内置操作和方法进行操作。

### 常见的字符串基本操作

- **长度**: 使用 `len(s)` 获取字符数量。
- **索引**: 使用 `s[index]` 访问单个字符（从 0 开始；负数索引从末尾计数）。
- **切片**: 使用 `s[start:end:step]` 提取子字符串（不包含 end）。
- **拼接**: 使用 `+` 连接字符串。
- **重复**: 使用 `*` 重复字符串。
- **成员**: 使用 `in` 或 `not in` 检查子字符串是否存在。

### 常用字符串方法

- `upper()` / `lower()`: 改变大小写。
- `strip()`: 移除开头/结尾的空白字符（或指定字符）。
- `replace(old, new)`: 替换子字符串。
- `split(sep)`: 分割成子字符串列表。
- `join(iterable)`: 将字符串列表连接成一个（在分隔符上调用）。
- `find(sub)` / `index(sub)`: 查找子字符串的位置（`find` 如果未找到则返回 -1；`index` 则抛出错误）。
- `startswith(prefix)` / `endswith(suffix)`: 检查前缀/后缀。
- 格式化字符串 (f-strings): 使用 `f"... {expr} ..."` 嵌入表达式。

### 示例

```python
s = "Hello, World!"

# 长度
len(s)                    # 13

# 索引和切片
s[0]                      # 'H'
s[-1]                     # '!'
s[0:5]                    # 'Hello'
s[7:]                     # 'World!'
s[:-7]                    # 'Hello,'

# 大小写转换
s.upper()                 # 'HELLO, WORLD!'
s.lower()                 # 'hello, world!'

# 替换
s.replace("World", "Python")  # 'Hello, Python!'

# 分割和连接
s.split(",")              # ['Hello', ' World!']
" ".join(["Hello", "Grok"])  # 'Hello Grok'

# 移除空白字符
"  spaced  ".strip()      # 'spaced'

# 查找
s.find("World")           # 7
s.find("xyz")             # -1

# 以...开头/结尾
s.startswith("Hello")     # True
s.endswith("!")           # True

# 拼接和重复
s + " Again."             # 'Hello, World! Again.'
"Hi" * 3                  # 'HiHiHi'

# f-string
name = "Alice"
age = 30
f"{name} is {age} years old."  # 'Alice is 30 years old.'
```

这些操作不会修改原始字符串（因为字符串是不可变的）；它们会返回新的字符串。
