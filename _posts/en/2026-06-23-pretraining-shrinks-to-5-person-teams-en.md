---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pretraining Shrinks to 5-Person Teams
translated: false
type: note
---

**Question:** Vlad Feinberg (Google DeepMind Gemini pretraining lead) said on a podcast that 5 people can handle Gemini 2.0 pretraining. What's the signal here about the future of LLM engineers vs agent engineers? Also, is the "40-day no-sleep" grind culture at CSDN a myth?

**Answer:**

Your read is mostly right, but let me sharpen it.

**The 5-person pretraining signal**

This is real and the trend is clear: pretraining is becoming *infrastructure*, not research. The bottleneck shifts from "how many ML engineers" to "how much compute and how good your data pipeline is." A small, extremely senior team (think: Karpathy-tier systems thinkers who can read CUDA, write XLA, and debug distributed training at 10k+ GPU scale) handles the core loop. Everyone else is overhead.

What that means practically:

- **Pretraining engineers**: fewer seats, but insanely high bar. You need to know the full stack — compiler, memory, distributed comms (NCCL/RCCL), loss curves, checkpoint strategy. Vlad getting a bonus from Jeff Dean for *unblocking the stack* rather than publishing is the signal — execution beats papers at this layer.
- **Fine-tuning / RLHF / post-training engineers**: slightly more seats, still shrinking as tooling matures (LoRA, GRPO, DPO are commoditizing).
- **Agent engineers**: yes, will be everywhere. But "everywhere" doesn't mean "low value" yet — it means the floor rises. Basic tool-use chains are already commoditized (LangChain tourists). The real edge is eval, reliability, and knowing when the LLM is hallucinating mid-chain.

Your instinct — *大模型工程师满大街, agent工程师满大街* — I'd split it:

| Role | Saturation timeline | What survives commoditization |
|---|---|---|
| Pretraining core | Already rare, stays rare | Systems + math depth |
| Fine-tuning | 2-3 years | Dataset curation taste |
| Basic agent (LangChain glue) | Already commoditized | Nothing |
| Agent infra (eval, memory, reliability) | 3-5 years | Distributed systems thinking |
| Model internals (attention, sampling, KV cache) | Long runway | First-principles ML |

Your path of training GPT-2 from scratch, reading nanoGPT, running on MI300X — that's building the foundation that *doesn't* get commoditized. The people who will matter in 5 years are the ones who can debug a broken attention pattern at the CUDA level, not just call `openai.chat.completions.create()`.

**On the CSDN "40-day no-sleep" take**

You're right to push back. Two-shift rotation is the actual story at most serious labs — not mythologized suffering. The Transformer paper team at Google wasn't sleeping under desks; they had sustained deep focus with good infrastructure. Vlad's Bard unblocking story is similar: it was dirty, unglamorous *engineering* work (OOM errors, TPU quirks), not heroic all-nighters.

CSDN-style content optimizes for engagement from people who haven't shipped at that scale. The real signal from Vlad's story is the opposite of grind culture: **5 disciplined engineers with the right mental model beat 50 caffeinated ones without it.**

The compounding move for you: keep the model internals depth (you're doing this), and build one production agent system end-to-end with real eval harness — that's the combination that's still rare.
