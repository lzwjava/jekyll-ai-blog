---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sparse Mixture-of-Experts AI Model
translated: false
type: note
---

**Question:** What does "A3B" mean in Qwen3.6-35B-A3B? Does "A" stand for "activation"?

**Answer:**

Yes. The "A3B" means only 3 billion parameters activate per forward pass, even though the full weight file holds 35 billion—this is a sparse Mixture-of-Experts design.

**Architecture breakdown:**

Qwen3.6-35B-A3B uses a Gated DeltaNet MoE architecture with 256 experts, where 8 experts are routed per token plus 1 shared expert. A router network learns which expert sub-networks to activate for each token; the remaining 247 stay dormant. The sparsity ratio is roughly 12:1 (3B active out of 35B total)—among the most aggressive in any publicly released model.

**Why this matters for you:**

The model delivers frontier-style coding and agent performance with only 3B active parameters, making it attractive for deployment because it reduces inference cost while behaving like a much larger model on coding and tool-heavy tasks. On SWE-bench Verified, Qwen3.6-35B-A3B scores 73.4% while Gemma 4-31B (a dense 31B model) scores 52.0%.

It supports a 262K token native context window (extensible to 1M via YaRN) and includes integrated thinking mode with reasoning traces preserved across multi-turn conversations. Available as `qwen3.6-flash` on Alibaba Cloud API or open-source on HuggingFace under Apache 2.0.

Given your MI300X setup and interest in MoE architectures—this is worth testing. The sparsity pattern and gated attention mixing (Gated DeltaNet hybrid linear + gated attention) is closer to what you'd see in DeepSeek v4-style architectures than typical dense transformers.

---

**References:**

- [Qwen3.6-35B-A3B: The Tiny-Active Open Model](https://medium.com/data-science-in-your-pocket/qwen3-6-35b-a3b-the-tiny-active-open-model-that-thinks-codes-and-agents-like-a-much-bigger-one-486d535e372e)
- [Qwen3.6-35B-A3B: The Small Model That Codes Like a Giant](https://www.labellerr.com/blog/qwen3-6-35b-a3b-open-source-ai-model/)
- [vLLM Recipes - Qwen3.6-35B-A3B](https://recipes.vllm.ai/Qwen/Qwen3.6-35B-A3B)
