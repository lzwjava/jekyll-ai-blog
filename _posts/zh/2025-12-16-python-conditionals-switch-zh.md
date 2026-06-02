---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Python 条件语句和 Switch
translated: true
type: note
---

问题：如何在 Python 中使用 if、elif 和 else 编写条件代码？Python 有 switch 语句吗？

答案：

Python 使用 `if`、`elif` 和 `else` 语句进行条件执行。与其他许多语言不同，Python **没有传统的 switch 语句**，直到 Python 3.10 引入了**结构化模式匹配**功能（`match` 和 `case`），它可以作为 switch 更强大的替代方案。

### 基本 if-elif-else 语法

```python
x = 10

if x > 20:
    print("x is greater than 20")
elif x > 5:
    print("x is greater than 5 but not greater than 20")
else:
    print("x is 5 or less")
```

- `if` 检查第一个条件。
- `elif`（“else if”的缩写）在前面的条件为假时检查附加条件。
- `else` 在以上条件都不为真时运行。
- 你可以有任意数量的 `elif` 子句，`else` 是可选的。

### 嵌套条件

```python
if x > 0:
    if x % 2 == 0:
        print("Positive even number")
    else:
        print("Positive odd number")
else:
    print("Non-positive number")
```

### 类似 Switch 的行为（Python 3.10+）：match-case

从 Python 3.10 开始，你可以使用 `match` 和 `case` 进行模式匹配，这通常用作 switch 的替代品：

```python
def http_status(status):
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _ :  # wildcard (default case)
            return "Unknown status"

print(http_status(200))  # Output: OK
```

`match` 语句比传统的 `switch` 更强大，因为它支持列表、字典、守卫等模式。

### 较旧的替代方法（Python 3.10 之前）

模拟 Switch 的常见方法：

- 使用字典：

```python
def handle_command(cmd):
    return {
        'start': lambda: print("Starting..."),
        'stop':  lambda: print("Stopping..."),
        'pause': lambda: print("Pausing...")
    }.get(cmd, lambda: print("Unknown command"))()

handle_command('start')
```

- 使用 if-elif 链（对于简单情况最常见和可读）。

在大多数情况下，除非你有许多情况或需要高级模式匹配，否则首选 `if-elif-else` 以保持清晰。
