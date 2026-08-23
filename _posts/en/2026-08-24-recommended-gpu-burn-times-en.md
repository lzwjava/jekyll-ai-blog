---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recommended GPU Burn Times
translated: false
type: note
---

**Question:** How long should we run gpu-burn for a proper GPU stress test?

**Answer:**

It depends on your goal:

---

### Quick Sanity Check — `60` to `120` seconds

```bash
./gpu_burn 60
./gpu_burn 120
```

- Good for: just installed a GPU, after driver update, quick health check
- Catches obvious failures fast

---

### Standard Stability Test — `600` seconds (10 min)

```bash
./gpu_burn 600
```

- Good for: new system build, after reseating GPU, before deploying a workstation
- Long enough for thermals to fully stabilize and reveal throttling

---

### Serious Stability / Overclock Validation — `3600` seconds (1 hour)

```bash
./gpu_burn 3600
```

- Good for: validating an overclock, burn-in a new GPU before production use
- Sustained load reveals memory errors that short tests miss

---

### Production Server / Mission-Critical — `14400`+ seconds (4+ hours)

```bash
./gpu_burn 14400
```

- Good for: data center GPU acceptance testing, before running expensive training jobs
- Industry standard for server GPU qualification

---

### What to Watch During the Test

| Metric | What's Healthy |
| --- | --- |
| `errors` | Must stay at **0** the entire time |
| `temps` | Should **stabilize** and not keep climbing |
| `Gflop/s` | Should remain **consistent** — a drop signals thermal throttling |

---

### Your RTX 4070 Result Context

Your 20-second run showed **61°C peak** and **zero errors** — very healthy. For a personal workstation, a **10-minute run** (`./gpu_burn 600`) would give you solid confidence. If you're about to run long ML training jobs, do **1 hour**.
