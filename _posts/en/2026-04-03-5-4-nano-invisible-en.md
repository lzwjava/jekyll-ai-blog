---
audio: false
generated: true
image: false
lang: en
layout: post
title: 5.4 Nano Not Visible in VSCode
translated: false
type: note
---

Question: Why can’t I see **5.4 nano** in VSCode even though it’s enabled in the GitHub Copilot enterprise web page?

Answer:

This is normal. In GitHub Copilot Enterprise, **“enabled in admin” ≠ “visible in VSCode model picker.”**
There are **three separate gates**:

1. Org enabled model
2. Feature rollout to IDE
3. Agent mode supports that model

If any one is missing → you won’t see **5.4 nano**.

---

# Most common reasons

### 1. VSCode extension version too old (most common)

5.4 / nano models only appear in **new Copilot Chat builds**.

Update both:

* GitHub Copilot
* GitHub Copilot Chat

In VSCode:

```
Extensions → GitHub Copilot → Update
Extensions → GitHub Copilot Chat → Update
```

Then reload:

```
Developer: Reload Window
```

This alone fixes it in many cases.

---

# 2. Model enabled for org but not for chat

Enterprise admin panel has **separate toggles**:

* inline completion models
* chat models
* agent models

Sometimes admin enabled:

```
5.4 nano → inline only
```

So you won't see it in **Agent model picker**.

---

# 3. Agent mode only shows “agent-supported” models

Some models are:

* chat-only
* inline-only
* agent-capable

If 5.4 nano is **inline optimized**, it may not appear in Agent.

Then Copilot internally uses:

```
Agent planner → 5.4
Executor → 5.4 nano
```

but UI only shows **5.4**

So you *are using nano*, just not selectable.

---

# 4. Enterprise policy hides model picker

Some orgs lock:

* default model
* hide dropdown
* enforce allowed list

Then VSCode shows only:

```
Default (managed by org)
```

But backend still uses nano.

---

# How to verify what's actually used

Open VSCode:

Command palette:

```
Copilot: Show Debug Info
```

or

```
Copilot: Open Logs
```

You may see:

```
model: gpt-5.4
executor: gpt-5.4-nano
mode: agent
```

This confirms nano is used.

---

# Another way: check status bar

Bottom-right in VSCode:

Sometimes shows:

```
Copilot: GPT-5.4 (Agent)
```

Even if nano is executor.

This is expected.

---

# The key thing

Copilot architecture:

```
Agent planner → bigger model
Execution → nano
Edits → nano
```

UI only shows planner model.

So you won't always see nano.

---

# If you really want it selectable

You need:

* latest Copilot Chat
* model picker enabled
* org allows manual selection
* nano flagged as agent model

Otherwise it's backend-only.

---

Short answer:

You likely **already have 5.4 nano**, but it's used internally and not shown in VSCode UI.
