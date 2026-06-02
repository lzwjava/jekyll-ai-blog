---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试与静态分析对比详解
translated: true
type: note
---

问题：<https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/> 的博客文章说了什么？

回答：

这篇文章，**"Tests and Static Analysis"** 作者王垠（2013年12月27日发布），系统地解释了软件测试和 static analysis 之间的区别。以下是全面的分解：

---

## 背景

作者开发了用于 Python 的 static analysis 工具 PySonar，经常被问到：“testing 和 static analysis 有什么区别？”——于是写了这篇文章，给出系统性的回答。

---

## 1. 静态 vs. 动态特性

static analysis 和 tests 都旨在提高代码质量，但它们在本质上不同：static analysis **不运行程序**（静态），而 tests **执行程序** 并使用实际输入（动态）。

- **Static analysis** 就像编译器类型检查器（type checker）的更强大版本。它可以检测资源泄漏、数组索引越界以及安全风险——本质上是推理 *可能* 发生的情况。
- **Tests** 就像“现实生活中的小实验”——它们在特定条件下运行程序并观察结果。

Static analysis 可以发现 tests 可能永远检测不到的问题（例如，导致安全漏洞的复杂事件链），而 tests 可以捕获 static analysis 无法检测的 bug（例如，自动驾驶仪在特定高度和速度下产生错误结果）。

---

## 2. Tests 无法证明正确性

通过 tests **并不**意味着程序是正确的——它只意味着你没有做“非常愚蠢的事情”。要正式保证正确性，你需要使用像 Coq、Isabelle 或 ACL2 这样的定理证明器进行机械证明，这需要深刻的数学知识，而且往往不可行。

---

## 3. 人工劳动的差异

Testing 需要大量的手动工作。为“愚蠢的 bug”如空指针解引用编写 tests 很繁琐，而且实现良好的 **path coverage** 几乎不可能，因为执行路径的数量随着程序规模呈指数增长。

相比之下，static analysis 是 **完全自动的**。它系统地探索所有路径，提供远高于任何人类测试编写者所能达到的 path coverage——即使使用启发式方法来控制运行时间。

---

## 4. 符号推理

Tests 使用 **具体的输入值**，因此未测试的值处的 bug 可能溜过去。Static analysis 是 **符号化的**——它对每个变量的 *所有可能值* 进行推理，而不仅仅是具体值。这允许它检测边界条件 bug（例如，数组索引越界），而 tests 只有在恰好使用正确输入值时才能捕获这些 bug。

---

## 5. Static Analysis 中的假阳性

一些 static analysis 工具设计得较为保守——不确定时，它们会警告“这里可能有问题”。这可能导致 **false positives**（关于实际永远不会发生的 bug 的警告）。Static analysis 中的大量工程工作就是降低 false positive 率。

另一方面，tests **没有 false positives**——如果 test 失败，程序在那些条件下确实失败了。

---

## 6. Static Analysis 的价值

Static analysis 是最强大的 bug 发现工具，不需要大量的手动劳动。它处理无脑、繁琐的 bug 捕获（像可能导致飞机坠毁或导弹发射的空指针解引用），从而让人类测试者专注于更有智慧和趣味的 tests。

---

## 总结表格

| 维度 | Static Analysis | Testing |
| --- | --- | --- |
| 运行时机 | 不执行代码 | 通过执行代码 |
| 覆盖率 | 指数级高（自动化） | 受限于人力 |
| 值 | 符号化（所有可能值） | 仅具体输入 |
| 假阳性 | 可能有 | 无 |
| 证明正确性？ | 否 | 否 |
| 人工努力 | 低 | 高 |

参考文献：

- [https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/](https://yinwang0.wordpress.com/2013/12/27/tests-and-static-anaysis/)
