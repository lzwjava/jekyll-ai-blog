---
audio: false
generated: true
image: false
lang: en
layout: post
title: ASUS GTX 970 Dragon Knight Overview
translated: false
type: note
---

Question: What is this ASUS GTX 970 4GB "Dragon Knight" GPU listing?

Answer:

NVIDIA GeForce GTX 970 is an older gaming GPU released in **2014** based on NVIDIA's **Maxwell (GM204)** architecture.

The listing:

> 华硕 GTX970-4G 龙骑士显卡
> 接口OK，PCIE通道OK
> 已经清灰换好硅脂了。
> 到手直接上机。

means:

* **ASUS GTX970-4G Dragon Knight**

  * ASUS custom cooler version ("龙骑士" = Dragon Knight series)
  * 4GB GDDR5 VRAM
* **接口 OK**

  * Display outputs tested
* **PCIe 通道 OK**

  * PCIe connection works, GPU recognized normally
* **清灰换硅脂**

  * Seller cleaned dust and replaced thermal paste
* **直接上机**

  * Ready to install

![Image](https://images.openai.com/static-rsc-4/Ox_IT7h4ToFzRx3fj0yKMJEKgoADEtWniqSysaVY-qBhrCGA-b7tuoCqlZked7_AN5noGkRM-3qUiEKy7QRgq2GemLoNZyuXd3weOub0aojcRQME862A1ZSs8B0dRxDFtGlTe3MFuW2PZwZ1zArM6waxFtKOFqF9ntMHmSxyLCLOzIHzpsve_b7JRl_00L__?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eGIdiXYnCAgdczOx3Scp9X-NNNzyCIYc6I22d-8PhNR7YwO6Ggrq7OEmXoeRMNICUiRRw7fRfuOTjAfQLFeszAUYkPIdnaaUeIKXiIqGUMrz9arXOMrQclgDhWIkgqCsuzAGjfBkmLWFRSuZUgd0E9T2n0hRmq9h-pe2Jy_jgL3DNfunsWPcFt1LYTjYhyaG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3WGc849jBYtGqOOepegYK4J5Cdu-stRSN5XAfE5h65PouIms2wCQHg7puoEtzsx9K_xRa9EA3hawTGnh55EolI4bPCzvGPNOy0anc104qgeTEfSLmge98kRqX5xAi9kbd23KXMT53iAl-fcyORSdwRidMKoKd64LgExh_E48qNKO3fB9XSfnGz9NyPt85RB-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/f2xBJ7-olnZgImT4etVSbQEM5kiPGVDxgo3yxdIob9VAoFgs9EsFOYH3YjPQEBP38Hk9Vp9vwzkDK3GByrz5G0Rk46N2ntej7UWnbpFoby3Tgk_aJCmUdD64Smn-iGbedia2Ox2taGBoOjEfCfq1VXztTYUWL4eCxzUom_h4ot8OiGAuc47forcD8W7s_XdQ?purpose=fullsize)

## Specs

|                 | GTX 970                                                                    |
| --------------- | -------------------------------------------------------------------------- |
| Architecture    | Maxwell GM204                                                              |
| CUDA cores      | 1664                                                                       |
| VRAM            | 4GB GDDR5                                                                  |
| Memory bus      | 256-bit (effectively 224-bit usable due to GTX 970 memory partition issue) |
| PCIe            | 3.0 x16                                                                    |
| Power           | ~145W                                                                      |
| Recommended PSU | 500W                                                                       |
| Release         | 2014                                                                       |

## AI / LLM usage

For your AI experiments, this card is basically not useful.

Reasons:

1. **Only 4GB VRAM**

   * Cannot run meaningful modern LLM inference.
   * Even tiny models need careful quantization.

2. **No Tensor Cores**

   * Maxwell has CUDA cores only.
   * No FP16 acceleration like RTX cards.

3. **Old CUDA support**

   * Modern PyTorch wheels usually target newer NVIDIA architectures.
   * You will fight compatibility issues.

Compared with your RTX 4070:

|              | GTX 970 | RTX 4070     |
| ------------ | ------- | ------------ |
| Architecture | Maxwell | Ada Lovelace |
| VRAM         | 4GB     | 12GB         |
| CUDA cores   | 1664    | 5888         |
| Tensor cores | ❌       | ✅ 4th gen    |
| FP16         | weak    | very strong  |
| LLM          | no      | yes          |

## Gaming today

Still okay for:

* 1080p esports:

  * League of Legends
  * CS2 (low settings)
  * Valorant
* Older AAA games:

  * GTA V
  * Witcher 3 (old version)

Not good for:

* Cyberpunk
* New AAA games
* Ray tracing

## Price judgment (2026)

On second-hand markets:

* Around **200–400 CNY**: reasonable
* Above **500 CNY**: not attractive

For a cheap desktop GPU it is okay, but for an AI workstation I would skip it.

Your previous GPU direction (RTX 3060 12GB / RTX 3090 / multiple RTX cards) makes much more sense because VRAM is the limiting resource for LLM work. A GTX 970 is basically a display card today, not a compute card.
