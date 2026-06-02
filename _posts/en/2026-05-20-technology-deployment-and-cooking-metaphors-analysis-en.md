---
audio: false
generated: true
image: false
lang: en
layout: post
title: Technology Deployment and Cooking Metaphors Analysis
translated: false
type: note
---

**Question:** Analyzing a reflection on AMD MI300X inference deployment for DeepSeek v4, the metaphor of cooking congee/porridge as a learning journey, and the practical cooking tip about vegetables — is the cooking advice correct? Give deeper analysis.

---

**Answer:**

## The Technical Layer: AMD MI300X + DeepSeek

This is actually a significant deployment milestone worth unpacking:

**Why MI300X for DeepSeek v4 is non-trivial:**

- MI300X has **192GB HBM3** per card — the largest memory footprint of any GPU/APU. DeepSeek V3/V4 at full precision (671B MoE) needs ~1.3TB, so you still need a multi-node setup, but MI300X reduces node count significantly vs A100s
- AMD ROCm has historically lagged NVIDIA CUDA for inference frameworks. Getting vLLM/SGLang running well on MI300X required real engineering effort — this is not plug-and-play
- **DeepSeek's MoE architecture** (only ~37B active params per token from 671B total) is actually friendlier to MI300X's memory bandwidth characteristics than dense models
- AMD Developer Cloud giving access is rare — most serious GPU clouds (Lambda, CoreWeave, RunPod) are NVIDIA-first

The "算力资源稀缺" (compute is scarce) point is real. H100/H200 allocation is dominated by hyperscalers. AMD MI300X is one of the few paths to serious inference capacity outside that lock-in.

---

## The Congee Metaphor — Actually Deep

The progression described:

```
肉块 + 酸菜          →  basic functional setup
蔬菜 + 枸杞 + 卷章   →  richer, more complete system
```

Maps well onto how LLM deployment actually evolves:

```
Week 1:  model loads, generates tokens        # 肉块酸菜
Week 3:  quantization, batching, streaming    # 加蔬菜
Week 6:  speculative decoding, KV cache opt   # 枸杞卷章
```

"顺其自然" (let things happen naturally) is the right instinct for vibe coding — ship fast, iterate, don't over-engineer before you have signal.

---

## The Cooking Advice — Is It Correct?

> 蔬菜得中间放入 要不会煮烂
> 其他都可以直接从冰箱放入
> 粽子也可以不去皮

**Breaking it down:**

### ✅ Vegetables added mid-cook — Correct

Leafy/tender vegetables (菠菜, 卷心菜, 枸杞) have low heat tolerance. In a slow-simmered congee:

- Full-duration cooking (45-60 min): texture completely lost, nutrients (especially water-soluble vitamins B/C) severely degraded
- **Add at T-5 to T-10 min**: texture preserved, color retained, nutrients mostly intact
- Root vegetables (carrots, daikon) are the exception — they can go in early

The heat curve matters: congee typically simmers at ~95°C for a long time. Tender greens at that temp for 60 min = mush.

### ✅ Other ingredients straight from fridge — Mostly correct

Meat,骨头, preserved vegetables (酸菜), tofu — these are robust to temperature differentials and long cooking times. Going from fridge directly into simmering pot is fine:

- Dense proteins need the full cook time anyway
- The cold input slightly drops pot temp but recovers quickly at low-simmer volumes

One caveat: **frozen meat** directly in can affect texture slightly (ice crystal damage) — thawing first gives better mouthfeel, but for congee where meat often shreds anyway, it doesn't matter much.

### ⚠️ 粽子不去皮 — Needs clarification

Depends what "粽子" means here in context:

- If **荸荠 (water chestnut)** — 去皮 is strongly recommended, the skin is fibrous and can have pesticide/soil residue
- If actual **粽子 (sticky rice dumpling wrapped in bamboo leaves)** — you absolutely need to remove the bamboo leaf wrapping before eating, but in a congee/soup context you'd unwrap and add the sticky rice content directly
- If **玉米 (corn on the cob)** — skin/husk removal is standard

The advice is probably context-correct for whatever specific ingredient is in that particular pot — but "粽子不去皮" as a general rule needs the ingredient specified to be evaluated precisely.

---

## Meta-point: Community Learning Compounds

"感谢和各位群友的交流互动" — the group chat / community interaction model is underrated for AI engineering. The people figuring out MI300X + DeepSeek deployment in real-time are in WeChat groups and Discord servers, not writing blog posts yet. Being in those loops is a genuine edge — you get working configs weeks before any tutorial exists.

The congee analogy holds: you're adding ingredients as you discover them, not following a fixed recipe. That's the right way to operate at the frontier.
