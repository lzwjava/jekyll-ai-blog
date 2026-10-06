---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSD alone is enough
translated: false
type: note
---

Question: If I only plug an SSD into the motherboard, do I also need a hard disk drive (HDD)?

Answer: **No. An SSD alone is enough.** You do **not** need an HDD.

For a normal PC:

```text
Motherboard
   │
   ├── SSD ──→ OS + applications + files
   │
   └── HDD ──→ optional extra storage
```

For example:

* **500 GB / 1 TB SSD** → completely sufficient to install Windows/Linux and run the computer.
* **SSD + HDD** → useful if you want **cheap, high-capacity storage** (e.g. 4–12 TB).
* **NVMe SSD** → plugs directly into the motherboard's M.2 slot.
* **SATA SSD/HDD** → connects with SATA data + power cables.

So if you're building your GPU/LLM test machine, you can simply do:

```text
CPU + motherboard + RAM + GPU + PSU + SSD
```

and it will work. An HDD is optional.