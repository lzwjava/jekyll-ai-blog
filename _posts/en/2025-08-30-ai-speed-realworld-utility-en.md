---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Speed Meets Real-World Utility
translated: false
type: note
---

Here are the **key points** from the paper:

---

### Core Concept

* **Traditional AI benchmarks** focus mainly on accuracy/quality, but neglect **processing speed**, which is crucial in real-world, time-sensitive applications (e.g., autonomous driving, customer service).
* Existing speed metrics (TTFT, TPS) are **token-centric** and inadequate for a multi-modal AI future.
* **Proposed new metric**: **Intelligence Bandwidth** — the amount of useful information an AI can produce per unit of time.

---

### Approximations of Intelligence Bandwidth

1. **Benchmark score per time**

   * Use normalized benchmark performance divided by time taken.
   * More informative than tokens/sec for practical tasks.

2. **Information theory approach**

   * Measure output information content via probability distributions.
   * Limited since info ≠ usefulness and requires access to probability vectors.

3. **Raw output bits per second**

   * Simplest, modality-agnostic.
   * Measures bits/sec of AI output (text, image, video).
   * Doesn’t directly measure usefulness, but works if applied only to top-performing models.

---

### Historical Context

* Speed was ignored previously because:

  1. AI wasn’t advanced enough to need it.
  2. Applications were narrow and task-specific.
* With **LLMs** and **multi-modal AI**, a **unified speed metric** has become necessary.

---

### Human-AI Interaction Implications

* Similar to **Moore’s Law** and **Nielsen’s Law**, this metric can reveal growth trends.
* **Threshold concept**: once AI output speed surpasses human perceptual speed (e.g., reading or listening), real-time interaction becomes possible.
* AI already exceeds human reading and listening speeds; next frontier is **real-time image and video integration**.
* Future: AI may support **real-time visual reasoning, whiteboard-style design, and immersive virtual environments**.

---

### Experiments & Data

* Measurement across historic LLMs, image, and video generators using **raw output bits/sec**.
* **Observations**:

  * LLMs: 0–3 KB/s.
  * Image generators: exponential growth.
  * Video generators: currently lag but expected to accelerate.
  * **Gemini 2.5 Flash** is an outlier (optimized for low latency).

---

### Jin’s Law

* **Formulation**: *The intelligence bandwidth of the best publicly available hosted AI model doubles every year.*
* Currently led by **image generators**; video expected to take over as serving improves.
* **Predictions**:

  1. **Image integration into AI chat** will become standard within 1 year.
  2. **Real-time video interaction** feasible within \~3 years (requires \~8× speedup).

---

### Limitations

* Defining **“useful information”** remains unresolved.
* Current data is sparse, so the 1-year doubling estimate is uncertain.
* Growth may be limited by energy/economy, not just tech progress.

---

### Takeaway

* AI evaluation must account for **both correctness and speed**, mirroring human intelligence assessment.
* **Intelligence Bandwidth** offers a predictive framework for AI’s future, especially for **real-time, multi-modal interaction**.

---

Do you want me to also create a **visual-style timeline** of Jin’s Law predictions (text → images → video → immersive environments) so it’s easier to grasp at a glance?
