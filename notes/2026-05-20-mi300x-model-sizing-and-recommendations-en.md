---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Model Sizing and Recommendations
translated: false
type: note
---

Great question — that MI300X is a beast. Let me give you concrete numbers.

First, the practical math for llama.cpp GGUF on your ~192 GB VRAM:

| Quant | GB per 100B params | Max model size (192GB) |
|---|---|---|
| Q2_K | ~32 GB | ~600B |
| Q3_K_M | ~45 GB | ~420B |
| Q4_K_M | ~57 GB | ~330B |
| Q5_K_M | ~70 GB | ~270B |
| Q6_K | ~82 GB | ~230B |
| Q8_0 | ~102 GB | ~185B |

Plus KV cache eats into that for long contexts — count ~2 GB per 100K tokens of context.

**Sensible ladder to climb** (best GGUF format for each):

**1. Next step up — Llama 3.3 70B Q4_K_M (~40 GB)**
Fast, smart, you'll notice the jump from 0.5B immediately. Feels like going from a bicycle to a sports car.

**2. Comfort zone — Qwen 2.5 110B Q4_K_M (~65 GB)**
Leaves plenty of headroom for context. Chinese + English, very strong. This is the sweet spot for your card.

**3. Heavy hitter — DeepSeek-V2 236B Q3_K_M (~106 GB)**
This is where the MI300X starts flexing. 236B MoE (only 37B active per token, so inference stays fast). Fits comfortably with room for 50K+ tokens of context.

**4. Max out — DeepSeek-V3 671B Q2_K (~150 GB)**
The biggest that practically fits. 671B MoE, ~37B active per token, so tokens/s stays reasonable despite the size. You'd have ~40 GB left for KV cache context. This is the "pushing it to the limit" run.

**5. Pure overkill — Llama 3.1 405B Q3_K_M (~182 GB)**
Only ~10 GB left for context — tight but it loads. You'd get a few thousand tokens of context max.

---

**My recommendation**: Try **Qwen 2.5 72B Q4_K_M** first as a natural next step, then jump to **DeepSeek-V2 236B Q3_K_M** to really feel what that 192 GB buys you. The 72B will run at 30-50 t/s, and the DeepSeek-V2 MoE will surprise you with how fast it is for its size thanks to sparse activation.

Want me to download and run one of these and see the actual throughput numbers?
