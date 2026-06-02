---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod vs DigitalOcean for GPU Work
translated: false
type: note
---

**Question:**
Is it reasonable that a normal DigitalOcean droplet keeps running (and charging about $8/week) even after stopping GPU training, and is it better to destroy it and restart on RunPod for short-term LLM training workloads?

---

**Answer:**

Yes — what you're observing is completely expected, and your conclusion is basically correct.

### 1. Why your DigitalOcean droplet keeps costing money

DigitalOcean uses a **traditional cloud billing model**:

* A *droplet = always-on VM*
* Billing is **time-based (hourly)**, regardless of usage
* Even if:

  * CPU is idle
  * No training is running
  * GPU droplet is shut down

👉 As long as the droplet exists, **you are paying for reserved resources (CPU, RAM, disk, IP)**

So your case:

* ~$8/week ≈ ~$0.05/hour → matches a small droplet
* Running for 1–2 weeks idle → normal billing behavior

---

### 2. Why this feels inefficient for LLM work

You’re doing something modern:

> short bursts of heavy compute (train, preprocess, stop)

But DigitalOcean is optimized for:

* web servers
* databases
* long-running services

NOT for:

* intermittent GPU jobs
* experimental training loops
* rapid start/stop workloads

---

### 3. Why RunPod feels better

RunPod is designed closer to **“compute as a job”** instead of “compute as a machine”:

* Pay **only when GPU is running**
* Easy to:

  * spin up
  * kill
  * restart
* No mental overhead about idle cost
* Better aligned with:

  * nanoGPT experiments
  * small model training (like GPT-2 124M)
  * trial-and-error loops

👉 That’s why it feels “牛叉” — it matches your workflow, not just your compute.

---

### 4. Your current situation (practical decision)

You said:

> 10 hours of work… droplet still running… busy… training paused

Here’s the rational move:

**Destroy the droplet.**

Because:

* The sunk cost (10 hours prep) is already paid
* The *ongoing cost* is pointless if idle
* Recreating environment is cheaper than leaking time/money

---

### 5. Snapshot vs rebuild (important tradeoff)

You mentioned snapshot — but your intuition is right:

| Option               | Pros                 | Cons                             |
| -------------------- | -------------------- | -------------------------------- |
| Snapshot             | saves environment    | still costs storage + complexity |
| Rebuild on RunPod    | clean, fast, aligned | need to redo setup               |
| Keep droplet running | zero effort          | **continuous cost leak** ❌       |

👉 For nanoGPT-scale work:
**Rebuild > Snapshot > Idle VM**

---

### 6. The deeper insight you already discovered (this is the real win)

You said:

> “关键认知：随机读写、20秒一步迭代”

This is actually more valuable than the 10 hours:

You now understand:

* **I/O bottlenecks** (random read/write → slow training)
* **Iteration time diagnostics** (~20s/step = something wrong)
* Relationship between:

  * dataset format
  * disk throughput
  * training speed

👉 This is exactly the kind of intuition that separates:

* “running models”
  vs
* “understanding systems”

---

### 7. What experienced people typically do

For your workflow:

* Data prep:

  * local machine OR cheap ephemeral VM
* Training:

  * RunPod / spot GPU / ephemeral instances
* Storage:

  * keep dataset separately (S3-like or local)

👉 Never keep compute alive without active work

---

### 8. Final judgment

Your conclusion is solid:

* DigitalOcean → **not designed for burst AI workloads**
* RunPod → **fits experimental LLM training perfectly**
* Destroying the droplet → **correct move**

---

If you want, I can help you design a **zero-waste nanoGPT workflow** (data → train → checkpoint → kill → resume) so you never lose time or money again.
