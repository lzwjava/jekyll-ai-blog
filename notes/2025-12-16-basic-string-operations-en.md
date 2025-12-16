---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Basic Python String Operations
translated: false
type: note
---

Question: What are the basic operations on strings in Python?

Answer: 

Strings in Python are immutable sequences of characters. They support a variety of built-in operations and methods for manipulation.

### Common Basic Operations

- **Length**: Use `len(s)` to get the number of characters.
- **Indexing**: Access individual characters with `s[index]` (0-based; negative indices count from the end).
- **Slicing**: Extract substrings with `s[start:end:step]` (end exclusive).
- **Concatenation**: Join strings using `+`.
- **Repetition**: Repeat a string using `*`.
- **Membership**: Check if a substring exists with `in` or `not in`.

### Common String Methods

- `upper()` / `lower()`: Change case.
- `strip()`: Remove leading/trailing whitespace (or specified characters).
- `replace(old, new)`: Replace substrings.
- `split(sep)`: Split into a list of substrings.
- `join(iterable)`: Join a list of strings into one (called on the separator).
- `find(sub)` / `index(sub)`: Find position of substring (`find` returns -1 if not found; `index` raises error).
- `startswith(prefix)` / `endswith(suffix)`: Check prefixes/suffixes.
- Formatted strings (f-strings): Embed expressions with `f"... {expr} ..."`.

### Examples

```python
s = "Hello, World!"

# Length
len(s)                    # 13

# Indexing and slicing
s[0]                      # 'H'
s[-1]                     # '!'
s[0:5]                    # 'Hello'
s[7:]                     # 'World!'
s[:-7]                    # 'Hello,'

# Case conversion
s.upper()                 # 'HELLO, WORLD!'
s.lower()                 # 'hello, world!'

# Replace
s.replace("World", "Python")  # 'Hello, Python!'

# Split and join
s.split(",")              # ['Hello', ' World!']
" ".join(["Hello", "Grok"])  # 'Hello Grok'

# Strip
"  spaced  ".strip()      # 'spaced'

# Find
s.find("World")           # 7
s.find("xyz")             # -1

# Starts/ends with
s.startswith("Hello")     # True
s.endswith("!")           # True

# Concatenation and repetition
s + " Again."             # 'Hello, World! Again.'
"Hi" * 3                  # 'HiHiHi'

# f-string
name = "Alice"
age = 30
f"{name} is {age} years old."  # 'Alice is 30 years old.'
```

These operations do not modify the original string (since strings are immutable); they return new strings instead.