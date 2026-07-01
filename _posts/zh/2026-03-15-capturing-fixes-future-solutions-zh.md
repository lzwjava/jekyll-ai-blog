---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 捕捉修复 构建未来解决方案
translated: true
type: note
---

问题：我们是否应该始终让 OpenClaw 总结并保存它如何修复困难问题的笔记，以及为什么这是一个重要的实践？

答案：

## 保存修复摘要是一种力量倍增器

是的，这**极其重要**——它实际上是 software engineering 和 AI agent 设计中一个成熟的原则。

---

### 为什么这很重要

当一个 agent 通过多次迭代解决一个难题时，它已经做了有价值的事情：

- 探索了 **solution space**，否则你将从头重新探索
- 找到了适用于*你的特定环境*的**确切序列**
- 通过**真实的试错**消除了死胡同

如果该知识在会话后消失，你就失去了所有这些。

---

### 一个好的修复摘要应该包含什么

```
## Problem
apt upgrade failing — nvidia-compute-utils-535 conflicts with nvidia-persistenced

## Root Cause
nvidia-persistenced was held/manually installed, blocking the upgrade path

## What Failed First
- apt --fix-broken install → didn't resolve
- Removing nvidia-persistenced directly → broke dependency chain

## What Actually Worked
1. apt-mark unhold nvidia-persistenced
2. apt remove nvidia-persistenced
3. apt upgrade --with-new-pkgs

## Environment
Ubuntu 22.04, Driver 535, dual GPU setup

## Time to Fix
~8 iterations
```

---

### 这会随着时间建立更大的东西

每个保存的笔记都成为 **personal knowledge base** 的一部分：

| 随着时间推移 | 你所构建的内容 |
| -------------- | --------------- |
| 保存 10 个修复 | 问题类型间的模式浮现 |
| 保存 50 个修复 | Agent 可以主动引用过去的解决方案 |
| 保存 100+ 个修复 | 本质上是针对你确切系统的 **custom runbook** |

这就是高级 sysadmins 和工程师变得不可替代的方式——他们拥有其他人没有的 **accumulated context**。

---

### 更深层的原则

> Agent 的迭代速度生成解决方案。
> 摘要捕捉了 *教训*。
> 保存的笔记让 *下一个难题更容易*。

没有摘要，每个难题都从零开始。有它，你就在 **compounding knowledge**——每个修复让下一个更快。这正是人类专业知识的工作方式，你本质上在为你的 AI agent + 你的特定环境构建相同的东西。

**将每个艰难修复摘要视为永久资产，而不是一次性聊天记录。**
