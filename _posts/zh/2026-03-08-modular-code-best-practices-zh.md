---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模块化代码最佳实践
translated: true
type: note
---

**问题：** 如何编写模块化代码？规则包括使用更多函数、分离常量/变量、更好的分类，以及将相关事物放在一起。

**答案：**

## 什么是模块化代码？

模块化编程不仅仅是编写干净的代码、自包含的类或更小的函数——它是将你的软件视为一组可互换模块的集合，每个模块都有明确定义的目的。你不是构建一个庞大的应用程序，而是将其分解成更小、更易管理的部分。

---

## 核心原则

### 1. Single Responsibility — 一个函数，一个职责

你编写的每个函数都应该专注于做一件事。如果一个函数在做多件事，它就更难泛化和重用。通常，如果你的函数名中有“and”（和），考虑重构。

**不良示例：**

```python
def process_and_save_and_notify(data):
    # 做了3件事——难以重用
    cleaned = data.strip()
    db.save(cleaned)
    email.send("Done!")
```

**良好示例：**

```python
def clean_data(data):
    return data.strip()

def save_to_db(data):
    db.save(data)

def send_notification(message):
    email.send(message)
```

---

### 2. DRY — Don't Repeat Yourself

模块化允许我们重用代码的部分。将重复的代码泛化并整合到函数或循环中。将代码抽象成函数不仅减少了重复，还通过描述性的函数名提高了可读性。

---

### 3. 分离常量和配置

将所有魔法数字、字符串和配置保存在一个专用位置，这样更改只需在一个地方进行。

```python
# config.py 或 constants.py
MAX_RETRY = 3
API_URL = "https://api.example.com"
TIMEOUT = 30

# main.py
from config import MAX_RETRY, API_URL
```

---

### 4. Separation of Concerns — 将相关事物分组

将代码的不同方面（数据处理、预处理、模型训练等）放在单独的模块中。封装隐藏了实现细节，只暴露必要的功能。

结构良好的项目看起来像这样：

```
project/
├── config/
│   └── settings.py         # constants & config
├── data/
│   ├── loader.py           # loading data
│   └── preprocessor.py     # cleaning data
├── services/
│   └── api_client.py       # API calls
├── utils/
│   └── helpers.py          # shared utilities
└── main.py                 # entry point
```

---

### 5. Layered Architecture

分层架构是一种常见方法，根据功能将代码组织成不同的层：**Presentation layer**（UI 逻辑）、**Business logic layer**（核心规则和流程）和 **Data access layer**（数据库交互）。这种分层方法促进了模块化，使得修改和维护单个层而不干扰整个系统更加简单直接。

---

### 6. 命名约定

命名约定可以帮助你避免混淆、歧义和错误，同时提高可读性和可维护性。你应该在整个代码中使用一致的命名约定，并遵循你所用编程语言的标准。例如，在 Python 中，遵循 PEP 8 风格指南，它定义了模块、变量、函数、类和常量的命名规则。

快速参考：

| 元素 | 约定 (Python) | 示例 |
|---|---|---|
| Variable | snake_case | `user_name` |
| Function | snake_case verb | `get_user()` |
| Constant | UPPER_CASE | `MAX_SIZE` |
| Class | PascalCase | `UserService` |
| Boolean | `is_` / `has_` prefix | `is_valid` |

---

### 7. 限制函数参数

尽可能将每个函数的参数限制在不超过三个。这不是硬性规则，但在许多情况下，使用更少的参数更有效。如果一个函数有很多参数，你可能需要重新思考如何拆分它。

---

### 8. 模块间的松耦合

模块应该作为独立的单元运行，仅通过明确定义的接口连接。这意味着你可以修改一个模块的内部工作方式，而无需更改其他模块，只要接口保持不变。

---

### 9. 避免过度模块化

程序员可能陷入过度模块化的陷阱。原本好的事情会演变成无意义的细分和再细分，没有考虑实际用例。老话“过早优化是一切邪恶的根源”仍然适用——在为模块化重构之前，给你的软件一些时间成形。

---

## 快速检查清单

- 每个函数只做**一件事**
- 常量存放在**专用的配置文件**中
- 相关代码**分组在同一模块/文件夹**中
- 无重复逻辑——使用**共享实用函数**
- 函数有**描述性名称**且**参数 ≤3 个**
- 模块**松耦合**（最小相互依赖）
- 遵循**一致的命名约定**

---

**参考资料：**

- [https://best-practice-and-impact.github.io/qa-of-code-guidance/modular_code.html](https://best-practice-and-impact.github.io/qa-of-code-guidance/modular_code.html)
- [https://vfunction.com/blog/modular-software/](https://vfunction.com/blog/modular-software/)
- [https://dev.to/prxtikk/how-to-write-clean-and-modular-code-1d87](https://dev.to/prxtikk/how-to-write-clean-and-modular-code-1d87)
- [https://blog.pixelfreestudio.com/best-practices-for-modular-code-design/](https://blog.pixelfreestudio.com/best-practices-for-modular-code-design/)
- [https://www.designreview.byu.edu/collections/from-chaos-to-clarity-modular-design-in-programming](https://www.designreview.byu.edu/collections/from-chaos-to-clarity-modular-design-in-programming)
