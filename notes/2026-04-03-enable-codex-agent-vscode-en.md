---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable Codex Agent in VSCode
translated: false
type: note
---

Question: How do you trigger the “Codex agent using 5.4 nano” architecture in VSCode? I only see Agent mode and Ask mode.

Answer:

Seeing **Agent** and **Ask** mode means you are already in the **correct UI**.
But **Codex vs non-Codex** is **not a separate button** — it’s controlled by **model selection**.

You trigger:

```
Agent mode
   + model = codex / 5.4 / 5.4 nano
```

That becomes:

```
VSCode
 └─ Copilot Chat
     └─ Agent mode
         └─ Model (5.4 nano / codex / etc)
```

---

# Step-by-step: how to trigger Codex agent

Do this inside VSCode:

### 1. Open Copilot Chat

```
Cmd/Ctrl + Shift + I
```

You should see:

* Ask
* Agent

Switch to **Agent**

---

### 2. Change the model (THIS is the key step)

Top of chat panel → model dropdown

Example:

```
GPT-5.4
GPT-5.4 mini
GPT-5.4 nano
Claude
Codex
```

Pick:

```
5.4 nano
```

Now Agent mode will use:

```
Agent planner + 5.4 nano executor
```

That is exactly:

```
Copilot
  → Agent
     → 5.4 nano
```

---

# If you don't see model picker

Enterprise org may:

* lock model selection
* set default model
* hide dropdown

Then Agent mode already uses **admin configured model**.

You can check:

```
VSCode settings
→ GitHub Copilot Chat
→ Model
```

or

```
Command palette
→ "Copilot: Change Chat Model"
```

---

# Ask vs Agent difference (important)

Ask mode:

* single response
* no file edits
* no planning

Agent mode:

* multi-step plan
* edit files
* run commands
* iterative

Codex only activates in **Agent mode**

So you're already in the right place.

---

# How to confirm you're using agent (Codex-style)

When Agent is active you'll see:

* "Planning..."
* "Analyzing repository..."
* "Editing 4 files..."
* "Running command..."

That is Codex-style behavior.

---

# If you want full Codex behavior

Use prompts like:

```
upgrade angular 14 to 17 across repo
```

or

```
refactor all services to use fetch instead of axios
```

Ask mode won't do this
Agent mode will

---

# Most likely your situation

You see:

Ask | Agent

You just need:

1. switch to Agent
2. choose model (5.4 nano)
3. run repo-level task

That's it.

You're already using Codex-style agent.

No extension needed.