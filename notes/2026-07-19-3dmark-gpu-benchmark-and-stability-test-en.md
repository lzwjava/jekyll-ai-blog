---
audio: false
generated: true
image: false
lang: en
layout: post
title: 3DMark GPU Benchmark and Stability Test
translated: false
type: note
---

**Question: what's 3DMark test in GPU tools?**

**Answer:**

3DMark is a **GPU performance benchmark and stability testing tool**. It renders complex 3D scenes (like a game engine) and measures how fast your GPU can process them.

People use it mainly for:

1. **Performance comparison**
2. **Checking if a second-hand GPU is healthy**
3. **Overclock/undervolt stability testing**
4. **Detecting thermal problems**

Common 3DMark tests:

| Test             | What it measures                     | Typical use                |
| ---------------- | ------------------------------------ | -------------------------- |
| Time Spy         | DirectX 12, 1440p gaming performance | Most common GPU comparison |
| Time Spy Extreme | DX12, 4K workload                    | High-end GPUs              |
| Port Royal       | Ray tracing performance              | RTX cards                  |
| Fire Strike      | DirectX 11 performance               | Older GPUs                 |
| Steel Nomad      | Modern cross-platform GPU workload   | Newer GPUs                 |

Example:

A second-hand RTX 3090 seller may say:

> "3DMark 99.3%, temperature around 70°C"

Meaning:

* The card completed the benchmark.
* Its score is close to other RTX 3090 cards in the same benchmark database.
* It probably does not have obvious GPU core/memory problems.
* 70°C under load is a good temperature for a 3090.

A typical workflow when buying used GPU:

```bash
1. Run GPU-Z
   -> check model
   -> check VRAM size
   -> check BIOS

2. Run 3DMark Time Spy
   -> compare score

3. Run FurMark
   -> stress temperature

4. Run VRAM test
   -> detect memory errors
```

The difference between **3DMark and FurMark**:

|                    | 3DMark                     | FurMark                     |
| ------------------ | -------------------------- | --------------------------- |
| Goal               | Realistic gaming benchmark | Extreme stress test         |
| Workload           | Game-like scenes           | Very heavy GPU load         |
| Score              | Yes                        | No useful performance score |
| Detect overheating | Yes                        | Excellent                   |
| Detect bad GPU     | Good                       | Good                        |
| Used by gamers     | Very common                | Common for testing          |

For RTX 3090 specifically:

Typical Time Spy Graphics Score:

* RTX 3090 reference: around **19,000–20,000**
* Good factory OC cards: **20,000+**
* Bad cooling / throttling cards: significantly lower

For used mining cards, 3DMark is useful because a card can appear normal but have:

* degraded VRAM
* unstable memory clocks
* overheating under sustained load

I would trust:

* **3DMark + GPU-Z + temperature test + visual inspection**
  more than just "it works".

References:

* [3DMark official benchmark software](https://benchmarks.ul.com/3dmark?utm_source=chatgpt.com)
* [GPU-Z official website](https://www.techpowerup.com/gpuz/?utm_source=chatgpt.com)
