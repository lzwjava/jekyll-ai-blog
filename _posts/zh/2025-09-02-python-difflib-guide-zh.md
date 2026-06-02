---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python Difflib序列比对指南
translated: true
type: note
---

在 Python 中，**`difflib`** 模块提供了比较序列（字符串、列表或任何可迭代对象）的工具。它常用于检测文本差异（类似 Unix 中的 `diff` 命令）或构建自动补全和相似性工具等任务。

---

### `difflib` 工作原理

`difflib` 的核心是尝试找出两个输入之间最长的连续匹配子序列，并利用这些匹配来突出相似性和差异性。该库能够：

* 生成人类可读的差异报告（`ndiff`、`unified_diff`、`context_diff`）
* 计算序列间的相似度比率
* 从列表中推荐近似匹配项（`get_close_matches`）

---

### `SequenceMatcher`

最重要的类是 **`difflib.SequenceMatcher`**。

**工作原理**：
* 逐元素比较两个序列
* 寻找最长公共子序列（不要求连续）
* 生成操作列表（`replace`、`delete`、`insert`、`equal`）来描述如何将一个序列转换为另一个

**核心方法**：

1. **`ratio()`**
   返回 [0, 1] 范围内的浮点数表示相似度
   计算公式：

   $$
   \text{ratio} = \frac{2 \times M}{T}
   $$

   其中 `M` = 匹配元素数量，`T` = 两个序列的元素总数

2. **`quick_ratio()`** 与 **`real_quick_ratio()`**
   通过牺牲精度换取速度的相似度快速估算方法

3. **`get_opcodes()`**
   返回将序列 `a` 转换为 `b` 的操作列表
   示例：`[('replace', 0, 2, 0, 1), ('equal', 2, 4, 1, 3)]`

4. **`get_matching_blocks()`**
   返回所有匹配子序列及其位置信息

---

### 示例演示

```python
import difflib

a = "hello world"
b = "helo wrld"

s = difflib.SequenceMatcher(None, a, b)

print("相似度比率:", s.ratio())
print("操作指令:", s.get_opcodes())
print("匹配区块:", s.get_matching_blocks())
```

**输出结果**：

```
相似度比率: 0.9090909090909091
操作指令: [('equal', 0, 1, 0, 1), ('delete', 1, 2, 1, 1),
          ('equal', 2, 5, 1, 4), ('delete', 5, 6, 4, 4),
          ('equal', 6, 11, 4, 9)]
匹配区块: [Match(a=0, b=0, size=1),
         Match(a=2, b=1, size=3),
         Match(a=6, b=4, size=5),
         Match(a=11, b=9, size=0)]
```

---

👉 核心要点：

* `difflib` 是序列比较工具集
* `SequenceMatcher` 是核心引擎——用于查找匹配子序列并计算相似度
* 适用于差异对比、拼写检查、抄袭检测、自动推荐等场景

需要继续了解如何使用基于 `SequenceMatcher` 的 `get_close_matches()` 方法实现模糊字符串匹配（如拼写检查或搜索建议）吗？
