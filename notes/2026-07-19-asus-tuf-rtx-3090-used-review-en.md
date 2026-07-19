---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS TUF RTX 3090 Used Review
translated: false
type: note
---

Question: How good is this ASUS TUF RTX 3090 24GB second-hand GPU listing?

Answer:

This is actually one of the **better RTX 3090 used listings**, especially for AI/LLM work.

![Image](https://images.openai.com/static-rsc-4/Womafy_aUANL9LTQQXwk1pBydE4WNCQLUR4qSm-bDNbmI-FF2SnjAK1AVRwcg7UT8n1F3NRODhkOyplxl-ALnOjQHa4BRn9ixi2M-vKS49kN0p2zeqSazSJuGqQrvlP75NbyFCq1mquoGqO_nQSuO5fEij_3nyaFFPIPk0VpUJHRErKrPa-v0WzVHq__qDNq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/138Sr2uAC0-4r1FkZ6HjRlHg5Hd44wwVeKlyLlXOfnKAQnhIPFtb5iI3sEV50-qzFEpsGNXHFwzsJgWHRKzVXpRQU3dpXnl2cX5pq2SkFTHssrqNP4FcG3ZnexvQyAdsFSsZLP2kuJboDb2mugRlxlIXJ0UWz3_7u5oMVG-v_KElK5K49HSN5Mpuod0XEpl7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/7dJZNcD8z0KgZv6VEjhKQAsnqjx-wS33y9haeJWFV4gf5OvIMPOcjhk6R_IbiqMtL3ErVKmz1jYdUpWO9C-yvypRq9CnMBmMakI9WkareiYUZ7wwg4Qyfz1fhWfSd6zlXNioU-DD4kp6VYMcyJdrp7w36k5MLyi-6gWlipGTJOXcTf4zm7PHQce0aGODzHIP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/SbHRyoaQ5iAypJfMNRBiCjDEdfuZLLWlJqXdc2pzrFwXL3vopX_n297Bm9lqfS7v_9-O51s2QiXg-vM19dzD10nSI2XIGWnalFF9QzxkuCKsX5nDgtDNQ8dcirP3I6GeyWMdMDrHyXbLoRn2g3alGcyB5Z544OotHBH818AG8vZ2EflDaPKCwR-5ldttGhob?purpose=fullsize)

Specs:

* GPU: ASUS TUF Gaming GeForce RTX 3090 24GB
* VRAM: **24GB GDDR6X** (the main reason to buy it)
* Architecture: Ampere
* Compute capability: 8.6
* Tensor cores: 328
* FP16 Tensor performance: ~142 TFLOPS
* Memory bandwidth: ~936 GB/s

For AI:

| Model workload                | RTX 3090 24GB |
| ----------------------------- | ------------- |
| Llama/Qwen 7B inference       | ✅ Excellent   |
| 14B models quantized          | ✅ Good        |
| 32B Q4 inference              | ✅ Possible    |
| LoRA fine-tuning 7B-14B       | ✅ Very good   |
| Full fine-tuning              | ❌ Too small   |
| GPT-2 760M / nanoGPT training | ✅ Comfortable |

Compared with your RTX 4070:

|                  | RTX 4070                | RTX 3090       |
| ---------------- | ----------------------- | -------------- |
| VRAM             | 12GB                    | **24GB**       |
| Memory bandwidth | 504 GB/s                | **936 GB/s**   |
| FP16 Tensor      | ~60 TFLOPS              | **142 TFLOPS** |
| Power            | 200W                    | 350W           |
| CUDA             | same generation support | same           |

For LLM development, the 3090 is a big jump because **VRAM is the bottleneck**.

---

The seller claims:

> 3dmark测试99.3
> 烤鸡温度70度左右

Good signs:

✅ Stress temperature 70°C is very good for a 3090.
3090s often run:

* GPU core: 75-85°C
* Memory junction: 95-110°C

The missing information:

**Need memory temperature.**

3090 has hot GDDR6X memory on both sides of PCB.

Ask seller:

```
GPU-Z screenshot:
- GPU temperature
- Memory junction temperature
- Hot spot temperature
- ASIC quality
- BIOS version
```

The key number:

* Memory junction < 90°C → excellent
* 90-100°C → normal
* > 105°C → avoid

---

Age:

> 20年的卡

Meaning 2020 card.

So it is ~6 years old.

Risk:

* Fan bearing aging
* Thermal pads drying
* Mining history possible

However ASUS TUF is among the better 3090 designs:

* large heatsink
* good VRM
* better cooling than many blower/reference cards

---

Price determines everything.

Approximate 2026 China used market:

* RTX 3090 normal: ¥2500-3200
* ASUS TUF / STRIX: ¥2800-3500
* suspicious cheap: <¥2200

My valuation:

| Price     | Judgment                       |
| --------- | ------------------------------ |
| <2500 CNY | 🔥 Buy                         |
| 2500-3000 | 👍 Good                        |
| 3000-3500 | OK only if excellent condition |
| >3500     | Not attractive                 |

---

For your use case (LLM training, ROCm experiments, local models):

I would rank:

1. RTX 3090 24GB ⭐⭐⭐⭐⭐
2. RTX 4090 24GB ⭐⭐⭐⭐⭐ (too expensive)
3. RTX 3090 Ti 24GB ⭐⭐⭐⭐
4. RTX 4070 Ti Super 16GB ⭐⭐⭐
5. RX 7900 XT 20GB ⭐⭐⭐ (ROCm advantage but ecosystem weaker)

The 3090's killer feature is simply:

**24GB CUDA VRAM at used-market price.**

For AI engineering, a 3090 often beats a newer 12GB/16GB card because many models simply don't fit.

Before buying, I would ask for:

```
1. GPU-Z full screenshot
2. GPU memory temperature under FurMark/OCCT
3. Run:
   nvidia-smi -q -d MEMORY
4. Any mining history?
5. Original invoice?
```

If the price is around **¥2800-3000**, this is a strong candidate.
