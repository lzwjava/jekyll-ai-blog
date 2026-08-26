---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KiCad S-表达式匹配Lisp
translated: true
type: note
---

**问题：** KiCad 的 S 表达式格式与 Lisp/Scheme 的 S 表达式相同吗？

**回答：**

是的，概念完全一致——KiCad 的格式直接受 Lisp/Scheme 的 S 表达式启发。具体对比如下：

**共同点**

核心语法在本质上相同：
- 圆括号用于分组：`(key value value ...)`
- 嵌套/递归结构
- 原子（符号、数字、字符串）

一段 KiCad 原理图片段如下：
```lisp
(kicad_sch
  (version 20230121)
  (symbol (lib_id "Device:R")
    (at 100.0 50.0 0)
    (property "Reference" "R1"
      (at 101.5 48.5 0)))
  (wire
    (pts (xy 100 50) (xy 110 50))))
```

这是纯粹的 S 表达式——Lisp 程序员阅读它会感到非常熟悉。

**与 Lisp/Scheme 的不同之处**

| 特性 | Lisp/Scheme | KiCad S 表达式 |
|---|---|---|
| 用途 | 代码 + 数据 | 仅数据 |
| 求值 | 由解释器执行 | 作为配置解析 |
| `car`/`cdr` 语义 | 有 | 无 |
| 宏 / lambda | 有 | 无 |
| 字符串 | `"..."` | `"..."` 相同 |
| 注释 | `;` 分号 | `#` 井号（KiCad 特有！） |

KiCad 的格式本质上是 **S 表达式纯粹用作数据序列化格式**——类似于 JSON，但使用圆括号而非花括号。没有求值，没有函数。

**历史背景**

这种模式已有先例——Emacs 配置文件、GNOME 的 GConf 以及许多 EDA 工具都使用 S 表达式作为 XML 或 JSON 的替代品，因为它具有人类可读且对版本控制系统友好的特性。KiCad 大约在 v5/v6 版本从旧的自定义格式切换到 S 表达式，正是因为它易于执行差异比较、解析和程序化生成。

**对于 AI/LLM 的用途**

由于它像 Lisp 一样具有规律性和递归性，你可以：
- 使用任何 Lisp 读取器（Common Lisp、Racket、Guile 均可直接使用）进行解析
- 在 Python 中使用简单的递归下降解析器或 `sexpdata` 库进行解析
- 直接将其输入给 LLM——该结构具有自文档特性

因此，是的——如果你了解 Lisp 或 Scheme，你已经在结构层面上理解了 KiCad 的文件格式。

**参考文献：**
- [KiCad 文件格式文档](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/)
- [维基百科：S 表达式](https://en.wikipedia.org/wiki/S-expression)