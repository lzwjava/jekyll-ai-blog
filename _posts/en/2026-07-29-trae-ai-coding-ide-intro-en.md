---
audio: false
generated: true
image: false
lang: en
layout: post
title: Trae AI Coding IDE Intro
translated: false
type: note
---

Question: Intro to [https://www.trae.cn](https://www.trae.cn)

Answer:

![Image](https://images.openai.com/static-rsc-4/5j9kFnRWd_A3oWVkUSKljJTOXV40Gf5MUlo6ON7FOO3NF1MU0ClWFt-E-pAOuqLVhtd_dW2iTiMfh6EaETBgZqbRyVeYsCDzNWNi1AZtafJK9_WAICEgKKs2KNbm2sOqoi8OUGJYrgf_l83lXN_7nbEpjY6S_oJtmmStq1IL9GpQbh5zThj5Kk3ICmsm4TBz?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Cvf1Rbz1prJgtlT_pdc1TkhIbzrAOYKp7ALciQFTvSSPnJKetPQS7CgauKT8ZsCVYHBdWZY6NCE8ax53COQm0z8PM3IwPyCOfiTQglep4-eseFxKarV1Suvuk2NqHkN11GhHVgIZVUfUL4UJikcW3t3cxnBaJ5SzDdQAuSU1cs4NxdYMcFWOGebKPUgxwF2b?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0neUZQk_nENnrKogVSDVBtO8FeJ1lDoNn6NUexixCj0PXyRlrqVanpxu_lZYayqP79PHAh8FjT8cSBNthEbN1uPOAMWoxT1bvSDQjOFFPeUMX_MaZ2TTitEeQl4K4YabIaq6loWG3aN-ODk1fxmVhI3i9peoU6RRHvXG4I4pqqLnmfRZeO2O-8w6QaDYQmO5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/l5Beoi0oVNJ1xSP3DE-GHts-iU2D-r1mIa8Ij-zqLZBZaKPQCrTw22zgPtuYeG7hJwpEfVPjc387o8DOfq0uNJautlBkHwuJN7vCCZvDXCJOnr6dejxqG0ZVAGtqcws7ajVldoXWaaw9gxLRBqn3dsJFrt1SzASrQfGcpEg1IdeMe_HZr5NkT4OXz2aca5Y_?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/U_oF_fjy0mEZnWJb8epQZBwvV7-tzbdD9sU5IEaXP1Gt0MGpHzJtJvWyYyXBU4Iy9ASaC2-okuNoadNCEkLGFuhFpCip1IdHQehvRRYw3iEndbA_9iqusWjdKd5RIdmynnDpWbc37y3yL6_l4KYmYddqsCcOsfG-ejGPDVbp7oSrfz2qqWejJf_U-Mv_IK-0?purpose=fullsize)

**TRAE** is an AI-native coding IDE created by ByteDance. The positioning is:

> "The Real AI Engineer" — an AI coding engineer that works with developers, not just autocomplete. ([Trae][1])

Think of it as ByteDance's answer to:

* Cursor
* GitHub Copilot
* Windsurf

It is basically **VS Code + LLM agent + project understanding + autonomous coding workflow**. ([Trae][2])

---

## Core idea

Traditional IDE:

```
Human
 |
 | writes code
 v
IDE
 |
 v
Compiler / Runtime
```

AI IDE:

```
Human intent
      |
      v
  AI Agent
      |
 +----+----+
 |         |
Codebase  Tools
 |         |
 v         v
Modify   Test
Code     Debug
 |
 v
Working Software
```

The developer moves from:

> "write every line"

to:

> "define intent, review changes, steer the agent"

This is the same direction as Claude Code, OpenAI Codex agents, Kimi Code, Manus-style agents.

---

## Main features

### 1. AI pair programmer

You can ask:

```
Explain this repository
Find authentication bug
Refactor this module
Add API endpoint
Write tests
```

The agent reads project context and edits files.

Similar workflow:

```bash
git clone my-project

trae

> understand this repo
> migrate spring boot 2 -> 3
> run tests and fix errors
```

---

### 2. Builder mode

One interesting feature is "Builder":

You describe a product:

```
Build a SaaS dashboard.

Requirements:
- React frontend
- Spring Boot backend
- PostgreSQL database
- User login
- Payment page
```

The agent tries to:

1. create architecture
2. generate files
3. install dependencies
4. connect components
5. run/debug

([Trae][3])

This is closer to an **AI software factory**.

---

### 3. SOLO agent

TRAE has a more autonomous mode called SOLO.

Conceptually:

```
Task
 |
 v
Planner Agent
 |
 +-- Coding Agent
 |
 +-- Testing Agent
 |
 +-- Debug Agent
 |
 v
Final PR
```

TRAE describes SOLO as an agent that can handle larger development tasks with planning and execution. ([Trae][2])

---

### 4. MCP / tools integration

Modern AI coding agents need tools:

```
LLM
 |
 +-- filesystem
 +-- terminal
 +-- browser
 +-- git
 +-- database
 +-- documentation
```

TRAE supports MCP-style external tool access, allowing agents to use additional resources. ([Trae][2])

---

## Why ByteDance built it?

Because software engineering is becoming an agent competition.

Old stack:

```
Engineer
   |
 IDE
   |
 Code
```

New stack:

```
Engineer
   |
 Intent
   |
 AI Agent Team
   |
 Codebase
   |
 Production
```

ByteDance already has:

* huge engineering organization
* internal codebases
* AI model infrastructure
* product iteration culture

So an AI IDE is strategically important.

---

## Compared with Cursor

Rough comparison:

|            | TRAE                 | Cursor             |
| ---------- | -------------------- | ------------------ |
| Company    | ByteDance            | Anysphere          |
| Base       | VS Code style        | VS Code fork       |
| Focus      | AI engineer workflow | AI pair programmer |
| Agent      | Strong emphasis      | Strong             |
| Enterprise | Growing              | Growing            |
| Ecosystem  | ByteDance ecosystem  | Independent        |

---

## For someone building agents / AI products

TRAE is interesting because it represents the next abstraction:

Before:

```
Developer writes code
```

Now:

```
Developer designs loops:

Goal
 ↓
Agent
 ↓
Tools
 ↓
Feedback
 ↓
Iteration
```

This matches your "loop engineering" idea.

A future engineer may spend more time writing:

```yaml
agent:
  goal: migrate payment service
  tools:
    - github
    - terminal
    - database
  evaluator:
    - unit_test
    - benchmark
```

than manually editing thousands of lines.

---

## Things to watch

### Privacy

Like any cloud AI IDE:

```
Your code
   |
   v
Remote model inference
   |
   v
AI provider servers
```

For private company code, check policies carefully. There have been community discussions and reports raising questions around telemetry and data collection, so enterprises should review security settings before adoption. ([TechRadar][4])

---

## My view

TRAE is not just "another Copilot".

The interesting part is the transition:

```
Copilot era (2022-2024)

AI = autocomplete


Agent era (2025+)

AI = junior engineer
```

TRAE, Cursor, Claude Code, Codex, Kimi Agent are all competing for the same future:

**the operating system for human + AI software development.**

For your workflow (nanoGPT, vLLM, agents, CLI tools), the interesting experiment would be:

```
TRAE + your repo
        |
        v
Ask it:
"Understand this AI agent framework.
Find 5 architectural improvements.
Implement one and run tests."
```

That tests whether it is actually an engineering agent rather than just a chat wrapper. ([Trae][2])

References:

* [TRAE official website](https://www.trae.cn/)
* [TRAE AI IDE product page](https://www.trae.ai/?utm_source=chatgpt.com)
* [TRAE enterprise introduction](https://www.trae.cn/enterprise?utm_source=chatgpt.com)

[1]: https://www.trae.cn/ "TRAE - The Real AI Engineer | TRAE - The Real AI Engineer"
[2]: https://www.trae.ai/?utm_source=chatgpt.com "TRAE - Collaborate with Intelligence"
[3]: https://trae.ai-kit.cn/home.html?utm_source=chatgpt.com "Trae ｜ 官网下载 ｜ 文档·教程 | 字节跳动免费AI编程IDE"
[4]: https://www.techradar.com/pro/security/bytedance-ai-tool-caught-spying-on-users?utm_source=chatgpt.com "ByteDance AI tool Trae caught spying on users"
