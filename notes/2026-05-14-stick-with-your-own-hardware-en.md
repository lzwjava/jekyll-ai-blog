---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stick with Your Own Hardware
translated: false
type: note
---

Question: What do you think about trying to borrow an A6000 Pro via Tailscale for training GPT-2 XL or GPT-3, versus just using my RTX 4070 for experiments?

Answer:

It sounds like you’ve already thought it through quite reasonably. A few points to consider:

1. **Practicality of borrowing via Tailscale:**

   * Technically, Tailscale can let you access a remote machine as if it’s on your local network, but sharing GPU access remotely comes with latency, bandwidth, and setup complexity.
   * You’d also need the owner to keep the machine available, potentially with elevated permissions, which is risky for both parties.
   * Long-term or heavy experiments could interfere with their work or exams, as you already noted.

2. **Using your RTX 4070:**

   * For GPT-2 XL, a 4070 is capable enough for many experiments, especially if you use techniques like gradient accumulation, mixed precision, or model parallelism.
   * GPT-3 full-scale training is practically infeasible on a single 4070, but small-scale experiments, fine-tuning, or training distilled/smaller variants still gives you meaningful insights.
   * As you said, training GPT-3 on an A6000 Pro might be more about bragging rights than real value unless you’re working at scale.

3. **Alternative paths:**

   * Consider cloud-based GPU instances with hourly billing. Sometimes a short burst on a powerful GPU (like A6000/H100) can let you test ideas without managing remote access through Tailscale.
   * Smaller models or modular experiments can actually give more practical knowledge than just seeing “full GPT-3 trained” on a massive card.

**Summary:** Stick with your 4070 for hands-on experiments. It’s safer, flexible, and still very capable. Borrowing someone else’s A6000 Pro is possible but has logistical and ethical complications, and the value might not justify the effort. Focus on clever experimentation rather than raw hardware.

You can treat the A6000 goal more like a milestone to aspire to rather than a necessity right now—it’s the learning that counts.
