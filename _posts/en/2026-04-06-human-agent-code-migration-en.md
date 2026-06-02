---
audio: false
generated: true
image: false
lang: en
layout: post
title: Human-Agent Collaboration in Code Migration
translated: false
type: note
---

Looking back at our session — I delegated exactly **once** at the start via `sessions_spawn` (the sub-agent did the bulk CI3→CI4 conversion: 25 controllers, 32 models). After that, everything else I did **directly** with my built-in tools:

- **File editing** (`edit`, `write`) — fixing broken `define()` calls, syntax errors, namespace issues
- **Reading** (`read`, `exec`) — diagnosing errors, checking file contents
- **Shell** (`exec`) — running `curl` tests, `docker cp`, `grep`, `sed` for bulk fixes
- **Process debugging** — tracing stack traces, fixing CI4 DB API calls (`result()` → `getResult()`)

The pattern that emerged: the coding agent handled the **big upfront migration**, and I handled the **targeted debugging** that followed. Once I saw an error, I could fix it in 1-3 tool calls without spinning up another agent.

So to answer directly: **I delegate for large, unstructured tasks (building, mass refactoring, exploring an unfamiliar codebase)**. For **known, targeted fixes** (like fixing a specific error or updating a specific file), my direct tools are faster and more precise.
