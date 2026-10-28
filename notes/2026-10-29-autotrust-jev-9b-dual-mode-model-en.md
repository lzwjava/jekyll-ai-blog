---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autotrust JEV-9B Dual-Mode Model
translated: false
type: note
---

**Question:** What is autotrust/JEV-9B, and what are its key features and capabilities?

---

**Answer:**

**autotrust/JEV-9B** is an open-weights language model (~9B parameters) built by **AutoTrust AI Lab**, designed as an integrated **System 1 + System 2** decision and reasoning model. It is built on the **Blocks of Experts (BoE)** recipe on top of a frozen Qwen3.5-9B backbone.

---

### 🧠 Core Concept: Dual-Mode Thinking

JEV-9B serves two modes of thinking from a single set of weights:

- **System 1** — Fast, calibrated typed decisions in a single forward pass, returning a calibrated probability distribution. Supports three question types:
  - `noul` — yes/no (true/false)
  - `choice` — pick one of 2–16 options
  - `score` — rate on a 0–5 scale
- **System 2** — Standard text generation with optional step-by-step reasoning (thinking mode), using the unmodified Qwen3.5-9B backbone.

Both run on the same backbone in the same engine, and a request chooses its system.

---

### 🏗️ Architecture: Blocks of Experts (BoE)

Rather than fine-tuning one monolithic model, the BoE recipe keeps a strong pretrained model as a frozen expert block and adds a small, detachable expert block trained for one capability. In JEV-9B the System 2 block is Qwen3.5-9B, bit-identical to the release; the System 1 block is 40.2M trained parameters (0.5% of the backbone), trained in approximately 3 hours on one B200.

Because the blocks stay separate, adding System 1 costs System 2 nothing: HumanEval is 70.7% before and after, with all 164 completions byte-identical.

---

### 📊 Key Performance Highlights

| Metric | Value |
| --- | --- |
| Mean KL to TypeSafe Jev 1.13 (teacher) | **≈ 0.019** (near-indistinguishable) |
| Yes/No AUROC (`noul`) | **0.994** |
| Choice top-1 agreement with teacher | **90.2%** |
| Rating MAE (`score`, 0–5) | **0.103** |
| Calibration error (ECE) | **0.0007** (essentially perfect) |
| System 2 HumanEval pass@1 | **70.7%** (identical to base Qwen3.5-9B) |
| Single decision latency (one B200) | **~90 ms** |

On one B200, a single decision takes a median ~90 ms, against 238–301 ms measured independently for the hosted TypeSafe Jev 1.13 API, and one GPU sustains about 15× the decisions per second an independent benchmark achieved against that API.

---

### 👁️ Vision Update (October 3, 2026)

JEV-9B now takes images. Every step is one System 1 decision: camera image or screenshot in, a probability for every action out, in a single forward pass (about 0.2 s on one GPU).

Key vision demos include:

- **Robot arm pick-and-place** from camera images (MuJoCo simulation, ~165 ms/decision)
- **Computer use** (screenshot → element to click), completing 95% of 60 random multi-step tasks (shop, settings, mail; 3–7 clicks each), about 0.2 s per click.

---

### 🎓 Training

The model was trained on `SargeDev/jev-distill-corpus-v3` (740,957 rows), with three streams: `yuri_v3` (498,010 rows, TypeSafe Jev 1.13 full output distributions), `openjev_v2` (94,801 rows, Open-Jev programmatic labels, CC0), and `yuri_v1` (148,154 rows, placeholder labels, down-weighted).

---

### ⚠️ Limitations

System 1 mirrors TypeSafe Jev 1.13, including its mistakes. Where the teacher was wrong or uncalibrated, so is JEV-9B — it is unreliable for multi-hop reasoning, arithmetic, dates, counting, and adversarial inputs. The model is also English-centric and not recommended for high-stakes decisions without confidence gating.

---

### 🆚 JEV-9B vs JEV-27B (family comparison)

For routing, moderation, topic triage and short option lists, JEV-9B gives nearly the same answers 2.6× faster with a third of the weight memory. For long option lists (more than about 8), unfamiliar task families, code-rule checks, fraud screening, or when the System 2 path matters, use autotrust/JEV-27B.

---

**License:** Apache-2.0 | **Live Demo:** [news.guru.so](https://news.guru.so/ui)

---

**References:**

- [autotrust/JEV-9B · Hugging Face](https://huggingface.co/autotrust/JEV-9B)
