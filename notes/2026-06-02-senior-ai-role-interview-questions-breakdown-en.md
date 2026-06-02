---
audio: false
generated: true
image: false
lang: en
layout: post
title: Senior AI Role Interview Questions Breakdown
translated: false
type: note
---

Ah — **interview questions** for senior AI/agent/full-stack roles. Yeah, here's what's actually being asked right now:

**Agent & Reasoning (most common)**

1. "Design an autonomous agent system that handles multi-step financial transactions. How do you handle tool failures, hallucinations, and state management?"
   - Probe: tool use, error recovery, prompt engineering at scale
   
2. "You have a task that needs reasoning. When do you use o1/R1 vs a fine-tuned smaller model vs chain-of-thought prompting? What's your decision framework?"
   - Probe: cost/latency trade-offs, when to sacrifice speed for reasoning

3. "Build a multi-agent system where agents coordinate. How do you avoid loops, ensure convergence, and log reasoning?"
   - Probe: system design, debugging invisible LLM behaviors

**Inference & Optimization**

4. "Your LLM API costs are $500k/month. Cut it to $100k without sacrificing quality. Walk me through your approach."
   - Probe: quantization, fine-tuning, model selection, caching, batching
   - Real question at banks/startups

5. "Implement speculative decoding or KV cache quantization. Code it."
   - Probe: actually understand the math, not just theory

6. "You have a 70B model and 12GB GPU memory. How do you run inference?"
   - Probe: LoRA, quantization (4-bit/2-bit), batching strategies

**Training & Fine-tuning**

7. "Walk me through a complete fine-tuning pipeline: data preparation → training → evaluation → deployment. What can go wrong?"
   - Probe: DPO/RLHF, eval metrics, drift detection
   - They want to see if you've actually done this

8. "You have 100k proprietary examples. Should you fine-tune a 7B model or use GPT-4? How do you decide?"
   - Probe: cost analysis, latency requirements, quality thresholds

**System Design (tricky but common)**

9. "Design a real-time AI agent for customer support that learns from interactions. Architecture, data flow, training loop, monitoring."
   - Probe: everything together — agent logic, data pipeline, model updates, observability

10. "How do you evaluate an LLM-powered system? Metrics, benchmarks, user feedback loops?"
    - Probe: beyond BLEU/ROUGE; do you understand business metrics?

**What They DON'T Ask Anymore**

- "Explain attention mechanism" (you should know it; they assume you do)
- "What's RAG?" (basic, boring)
- "Build a simple chatbot" (too junior)

**How to Prepare (your style)**

- **Have a project ready**: Your agents/fine-tuning work. Be able to walk through the code, the trade-offs, what you'd do differently.
- **Know numbers**: Your 1.5B token/year consumption → what did that cost? How did you optimize? This is proof you've operated at scale.
- **Code on the board**: If they ask about quantization or speculative decoding, show actual code (PyTorch/vLLM snippets), not handwaving.
- **Have a "cost reduction" story**: Every bank/startup cares about this. Your H100 fine-tuning vs GPT-4 cost trade-off is gold.
- **Understand failure modes**: What breaks with LLM systems? Hallucinations? Latency spikes? Token limits? Show you've debugged real systems.

**For your specific profile**, emphasize:
- Agent architecture (ww, iclaw, zz — walk them through)
- Fine-tuning on domain data (financial systems are perfect)
- Inference optimization at scale (H100 batching, quantization)
- Cost/latency trade-offs (1.5B tokens → what's your optimization?

They're not asking if you can implement a transformer from scratch. They're asking: **Can you ship AI systems that work, stay cheap, and actually help the business?**

That's your north star for prep.