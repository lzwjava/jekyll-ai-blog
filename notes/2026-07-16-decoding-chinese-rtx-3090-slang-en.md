---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding Chinese RTX 3090 Slang
translated: false
type: note
---

Question: How to understand “目前3090只有猛禽 雕 魔龙” in the GPU second-hand market?

Answer:

This is Chinese GPU seller slang. It means:

> “Currently, for RTX 3090, only the ROG Strix, (某个‘雕’ series), and Gaming X Trio/魔龙 series are available.”

Breaking it down:

* **3090** → NVIDIA GeForce RTX 3090 24GB.

* **猛禽** → usually refers to ASUS ROG Strix GeForce RTX 3090.

  * “ROG 猛禽” is ASUS's high-end gaming model.
  * Big cooler, good PCB, high power limit.
  * Usually expensive in the used market.

* **雕** → usually refers to Gigabyte AORUS GeForce RTX 3090 XTREME (“大雕” / AORUS).

  * Gigabyte AORUS cards are nicknamed “雕” because of the eagle logo.
  * “大雕” = AORUS XTREME flagship.
  * “小雕” = AORUS MASTER sometimes.

* **魔龙** → usually refers to MSI GeForce RTX 3090 GAMING X TRIO (Chinese nickname “魔龙”).

  * MSI Gaming X Trio series.
  * Good cooler and relatively reliable PCB.

So the seller is basically saying:

```
RTX 3090 available models:

ASUS ROG Strix 3090     = 猛禽
Gigabyte AORUS 3090     = 雕
MSI Gaming X Trio 3090  = 魔龙
```

These are all **large triple-fan AIB cards**, not NVIDIA Founders Edition or cheaper models.

For AI/LLM workloads, the differences are much smaller than gamers care about:

| Model                  | VRAM        | AI performance | Cooling   | Typical used value |
| ---------------------- | ----------- | -------------- | --------- | ------------------ |
| ROG Strix 3090         | 24GB GDDR6X | same           | excellent | highest            |
| AORUS 3090             | 24GB GDDR6X | same           | excellent | high               |
| MSI Gaming X Trio 3090 | 24GB GDDR6X | same           | good      | high               |
| Cheap 3090 models      | 24GB GDDR6X | same           | varies    | cheaper            |

For LLM inference/fine-tuning, the important things are:

1. **24GB VRAM**
2. **memory temperature**
3. **power stability**
4. **whether it was used for mining**

A ¥5000–6000 used RTX 3090 with a good cooler is often more valuable for AI than paying extra for the “猛禽/雕/魔龙” branding. The GPU chip and VRAM capacity are identical.

References:

* [ASUS ROG Graphics Cards](https://rog.asus.com/graphics-cards/?utm_source=chatgpt.com)
* [GIGABYTE AORUS Graphics Cards](https://www.gigabyte.com/Graphics-Card/AORUS-Graphics-Cards?utm_source=chatgpt.com)
* [MSI Graphics Cards](https://www.msi.com/Graphics-Cards?utm_source=chatgpt.com)
