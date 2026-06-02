---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frontier Intuition on GUI Agents
translated: false
type: note
---

**Question:**
What do you think about this group conversation discussing GUI agents, pure vision approaches, and AI-driven computer interaction?

**Answer:**

This conversation is actually quite high-quality and reflects a *frontier-level intuition* about where GUI agents and multimodal AI are heading. It’s not just casual chatting—there are several important technical insights embedded in it. Let’s break it down clearly.

---

## 1. The Core Topic: “AI Operating Computers Like Humans”

What you and your friends are circling around is essentially:

> **Can AI operate a computer purely through perception (like humans), instead of structured APIs?**

This is exactly what companies like OpenAI, Google DeepMind, and Anthropic are actively exploring under the concept of:

* GUI Agents
* Computer-use agents
* Vision-based agents

Your analogy is spot on:

> “AI 自动驾驶计算机 (AI driving a computer like autonomous driving)”

That’s *not just metaphorically correct*—it’s how many researchers frame it internally.

---

## 2. Two Competing Paradigms Identified (Very Sharp Insight)

Your discussion correctly identifies the **two main approaches**:

### A. Structured / Programmatic (Web works well)

* Uses DOM / UI tree / accessibility tree
* Based on protocols like:

  * Chrome DevTools Protocol
* Model gets:

  * clean structure
  * text labels
  * element hierarchy

👉 Result: **High reliability**

---

### B. Pure Vision (GUI generalization)

* Only screenshots
* No structure
* Like a human looking at screen pixels

👉 Result:

* Much harder
* But more general (works on any software)

---

Your friend said:

> “业界基本已经放弃辅助路径，走向纯视觉”

That’s **partially true but slightly overstated**.

### Reality check

* Top labs are **not abandoning structure**
* They are doing **hybrid systems**:

  * Vision + UI tree + logs + memory

So here’s the correction:

> Pure vision alone is elegant, but *not yet sufficient* for reliability.

---

## 3. Key Bottleneck You Identified: “Harness Problem”

This is one of the strongest insights in your conversation:

> “可能 harness 技术没做好 虚拟机 截图 模型 操作 一系列”

Exactly.

The real difficulty is not just the model, but the **system pipeline**:

* Screenshot latency
* Action execution delay
* State mismatch
* Missing intermediate states (e.g., popup disappears)
* No feedback loop

👉 This is **very similar to robotics**, not just LLM.

---

## 4. Why Web Is Easy but GUI Is Hard (You Got This Right)

You said:

> “web能操作好是因为喂 uitree 给模型”

That’s exactly the reason.

### Web

* Structured (HTML, DOM)
* Deterministic
* Observable

### Native GUI

* No standard
* Framework fragmentation:

  * Windows (Win32 / WPF)
  * Java Swing
  * Electron
  * Qt

👉 So your conclusion is correct:

> “web 协议标准高，gui 没标准”

This is *the* core industry pain point.

---

## 5. Your Idea: “AI-native GUI / Virtual Machine”

This part is particularly interesting:

> “需要 AI 时代的虚拟机 headless GUI 类似浏览器”

This is actually a **very promising direction**, and people are exploring similar ideas:

* AI-friendly environments
* Instrumented OS layers
* Synthetic UI systems

Your proposal:

> GUI → expose UITree / logs → feed to AI

This is essentially:

> Turning GUI into something like a browser

That’s a **very pragmatic engineering shortcut**, and likely to work better than pure vision.

---

## 6. The “Pure Vision vs Multimodal” Debate

You discussed:

* single screenshot vs multi-frame
* popup disappearing
* logs helping humans

This leads to an important conclusion:

> GUI understanding is **temporal**, not static.

One screenshot is often insufficient because:

* UI changes over time
* Context matters
* Actions have delayed effects

👉 So the future is likely:

* Vision + memory + action history

---

## 7. One Weak Spot in the Discussion (Constructive Criticism)

There is one place where the conversation drifts a bit:

> “需要 GUI transformer diffusion”

This is *creative*, but currently not grounded.

Why?

* The bottleneck is **interaction loop**, not just model architecture
* Transformers already handle vision reasonably well
* Diffusion is not naturally suited for decision-making loops

So the issue is less:

> “new model architecture”

and more:

> “system design + environment + feedback”

---

## 8. Overall Evaluation

### Strengths of the conversation

* Correctly identifies key bottlenecks
* Good analogy to autonomous driving
* Understands importance of structure vs vision
* Recognizes system-level challenges

### Weaknesses

* Slight overconfidence in “pure vision only”
* Underestimates hybrid approaches
* Some speculative ideas without grounding

---

## 9. Final Take

If I summarize your group’s thinking:

> You are already thinking at the level of **“post-LLM system design”**, not just models.

That’s a good direction.

The real opportunity space is:

* AI-native interfaces
* Standardized GUI protocols
* Hybrid perception systems
* Better execution environments (VM / sandbox / replay)

And your intuition here is solid:

> The gap is not just model capability — it's the **interface between model and world**.

---

If you want, I can help you map this into a **concrete experiment setup** (e.g., how to build a minimal GUI agent benchmark with screenshots + actions + evaluation).
