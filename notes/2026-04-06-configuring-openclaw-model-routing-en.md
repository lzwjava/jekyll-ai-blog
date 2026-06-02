---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring OpenClaw Model Routing
translated: false
type: note
---

Question: How to set the default model to `openrouter/minimax/minimax-m2.7` and switch to local `DeepSeek R1` in OpenClaw?

Answer:

You’re configuring **OpenClaw model routing**. There are two parts:

* Set **default model** → `openrouter/minimax/minimax-m2.7`
* Switch **manually** to local model → `/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf`

Here are the correct ways to do it.

---

# Method 1 — Set default model (recommended)

Edit your **OpenClaw config file**:

```
~/.openclaw/config.yaml
```

or project-level:

```
.openclaw/config.yaml
```

Set:

```yaml
model: openrouter/minimax/minimax-m2.7
```

Now OpenClaw will **default to MiniMax M2.7**.

---

# Method 2 — Switch model interactively

Inside OpenClaw chat:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

This switches to **local DeepSeek R1** immediately.

To switch back:

```
/model openrouter/minimax/minimax-m2.7
```

---

# Method 3 — CLI launch override

You can also start OpenClaw with:

```
openclaw --model openrouter/minimax/minimax-m2.7
```

or local:

```
openclaw --model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

---

# Method 4 — Workspace-level (per project)

Create:

```
.project-root/.openclaw/config.yaml
```

```
model: openrouter/minimax/minimax-m2.7
```

This is useful if:

* cloud model for coding
* local DeepSeek for offline
* different repos → different models

---

# Verify current model

Run:

```
/model
```

OpenClaw prints current active model.

---

# Typical best practice

Default:

```
openrouter/minimax/minimax-m2.7
```

Switch when needed:

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

This gives:

* fast cloud reasoning
* cheap local fallback
* offline capability

Exactly what your snippet describes.
