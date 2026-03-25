---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Use Superpowers Plugin Skills
translated: false
type: note
---

Question: How do I use the “skills” shown in `/skills` (from the superpowers plugin)?

Answer:

Those **skills** are reusable prompt templates provided by the **Superpowers** system. They are not commands by themselves — you **invoke them by name** when chatting with the CLI agent.

---

# How to Use Skills

You **call a skill explicitly** in your prompt.

General format:

```
/skill <skill-name>
```

or simply describe the task and reference the skill:

```
Use skill: brainstorming
```

or:

```
brainstorming: help me design a caching layer
```

All three usually work (depends on the CLI wrapper).

---

# Examples

## 1. brainstorming

```
/skill brainstorming
Help me design a local-first note app
```

This triggers structured ideation:

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

The skill forces the AI to:

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

This skill typically:

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

It will guide:

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

This forces AI to:

* implement
* test mentally
* verify edge cases
* validate output

Very useful for correctness.

---

# What `/skills` actually shows

It lists:

* skill name
* plugin source (`superpowers`)
* description tokens (prompt length)
* number of skills loaded

So:

```
brainstorming · superpowers · ~56 tokens
```

means:

* name = `brainstorming`
* provider = superpowers
* size = 56 tokens prompt template

---

# When to Use Skills

Use them when you want **behavior mode switching**:

| Use skill                      | When                 |
| ------------------------------ | -------------------- |
| brainstorming                  | exploring ideas      |
| receiving-code-review          | reviewing PRs        |
| finishing-a-development-branch | before merge         |
| verification-before-completion | correctness critical |
| using-git-worktrees            | multi-branch work    |

---

# Pro Tip (Best Usage)

You can combine them:

```
Use skill: brainstorming
Then use skill: verification-before-completion
Design a distributed rate limiter
```

This gives:

1. idea exploration
2. careful validated solution

---

# Mental Model

Skills = **preloaded expert prompts**

Instead of writing:

> "Please carefully analyze, think step by step..."

You just use:

```
/skill verification-before-completion
```

Much cleaner.

---

If you'd like, I can also show:

* how to create your own skills
* where skills are stored
* how superpowers loads them
* how to auto-trigger skills

Just tell me.