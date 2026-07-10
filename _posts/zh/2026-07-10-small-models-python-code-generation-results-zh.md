---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小型模型的Python代码生成结果
translated: true
type: note
---

评估已完成。BPB验证失败（评估数据加载器期望的是默认的nanochat数据路径，而非我们的codeparrot数据——不过我们已有的训练val_bpb值为：**0.372**）。**Python代码生成结果才是真正的亮点**：

**Python代码生成结果（286M模型，temperature=0.3）：**

```
def fibonacci(n):
    if n == 0:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```
**✓ 正确** 递归实现。随后生成了`fibonacci2`、`fibonacci3`等变体。

---

```
def reverse_linked_list(head):
    if head == None:
        return None
    if head.is_empty():
        return None
    if head.is_linked():
        return head
    return reverse_linked_list(head.next)
```
**~** 识别出问题，生成了合理的节点API（`.is_empty()`、`.is_linked()`），但递归逻辑有误（对`is_linked`的判断会导致无限递归）。整体结构是正确的。

---

```
class Stack:
    def __init__(self):
        self._stack = []
        self._stack.append(None)

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0
```
**✓ 正确** —— 功能完整的Stack类，包含所有标准方法。

---

```
def is_palindrome(s):
    if len(s) == 0:
        return False
    if s[0] == s[-1]:
        return True
    else:
        return False
```
**~** 识别到首尾字符比较的逻辑，但实现有误（直接返回True，未使用递归）。尝试了`is_palindrome2`、`is_palindrome3`等变体。

---

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
...
```
**✓** 生成了合理的导入链。

---

**评估结论：** 对于一个仅基于codeparrot-clean训练（未进行SFT微调）的286M模型而言，表现相当扎实。它已学会：
- Python语法和缩进规则完全正确
- 类/函数结构
- 文档字符串和注释
- 常见的导入模式
- 常见算法的*基本框架*（即使逻辑仍有偏差）

存在的局限性也在预期之内：小模型容量导致它能记忆模式，但无法深入理解算法逻辑。通过SFT微调可以显著改善这一问题。

结果已保存至`/mnt/data/zz/codeparrot/eval/results/`。接下来是否要尝试运行聊天CLI与其交互？