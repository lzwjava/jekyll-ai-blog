---
audio: false
generated: true
image: false
lang: en
layout: post
title: Self-Driving Stalled, LLMs Soared Why
translated: false
type: note
---

Question: Why did self-driving car companies (like Waymo, Pony.ai) fail to achieve the breakthrough they dreamed of in the 2010s, while LLM/NLP companies (OpenAI, Anthropic, Kimi, Gemini) succeeded — and what does this tell us about staying cold-headed and observing truth?

Answer:

## The Self-Driving Dream vs. The LLM Reality — A Lesson in Epistemic Humility

---

### 1. The Hubris of the 2010s Self-Driving Boom

Starting around 2010–2015, a wave of brilliant founders — many with elite credentials (Tsinghua, Stanford PhDs) — poured into self-driving. The vision was genuinely noble: reduce traffic deaths, revolutionize transportation. Waymo, Pony.ai, Cruise, Aurora, Mobileye all attracted billions of dollars and some of the world's smartest people.

The ambition was real. The integrity was real. The talent was real.

**But ambition and talent are not the same as correctly reading reality.**

---

### 2. Why Self-Driving Is Fundamentally Hard to Scale

The article by Wang Yin (王垠, 2016) nailed this prophetically. The core insight:

**The physical world does not forgive approximation.**

- A neural network predicting the next word can be wrong 5% of the time and the text is still readable and useful.
- A self-driving car that misclassifies a wet road surface, a pedestrian in unusual clothing, or a piece of debris — even 0.01% of the time — can kill someone.

Key scaling obstacles:

| Problem | Why It Matters |
|---|---|
| **Watery road surfaces, glare, fog** | Sensor data becomes ambiguous; physics is messy |
| **Long-tail edge cases** | The world has infinite scenarios; training data never covers them all |
| **Real-time 3D perception** | Computationally expensive, latency-sensitive, must be near-perfect |
| **Legal & liability** | One fatal accident = massive regulatory setback |
| **Neural networks are probabilistic** | They output confidence scores, not guarantees — unacceptable for safety-critical systems |

Wang Yin's observation was striking: a human needs roughly 1,000 miles of practice to drive competently. Google's self-driving cars needed millions of miles of data and *still* required human intervention hundreds of times per year — in a small, simple town (Mountain View) under ideal conditions.

This is not a gap that more compute closes easily. It reflects a fundamental difference: **humans have cognitive understanding; machines have statistical pattern matching.**

---

### 3. Why NLP/LLM Scaled So Much Easier

Text has properties that made it a perfect match for modern deep learning:

- **Discrete, structured tokens** — far simpler input space than continuous sensor data from a 3D physical world
- **Error-tolerant** — a slightly wrong word doesn't crash anything
- **Massive, clean training data** — the entire internet is essentially a free corpus
- **Feedback loops are cheap** — you can test millions of text completions instantly; you cannot test millions of driving scenarios safely
- **The Transformer architecture** — happened to fit text beautifully; its attention mechanism aligns naturally with language's sequential, contextual structure

The key asymmetry: **language is a human abstraction, so human-generated data perfectly captures it. The physical world is not a human abstraction — it is indifferent, continuous, and chaotic.**

---

### 4. The Psychological Trap — How Smart People Get Blinded

This is the deeper, more universal lesson your reflection points to.

The founders of self-driving companies had:
- ✅ High IQ
- ✅ Technical depth
- ✅ Real ambition
- ✅ Good intentions

But they also had:
- ❌ Confirmation bias — once you've committed publicly, every small success feels like validation
- ❌ Investor pressure — billions of dollars create a reality distortion field; nobody wants to say "this might take 100 years"
- ❌ Narrative seduction — "self-driving cars" is a *great story*; LLMs helping people write emails is mundane but actually works
- ❌ Misreading what "scaling" means — they assumed more data + more compute = solved, the way ImageNet improvements seemed to suggest

Wang Yin wrote in 2016 that self-driving at human level might take 100–1000 years, or may never happen fully. That was an extreme claim at the time. But 9 years later, Cruise shut down after a fatal accident, Argo AI was dissolved, and even Waymo — the best in class — operates only in select geofenced cities with massive support infrastructure.

---

### 5. The Meta-Lesson: Cold Observation Beats Passionate Vision

Your instinct here is philosophically important. It echoes what good scientists and investors call **falsifiability thinking**:

> "What would have to be true for this to work? And is that actually true?"

The self-driving founders asked: *"Can we build this?"*  
They should have first asked: *"Does the current state of physics, sensors, and AI actually allow this at acceptable cost and safety?"*

The LLM founders (Altman, Amodei, etc.) benefited — perhaps partly by luck — from working in a domain where the answer to that second question was quietly becoming "yes" around 2017–2022.

**Principles that survive the cold light of truth:**

1. **Scalability is domain-specific** — what scales in text does not automatically scale in physical-world perception
2. **Probabilistic systems + zero-tolerance domains = friction** — medicine, aviation, nuclear, and driving all punish "good enough"
3. **Data availability matters enormously** — LLMs had the internet; self-driving had to generate its own data expensively
4. **Ego and capital can sustain illusions for a decade** — but not forever
5. **Calm, dispassionate analysis of "what is actually hard" is rarer and more valuable than enthusiasm**

---

### 6. What This Doesn't Mean

This is not an argument that self-driving is *worthless* or *impossible forever*. Waymo is genuinely impressive in its operational zones. Tesla's FSD has improved. But the timeline fantasies of the 2010s — "fully autonomous by 2020" (Musk, 2016) — were wishful thinking dressed as engineering roadmaps.

The gap between "works 99% of the time in controlled conditions" and "safe enough to deploy everywhere without supervision" is not a 1% gap. It may be the hardest 1% in all of engineering.

---

### Summary

The self-driving story is a reminder that **truth is not moved by ambition, credentials, or funding**. The physics of wet road surfaces doesn't care how good your PhD is. Neural networks remain probabilistic. The physical world remains continuous and chaotic.

Staying cold, calm, and honest about *what is actually hard* — rather than what we wish were true — is one of the rarest and most valuable cognitive skills. The people who built LLMs didn't necessarily have better intentions than the self-driving founders. They just happened to be working in a domain where the underlying truth aligned with their ambitions.

That alignment is not something you manufacture. It's something you *discover* — if you're honest enough to look.

References:

- [王垠：我看自动驾驶技术 — TecHug](https://www.techug.com/post/self-driving-car/)