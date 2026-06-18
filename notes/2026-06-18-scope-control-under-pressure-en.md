---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scope Control Under Pressure
translated: false
type: note
---

**Question:** I failed some AI engineer interviews recently. The feedback was that I couldn't stay focused on one question, making it hard for interviewers to evaluate my skills. A friend advised me to listen more before reacting. What's your take?

**Answer:**

Your friend is right, and the feedback is pointing at a specific failure mode that's very common in engineers who think fast and build fast — which you clearly do.

Here's the honest diagnosis:

**The real problem: you're pattern-matching before the question is finished.**

With 12 years of experience and 1B tokens/month of LLM usage, your brain has seen most problems before. When an interviewer starts a question, you recognize the shape of it early and start constructing an answer — sometimes before they've finished framing it. This causes you to answer the question you *predicted* rather than the question they *asked*. The interviewer then either has to redirect you (losing time, losing confidence in you) or just gets a misaligned answer.

In interviews, this reads as: scattered, hard to evaluate, possibly overconfident.

**What "listen more" actually means technically:**

1. **Let them finish the full question before you begin processing.** Full stop. Even if you know where it's going. Let them land the plane.

2. **Repeat the question back in one sentence before answering.** "So you're asking me to design X with constraint Y, right?" This forces you to compress what you heard, confirms alignment, and buys 5 seconds of structured thinking time.

3. **Answer the exact question, then stop.** Don't free-associate into adjacent topics. If they asked about KV cache eviction, don't drift into MoE routing. Answer the specific question, stop, let them follow up.

4. **Treat the interview like a debugging session, not a demo.** You're not showing everything you know — you're helping them probe one specific thing at a time. Resist the urge to show range.

**Why this is especially hard for you:**

You build CLI agents, train models, write 400 blog posts. Your natural mode is expansive and generative. That's a strength in building — you connect dots across domains fast. But interviews are *constrained* problem solving, not open-ended exploration. The evaluation requires them to isolate one signal at a time. If you give them five signals mixed together, they can't score any of them cleanly.

**Practical drill before next interview:**

Practice with a timer. Ask someone (or use Claude) to give you a technical question. Enforce this protocol:
- 0–5s: silence, absorb
- 5–10s: one sentence back to confirm the question
- 10s–N: answer only what was asked
- After answer: stop and wait

Do this 10 times. You'll feel the urge to expand — that's the thing to suppress.

The underlying skill is not "listening" in the soft sense. It's **scope control under pressure** — which is also a real engineering skill that matters beyond interviews.
