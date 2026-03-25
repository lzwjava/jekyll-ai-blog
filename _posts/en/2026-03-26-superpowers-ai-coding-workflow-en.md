---
audio: false
generated: true
image: false
lang: en
layout: post
title: Superpowers AI Coding Agent Workflow Framework
translated: false
type: note
---

Question: What is the GitHub project [https://github.com/obra/superpowers](https://github.com/obra/superpowers) and how does it work?

Answer:

## Overview

**Superpowers** is an open-source **AI coding agent workflow framework**. It doesn’t add a new model — instead it **forces AI coding agents (Claude Code, Codex, OpenCode, etc.) to follow a disciplined software engineering process** using modular “skills”. ([AIToolly][1])

Think of it as:

> A **development methodology encoded as skills** that your AI agent must follow.

Instead of:

```
You: build login feature
Agent: writes random code immediately
```

It enforces:

```
1. clarify requirements
2. design
3. plan
4. implement (TDD)
5. review
6. merge
```

---

## Core Idea

Superpowers = **skills + workflow + auto-trigger rules**

* Skills = small capabilities (brainstorm, write plan, TDD, review)
* Workflow = strict order of execution
* Auto-trigger = agent automatically uses them

The agent **does NOT jump into coding** — it first extracts spec, creates plan, then executes using subagents. ([GitHub][2])

---

## How It Works (Step-by-Step)

### 1. Brainstorming (before coding)

Agent asks questions and clarifies what you actually want.

Example:

```
You: build todo app
Agent:
- web or mobile?
- local storage or backend?
- auth needed?
```

This produces a **design document**.

---

### 2. Write Implementation Plan

Then it creates **small tasks (2–5 min each)**

Example:

```
Task 1: create project structure
Task 2: add todo model
Task 3: write failing test
Task 4: implement minimal code
```

Each task includes:

* file paths
* exact code
* verification steps

This is generated automatically. ([GitHub][2])

---

### 3. Subagent-driven development

Now it spawns **sub agents** to execute tasks one-by-one:

* agent A writes code
* agent B reviews
* agent C runs tests
* agent D continues next step

This allows **long autonomous coding sessions**. ([GitHub][2])

---

### 4. Enforced TDD

It forces:

```
RED → failing test
GREEN → minimal fix
REFACTOR → cleanup
```

Agent is not allowed to write feature code before tests. ([志文工作室][3])

---

### 5. Automatic Code Review

After each task:

* spec compliance check
* code quality check
* block if critical issues

---

### 6. Finish Branch

When done:

* verify tests
* merge branch
* create PR
* cleanup workspace

---

## Built-in Skills (Examples)

### Planning

* brainstorming
* writing-plans
* executing-plans

### Development

* test-driven-development
* using-git-worktrees
* subagent-driven-development

### Debugging

* systematic-debugging
* verification-before-completion

### Collaboration

* requesting-code-review
* finishing-development-branch

All are composable skills. ([GitHub][2])

---

## Why This Project Is Popular

It fixes the **biggest AI coding problems**:

Without Superpowers:

* agent writes messy code
* no tests
* no plan
* random refactors

With Superpowers:

* design first
* small steps
* tests enforced
* reviews mandatory
* autonomous execution

It’s basically **turning LLM into disciplined junior engineer**.

---

## Supported Agents

Works with:

* Claude Code
* OpenCode
* Codex
* Cursor (manual)
* OpenClaw (community usage)

---

## Example Commands

After install:

```
/superpowers:brainstorm
/superpowers:write-plan
/superpowers:execute-plan
```

These control the workflow. ([GitHub][2])

---

## In One Sentence

**Superpowers = structured software engineering workflow for AI coding agents using modular skills.**

---

## When It’s Most Useful

This is especially powerful when:

* building large apps
* long autonomous coding
* multi-file refactoring
* TDD workflows
* agent-driven development

Less useful for:

* quick scripts
* small edits
* chat coding

---

If you want, I can also explain:

* how it compares to Claude Code default
* how to install
* whether it's better than "dangerously skip permission" style agents
* how people use it with OpenClaw

References:

* [https://github.com/obra/superpowers](https://github.com/obra/superpowers)
* [https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents](https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents)
* [https://new2026.medium.com/superpowers-obra-superpowers-claude-code-plugin-for-an-agentic-software-development-workflow-1e7bdffeb065](https://new2026.medium.com/superpowers-obra-superpowers-claude-code-plugin-for-an-agentic-software-development-workflow-1e7bdffeb065)
* [https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/](https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/)

[1]: https://aitoolly.com/ai-news/article/2026-02-26-superpowers-a-new-software-development-workflow-and-agent-skill-framework-for-coding-agents?utm_source=chatgpt.com "Superpowers: Agent Skill Framework & Software Development Workflow | AIToolly"
[2]: https://github.com/obra/superpowers?utm_source=chatgpt.com "GitHub - obra/superpowers: Claude Code superpowers: core skills library"
[3]: https://lzw.me/docs/opencodedocs/obra/superpowers/start/superpowers-intro/?utm_source=chatgpt.com "What is Superpowers: Software Development Lifecycle Workflow for AI Coding Agents | Superpowers Tutorial | OpenCodeDocs"