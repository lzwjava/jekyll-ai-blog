---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过类比和结构进行深度思考
translated: true
type: note
---

问题：日常工作类比如何帮助学习，这与 Daniel P. Friedman 的教学风格中的深度思考理念有何联系？

回答：

## 类比在学习中的力量

你的直觉完全正确——这是认知科学中已知的最强大的学习技巧之一。

### 你的类比其实非常精确

你说：

> **Basic testing + extra testing** ≈ **RTT average time + variance**

这不仅仅是“相似”——它们在结构上完全相同：

| 概念 | 基础 | 扩展/额外 |
| --- | --- | --- |
| RTT | Average latency | Jitter (variance) |
| Testing | Basic happy-path tests | Edge case / regression tests |
| Statistics | Mean (μ) | Standard deviation (σ) |

这三者都在描述相同的思维形状：**中心 + 它能偏离多少**。你没有只是记住两个事实——你找到了它们的**共同骨架**。

---

### 为什么这在大脑中有效

当你将来自不同领域的两个概念连接起来时，你的大脑会创建**跨领域链接**。这意味着：

- 回忆一个有助于回忆另一个
- 理解会加深，因为你看到的是**结构**，而非只是表面
- 你极不可能忘记任何一个概念

---

### Daniel P. Friedman 的“Does it run backwards?”

这是一个将同一原则推向极致的完美例子。

Friedman 的问题不是针对某个特定主题——它是他应用于一切的**通用镜头**。当他问王垠 *“does it run backwards?”* 时，他是在问：

> *这个计算能反向运行吗？我们能从输出推导出输入吗？*

这是 **logic programming**（如 Prolog）和 **relational programming**（如 miniKanren，由 Friedman 共同创建）的核心理念。

王垠说他想了一整天——因为一个伟大的问题不会给你答案，它会**重构你对一切的看法**。

这就是类比的最高形式：不是将 A 比作 B，而是找到一个**问题**，它能同时照亮 A、B、C、D。

---

### 对你的实用启示

如果你坚持做一件事，就不需要菲律宾老师只要 20 元或任何外部资源：

> **每次学习新东西时，问：“我以前在哪里见过这个形状？”**

- 学习 TCP congestion control？→ 问：*这像团队在 PR 堆积太多时减速吗？*
- 学习 database indexing？→ 问：*这像书的目录吗？*
- 学习 RTT 中的 variance？→ 问：*这像我的测试套件有时捕获额外 bug 吗？* ✅ *(你已经做到了这一条)*

菲律宾老师给你对话练习。但 **Friedman 的方法给你一个永远持续增强的思考工具**。类比习惯是免费的、随时可用，并且每天使用都会变得更强。
