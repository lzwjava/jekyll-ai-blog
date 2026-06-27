---
audio: false
generated: true
image: false
lang: en
layout: post
title: Contractor Can't Self-Assign Principal Role
translated: false
type: note
---

Question: After 16 months on a Java + Angular full-stack contract, I'm no longer willing to take routine tasks and have a large backlog. Can I tell the team to let them handle most work and only escalate very difficult tasks to me, framing myself as a principal-level engineer? I'm only excited by the Python/DuckDB Excel-gap tool with the Principal Engineer. I want to move toward AI/LLM inference and model training. How do you think about this?

Answer:

Let me be direct, because the soft version doesn't serve you.

**The "only give me hard tasks" move won't work the way you want.**

You're a contractor, not a principal engineer in the org chart. The title "principal engineer" is something the company confers based on scope, ownership, and political standing — you can't self-assign it by declining tasks. If you tell a team "let them do it, only give me the very difficult tasks," what they hear from a contractor is "I've checked out." That gets your contract not renewed, not your scope elevated. The leverage to dictate task selection comes from being staff/principal *and* being load-bearing on something they can't replace. You're neither here, by your own description.

So no — don't say that. It reads as disengagement, and it's a fast path to a bad reference and an early exit on their terms instead of yours.

**But your underlying instinct is correct.** The bank job is, per your own playbook, a tax to pay for salary plus a learning ground. You've extracted a lot: 1,100 guides, 400 scripts, the AIPlayer contribution award, top 6% Copilot usage, real banking domain knowledge. Sixteen months of full-stack Java/Angular is a diminishing-returns curve now. The notes and scripts you generate per month are going down in novelty because you've already mined the seam.

The question isn't "how do I do less here" — it's "what's the exit path, and what am I exiting *to*."

**The hard truth about the AI/LLM inference + training goal:** wanting it isn't the same as being hireable for it. What you've done so far — nanoGPT, GPT-2 760M, fine-tuning on ~5M tokens, inference with Qwen, ROCm/FlashAttention familiarity — is genuinely strong *hobbyist-to-serious-practitioner* territory. It's not yet the profile that gets you hired onto an inference or training team at a place doing it for real. Those roles want: production inference optimization (paged attention, continuous batching, quantization that holds accuracy, kernel-level work), or training-infra experience (distributed training, FSDP/DeepSpeed, dealing with loss spikes at scale, data pipelines). The gap between "I trained GPT-2 760M on an MI300X" and "I can own inference latency for a serving system" is the gap you need to close before the move pays off.

**So here's how I'd actually sequence it, grounded in your situation (900K mortgage, family wants security, contractor with no promotion path):**

1. **Don't quit into a vacuum. Line up the next thing first.** You have a mortgage and two daughters. The move out should be *into* a role or contract that is AI-inference/training-adjacent, not into unemployment-while-I-figure-it-out. Your family's resistance is rational given the numbers.

2. **Use the remaining bank time to close the credibility gap, not to coast.** The Principal Engineer Excel/DuckDB project is your best asset there — it's the one piece of bank work that's Python-first, AI-adjacent, and gives you a senior collaborator who can be a reference. Lean *into* that one, not away from everything. A principal engineer vouching for you is worth more than any of your 1,100 guides.

3. **Build one inference artifact that's undeniably real.** Not another fine-tune. Something like: take an open model, serve it with vLLM or SGLang, measure and optimize throughput/latency, write up the kernel-level or batching-level wins with numbers. Or implement paged attention / a sampling optimization from scratch and benchmark it. One deep, benchmarked, public artifact beats 300 more scripts. That's the thing that converts "enthusiast" into "hireable for inference."

4. **The 1000 notes / 300 scripts are sunk leverage — stop counting them as progress.** They were the right move months ago. Now they're a comfort metric. More notes ≠ closer to the AI job. A single benchmarked vLLM optimization or a distributed-training run that survives a loss spike moves you further than 200 more notes.

On the actual exciting work — yes, inference and training are where the frontier is and where you want to be. The honest read: you're closer than most, but the last mile (production-grade inference, distributed training at non-toy scale) is the part that's missing, and it's exactly the part the bank can't teach you. That's the real argument for moving — not that the Java tasks are boring, but that they no longer build the specific skill you're trying to compound.

Want me to spec out a concrete 8-week inference project (vLLM serving + benchmarked optimization, or a from-scratch paged-attention implementation) that would be the single strongest portfolio piece for an inference/training role? That's the highest-leverage thing I could hand you right now.
