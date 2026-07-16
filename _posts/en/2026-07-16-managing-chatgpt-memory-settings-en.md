---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing ChatGPT Memory Settings
translated: false
type: note
---

**Question: How to change ChatGPT memory when Memory is enabled?**

**Answer:**

You can manage memory in two ways:

### 1. Ask ChatGPT directly

Use explicit commands:

```
Remember that I prefer English answers.
```

or

```
Update your memory: I no longer use AMD MI50. Remove that assumption.
```

or

```
Forget that I own an AMD MI50 GPU.
```

For corrections, be very specific:

```
Change memory:
- Old: I own an AMD MI50 16GB.
- New: I only researched MI50; I do not own one.
```

ChatGPT should update/remove the stored item.

---

### 2. Manage from Settings

Open:

```
ChatGPT → Profile icon → Settings → Personalization → Manage memories
```

There you can:

* View saved memories
* Delete individual memories
* Clear all memories
* Turn memory on/off

---

### 3. Best practice for avoiding wrong assumptions

Memory is not a full conversation database. It stores long-term facts that seem useful. Sometimes it can generalize incorrectly.

Use phrases like:

```
This is only a research topic, not something I own.
```

or:

```
Do not store this as a fact about me.
```

For hardware experiments, a good pattern is:

```
Update memory:
I discuss many GPUs for research. Do not assume I own a GPU unless I explicitly say I bought it.
```

That prevents future answers from treating every GPU you investigate as your hardware.
