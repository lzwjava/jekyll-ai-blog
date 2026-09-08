---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M60 Trio at $15 Each
translated: false
type: note
---

Question: Is 320 CNY for a bundle of 3 NVIDIA Tesla M60 cards a good deal?

Answer:

Yes, **3 cards for 320 CNY (~$44 USD)** is an exceptionally low price — roughly **~107 CNY ($15) per card**. That's basically scrap/salvage pricing.

**Why so cheap per card?**

| Reason | Detail |
| --- | --- |
| Bulk lot pricing | Sellers want to move inventory fast, bundle = discount |
| Unknown condition | "成色如图" (condition as shown in photos) — could have wear, fan issues, thermal paste dried out |
| No warranty | Private second-hand sale, zero recourse if DOA |
| High power draw risk | Each M60 draws ~300W — 3 cards = **~900W** total, needs serious PSU |
| Datacenter pulls | Often missing brackets, dusty, fans degraded |

**What 3 cards could theoretically give you:**

| Metric | Per Card | 3 Cards Total |
| --- | --- | --- |
| VRAM | 16GB | **48GB total** |
| FP32 | ~7.4 TFLOPS | ~22 TFLOPS |
| Power Draw | ~300W | ~900W |

**48GB of VRAM across 3 cards** is actually attractive for running large LLMs (e.g. LLaMA 3 70B in multi-GPU inference), **but** the M60 has no NVLink — inter-GPU communication is over PCIe, which creates a serious bandwidth bottleneck for multi-GPU workloads.

**Key risks to check before buying:**

- Are all 3 fans working? (replacement blower fans for M60 are hard to find)
- Do all 3 POST and show up in `nvidia-smi`?
- What PSU does the seller include — is it rated for 900W+ sustained load?
- Any burnt smell, bent pins, or physical damage in the photos?

**Verdict:** At ~$15/card it's worth it **if** you treat it as an experiment or inference box — not a training rig. Worst case you lose $44. Best case you get 48GB VRAM for almost nothing.

---

References:

- [NVIDIA Tesla M60 Specs — TechPowerUp](https://www.techpowerup.com/gpu-specs/tesla-m60.c2760)
- [Running LLMs on Old Tesla GPUs — Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/used_tesla_gpus)
