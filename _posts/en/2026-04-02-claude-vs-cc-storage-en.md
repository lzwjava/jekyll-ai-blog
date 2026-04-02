---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code vs CC Storage Architecture
translated: false
type: note
---

Question: What is the conversation storage and prompt structure in CC code, and how does it compare to Claude Code?

Answer:

The prompt / conversation structure in Claude Code is **more structured and layered** than most “CC-style” code assistants (like simple chat-based code copilots). It is designed specifically for **long coding sessions, repo-aware reasoning, and tool use**.

Here’s the typical architecture.

---

# Claude Code Prompt Structure (Conceptual)

Claude Code internally builds a **multi-layer prompt** each turn:

### 1. System Layer (fixed)

* coding rules
* tool usage instructions
* diff format requirements
* safety + file edit policies

Example (conceptual):

```
You are Claude Code.
You can read/write files.
Return edits as unified diffs.
Prefer minimal changes.
```

---

### 2. Project Context Layer

Automatically injected:

* repo tree
* relevant files
* open files
* git status
* recent edits

Example:

```
Repository:
src/
  api.ts
  db.ts
tests/
  api.test.ts
```

This is **not chat history** — it's **state snapshot**.

---

### 3. Conversation Memory Layer

Recent turns only (sliding window)

```
User: refactor db layer
Assistant: suggested changes
User: make it async
```

Claude Code **does NOT keep full history**
It compresses / summarizes older turns.

This is important:

* avoids token explosion
* keeps reasoning focused
* improves long coding sessions

---

### 4. Tool Result Layer

Claude Code heavily uses tool outputs:

* file reads
* grep search
* AST search
* test results
* lint output

Example:

```
Tool: read_file src/db.ts
Result: ...
```

This becomes part of prompt.

This is **very different** from normal CC assistants.

---

### 5. Scratchpad / Planning Layer (hidden)

Claude Code internally does:

* plan
* reasoning
* edit strategy
* multi-step actions

Then outputs:

* explanation
* diff
* commands

---

# Compared to Typical "CC" Chat Code Assistants

Most CC-style assistants:

### Simple Structure

```
system prompt
chat history
user message
```

Sometimes plus:

* selected code
* open file

That's it.

No:

* repo memory
* tool chaining
* diff planning
* execution loop

---

# Claude Code Is Closer to an Agent Loop

It works like:

```
read files
↓
reason
↓
edit
↓
run tests
↓
fix
↓
repeat
```

Each step appended to prompt.

So conversation becomes:

```
User request
Tool read files
Plan
Apply diff
Run tests
Fix errors
Return result
```

This is **stateful execution**, not just chat.

---

# Key Differences

| Feature        | CC-style chat   | Claude Code          |
| -------------- | --------------- | -------------------- |
| History        | full chat       | sliding + summarized |
| Repo awareness | weak            | strong               |
| Tool use       | limited         | heavy                |
| File edits     | text suggestion | structured diffs     |
| Planning       | minimal         | multi-step           |
| Execution loop | no              | yes                  |
| Memory         | conversation    | project state        |

---

# Why Claude Code Feels Smarter

Because prompt includes:

* repo structure
* recent edits
* tool outputs
* plan
* diff format

Instead of just:

```
"Here is code, fix bug"
```

It becomes:

```
Here is repo
Here is failing test
Here is file
Here is previous attempt
Fix correctly
```

Much higher signal.

---

# Real Mental Model

Claude Code prompt each turn:

```
[system rules]
[repo snapshot]
[relevant files]
[conversation summary]
[last tool outputs]
[user request]
```

Then:

```
→ plan
→ modify
→ run tools
→ finalize
```

---

If you're comparing with:

* Cursor
* Copilot Chat
* OpenCode
* OpenClaw

I can break those down too — they all structure prompts differently.