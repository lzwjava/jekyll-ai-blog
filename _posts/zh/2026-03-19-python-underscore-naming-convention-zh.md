---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python 下划线命名规范详解
translated: true
type: note
---

**问题：** 在 Python 中，使用 `_func`（单个前导下划线）来表示函数不被导出，类似于 Java 中的 `private`/`protected`，这是好习惯吗？

**回答：**

是的，这绝对是 Python 中一个良好且广泛接受的实践。然而，机制和强制执行与 Java 显著不同。以下是全面分解：

---

## 约定：单个前导下划线 `_func`

下划线前缀旨在提示其他程序员，以单个下划线开头的变量或方法 предназначен для内部使用。此约定在 PEP 8 中定义，但 **Python 并不强制执行它**。

Python 不强制执行公共或私有名称的访问限制。它依赖命名约定，其中公共名称没有下划线，非公共名称以单个下划线开头。

---

## 与 Java `private`/`protected` 的比较

| 特性 | Java `private` | Java `protected` | Python `_func` |
|---|---|---|---|
| 由语言强制执行？ | ✅ 是 | ✅ 是 | ❌ 否 |
| 外部可访问？ | ❌ 否 | 仅子类 | ✅ 仍然可访问 |
| 基于约定？ | 否 | 否 | ✅ 是 |
| 从通配符导入中排除？ | N/A | N/A | ✅ 是 |

所以在 Python 中，`_func` 是一种 **君子协定**，而不是硬性规则。

---

## 实际效果：通配符导入排除

`_func` 的一个 **具体且强制执行的** 行为是它对导入的影响：

Python 不会导入以单个下划线开头的名称，如果您使用 `from module import *` 从模块导入所有方法和名称。

示例：

```python
# mymodule.py
def public_func():
    return "I am public"

def _private_func():
    return "I am internal"
```

```python
from mymodule import *
public_func()    # Works fine
_private_func()  # NameError: not imported!
```

这使得 `_func` 直接类似于“not exported”——这正是您所描述的。

---

## Python 中的完整下划线系统

Python 识别以下使用前导或尾随下划线的特殊形式：

- `_single_leading_underscore`: 弱“内部使用”指示器
- `single_trailing_underscore_`: 用于避免与 Python 关键字冲突
- `__double_leading_underscore`: 当命名类属性时，触发名称重整
- `__double_leading_and_trailing_underscore__`: “magic” 对象或属性

### 单个下划线 `_func` — “Protected / Internal”

如果您想表示属性或方法仅供类及其子类内部使用，而非外部使用，请为其添加单个下划线前缀 (`_`)。这向其他开发者发出信号，表示该属性或方法是“protected”，不应直接访问。

### 双下划线 `__func` — “带名称重整的 Private”

如果您想使类外的属性或方法不易访问，以避免意外修改或使用，请添加双下划线前缀 (`__`)。这会触发名称重整，使从类外部访问该属性或方法变得更难（但并非不可能）。

例如，在 `class Foo` 中的 `__method` 内部变为 `_Foo__method` ——如果知道重整后的名称，仍然可以访问，但它防止了子类中的意外冲突。

---

## PEP 8 官方推荐

即使正确设置了 `__all__`，内部接口（包、模块、类、函数、属性或其他名称） **仍应添加单个前导下划线**。

---

## 总结与最佳实践

- ✅ **使用 `_func`** 用于您认为内部的模块级或类级函数/方法——这是标准的 Pythonic 约定，并由 PEP 8 推荐。
- ✅ 它有效地充当“not exported”，因为 `from module import *` 会跳过它。
- ⚠️ 它 **不** 防止直接访问——外部代码如果想的话仍然可以调用 `module._func()`。
- ✅ **仅在需要名称重整以防止子类属性冲突时（并非主要为了隐私），在类中使用 `__func`**。
- 🐍 Python 的哲学是 **“我们都是自愿的成年人”** ——社区相信开发者会尊重下划线信号，而无需语言强制执行。

---

**参考资料：**

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Single and Double Underscores in Python – Real Python](https://realpython.com/python-double-underscore/)
- [The Meaning of Underscores in Python – dbader.org](https://dbader.org/blog/meaning-of-underscores-in-python)
- [Python Private Methods Explained – DataCamp](https://www.datacamp.com/tutorial/python-private-methods-explained)
