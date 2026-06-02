---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 引导的战略多提交樱桃挑选
translated: true
type: note
---

Question:
我们可以使用像 Copilot 这样的代码助手，从 branch A cherry-pick 数十个 commits 到 branch B，并通过仔细提示来按功能控制冲突策略（prefer theirs vs ours）吗？

Answer:

是的——这实际上是代码助手的**非常好的用例**。特别是在以下情况：

* 必须 cherry-pick **数十个 commits**
* 某些功能应该 **prefer theirs**
* 某些功能应该 **prefer ours**
* 手动冲突解决会 **繁琐且容易出错**

你的想法是正确的。助手可以充当**引导式合并操作器**，而你按功能定义策略。

---

# 为什么这很有效

Cherry-pick 多个 commits 通常会导致：

* 重复冲突
* 混合所有权（某些文件要 theirs，某些要 yours）
* 依赖排序问题
* 容易遗漏的语义冲突

代码助手可以：

* 分析冲突上下文
* 遵循你定义的规则
* 按功能应用不同策略
* 一致地生成正确的解决方案

---

# 示例工作流程（最佳实践）

### Step 1 — 在提示中定义规则

示例：

```
We are cherry-picking commits from branch A into branch B.

Rules:
- For feature "payment", prefer theirs
- For feature "logging", prefer ours
- For config files, always prefer ours
- For new files, prefer theirs
- Do not remove existing API signatures
- Keep tests from both sides
```

这为助手提供了**合并策略**，而不仅仅是指令。

---

### Step 2 — 顺序 cherry-pick

```
git cherry-pick <commit1>
```

发生冲突时：

向 Copilot / 助手询问：

```
Resolve conflicts using rules:
- payment: theirs
- logging: ours
- config: ours
- new files: theirs
```

这比盲目使用 **要安全得多**：

```
git cherry-pick -X theirs
```

因为 `-X theirs` 是**全局应用**的，而不是选择性的。

---

# 何时这比 git 标志好得多

Git 只支持：

```
-X ours
-X theirs
```

但你想要：

* feature A → theirs
* feature B → ours
* file C → manual merge
* test → combine both

只有 AI/代码助手才能**按冲突进行推理**。

---

# 更好：批量策略

你可以告诉助手：

```
Cherry-pick these commits:

A1 A2 A3 A4 A5

Strategy:
- commits A1-A2: prefer theirs
- commits A3-A4: prefer ours
- A5: manual merge
```

这非常强大。

---

# 另一个强大模式

让助手生成命令：

```
git cherry-pick A1
git checkout --theirs src/payment/*
git checkout --ours config/*
git add .
git cherry-pick --continue
```

这结合了：

* 自动化
* 正确性
* 可审计性

---

# 重要警告（你正确注意到了）

提示质量非常重要。

坏提示：

> fix conflict

好提示：

```
Resolve conflict.
Rules:
- Keep branch B logging system
- Use branch A payment implementation
- Preserve both test cases
- Do not change public interfaces
```

要安全得多。

---

# 此方法特别有用的场景

* backporting features
* partial feature migration
* long-lived branch sync
* refactor branch merge
* vendor fork updates
* large monorepo merges

---

# 另一个专业提示

使用 **no-commit 模式**：

```
git cherry-pick -n <commit>
```

然后让助手在 commit 前解决。

这给你**完全控制**。

---

# 总结

是的——你的理解正确：

* Cherry-pick 多个 commits ✅
* 按功能策略（ours/theirs） ✅
* 代码助手帮助推理 ✅
* 提示精确性至关重要 ✅
* 比单独使用 git 标志更安全 ✅

这实际上是一个**非常高级的 Git 工作流程**。
