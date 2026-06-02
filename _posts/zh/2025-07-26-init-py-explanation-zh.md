---
audio: false
generated: true
lang: zh
layout: post
title: Python为何需要`__init__.py`文件
translated: true
type: note
---

### 修正拼写错误
看起来您指的是 `__init__.py`（"init" 是 "initialization" 的缩写），而不是 `__int__.py`。如果不是这个情况，请随时说明！假设确实是 `__init__.py`，以下是相关解释。

### 为什么 Python 需要在目录中包含 `__init__.py`
在 Python 中，一个目录不会仅仅因为包含 Python 文件就被自动视为模块或包。为了将代码组织成可重用的包（本质上是相关模块的目录），Python 要求在该目录中包含一个 `__init__.py` 文件。原因如下：

- **将目录标记为包**：`__init__.py` 的存在告诉 Python 该目录应被视为一个包。这样您就可以使用点符号从该包中导入模块，例如 `import mypackage.mymodule`。如果没有该文件（在标准情况下），Python 会将目录视为普通文件夹，不允许从中导入模块。

- **防止名称冲突**：它可以避免模块的意外遮蔽。例如，如果您有一个名为 `string` 的目录（这是一个常见名称），在没有 `__init__.py` 的情况下，它可能会无意中隐藏 Python 内置的 `string` 模块。

- **初始化和自定义**：该文件可以是空的（对于简单的包来说很常见），但也可以包含在包被导入时运行的代码。这对于执行初始化任务（例如自动导入子模块）非常有用。此外，您可以在 `__init__.py` 中定义一个名为 `__all__` 的特殊变量，以控制当有人执行 `from mypackage import *` 时导入哪些内容（例如 `__all__ = ['module1', 'module2']`）。

### 历史背景和版本特定说明
- 这一要求自 Python 早期版本以来就存在，目的是保持模块系统的明确性和组织性。
- 从 Python 3.3 开始，引入了“命名空间包”，这种包不需要 `__init__.py`。它们允许包分布在多个目录中（例如用于分发目的），而无需该文件，可以使用 `pkgutil` 或 `importlib` 等工具实现。然而，这被视为高级功能，对于大多数日常使用场景，`__init__.py` 仍然是常规包的推荐且广泛使用的方式。

如果您使用的是 Python 3.3 或更高版本，可以尝试命名空间包，但对于初学者来说，使用 `__init__.py` 更简单直接。

[Python 教程：模块](https://docs.python.org/3/tutorial/modules.html#packages)
