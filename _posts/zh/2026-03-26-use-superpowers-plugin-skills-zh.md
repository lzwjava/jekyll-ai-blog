---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何使用超能力插件技能
translated: true
type: note
---

Question: 如何使用 `/skills`（来自 superpowers 插件）中显示的 “skills”？

Answer:

这些 **skills** 是由 **Superpowers** 系统提供的可复用 prompt templates。它们本身不是命令 —— 你在与 CLI agent 聊天时**通过名称调用它们**。

---

# 如何使用 Skills

你在 prompt 中**显式调用一个 skill**。

通用格式：

```
/skill <skill-name>
```

或者简单地描述任务并引用该 skill：

```
Use skill: brainstorming
```

或者：

```
brainstorming: help me design a caching layer
```

这三种方式通常都有效（取决于具体的 CLI wrapper）。

---

# Examples

## 1. brainstorming

```
/skill brainstorming
Help me design a local-first note app
```

这会触发结构化的 ideation：

* goals
* constraints
* options
* tradeoffs
* recommended direction

---

## 2. receiving-code-review

```
/skill receiving-code-review
Review this PR:
<code here>
```

该 skill 会强制 AI 执行：

* look for bugs
* suggest improvements
* flag architecture issues
* check readability

---

## 3. finishing-a-development-branch

```
/skill finishing-a-development-branch
I'm about to merge feature/auth-refactor
```

该 skill 通常包括：

* checks tests
* checks lint
* checks commits
* ensures changelog
* merge checklist

---

## 4. using-git-worktrees

```
/skill using-git-worktrees
I want to work on two features at once
```

它将指导：

* create worktrees
* branch layout
* cleanup
* best practices

---

## 5. verification-before-completion

```
/skill verification-before-completion
Implement Redis caching for this service
```

这会强制 AI 执行：

* implement
* test mentally
* verify edge cases
* validate output

对保证 correctness 非常有用。

---

# `/skills` 实际显示的内容

它列出了：

* skill name
* plugin source (`superpowers`)
* description tokens (prompt length)
* number of skills loaded

例如：

```
brainstorming · superpowers · ~56 tokens
```

意味着：

* name = `brainstorming`
* provider = superpowers
* size = 56 tokens prompt template

---

# 何时使用 Skills

当你想要进行 **behavior mode switching** 时使用它们：

| Use skill                      | When                 |
| ------------------------------ | -------------------- |
| brainstorming                  | exploring ideas      |
| receiving-code-review          | reviewing PRs        |
| finishing-a-development-branch | before merge         |
| verification-before-completion | correctness critical |
| using-git-worktrees            | multi-branch work    |

---

# Pro Tip (最佳用法)

你可以组合使用它们：

```
Use skill: brainstorming
Then use skill: verification-before-completion
Design a distributed rate limiter
```

这将得到：

1. idea exploration
2. 经过仔细验证的 solution

---

# 心理模型

Skills = **预加载的 expert prompts**

与其编写：

> "Please carefully analyze, think step by step..."

你只需要使用：

```
/skill verification-before-completion
```

更加简洁。

---

如果你愿意，我还可以展示：

* 如何创建你自己的 skills
* skills 存储在哪里
* superpowers 如何加载它们
* 如何自动触发 skills

请告诉我。
