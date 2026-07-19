---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ASUS GTX 970 龙骑士 概述
translated: true
type: note
---

问题：这个 ASUS GTX 970 4GB "Dragon Knight" GPU 列表是什么？

答案：

NVIDIA GeForce GTX 970 是一款较旧的游戏显卡，于 **2014** 年发布，基于 NVIDIA 的 **Maxwell (GM204)** 架构。

这个列表：

> 华硕 GTX970-4G 龙骑士显卡
> 接口OK，PCIE通道OK
> 已经清灰换好硅脂了。
> 到手直接上机。

含义：

* **ASUS GTX970-4G Dragon Knight**
  * ASUS 定制散热版本（"龙骑士" = Dragon Knight 系列）
  * 4GB GDDR5 显存
* **接口 OK**
  * 显示输出接口已测试正常
* **PCIe 通道 OK**
  * PCIe 连接正常，显卡能被正常识别
* **清灰换硅脂**
  * 卖家已清灰并更换了硅脂
* **直接上机**
  * 可直接上机使用

![Image](https://images.openai.com/static-rsc-4/Ox_IT7h4ToFzRx3fj0yKMJEKgoADEtWniqSysaVY-qBhrCGA-b7tuoCqlZked7_AN5noGkRM-3qUiEKy7QRgq2GemLoNZyuXd3weOub0aojcRQME862A1ZSs8B0dRxDFtGlTe3MFuW2PZwZ1zArM6waxFtKOFqF9ntMHmSxyLCLOzIHzpsve_b7JRl_00L__?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eGIdiXYnCAgdczOx3Scp9X-NNNzyCIYc6I22d-8PhNR7YwO6Ggrq7OEmXoeRMNICUiRRw7fRfuOTjAfQLFeszAUYkPIdnaaUeIKXiIqGUMrz9arXOMrQclgDhWIkgqCsuzAGjfBkmLWFRSuZUgd0E9T2n0hRmq9h-pe2Jy_jgL3DNfunsWPcFt1LYTjYhyaG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3WGc849jBYtGqOOepegYK4J5Cdu-stRSN5XAfE5h65PouIms2wCQHg7puoEtzsx9K_xRa9EA3hawTGnh55EolI4bPCzvGPNOy0anc104qgeTEfSLmge98kRqX5xAi9kbd23KXMT53iAl-fcyORSdwRidMKoKd64LgExh_E48qNKO3fB9XSfnGz9NyPt85RB-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/f2xBJ7-olnZgImT4etVSbQEM5kiPGVDxgo3yxdIob9VAoFgs9EsFOYH3YjPQEBP38Hk9Vp9vwzkDK3GByrz5G0Rk46N2ntej7UWnbpFoby3Tgk_aJCmUdD64Smn-iGbedia2Ox2taGBoOjEfCfq1VXztTYUWL4eCxzUom_h4ot8OiGAuc47forcD8W7s_XdQ?purpose=fullsize)

## 规格

|                 | GTX 970                                                                    |
| --------------- | -------------------------------------------------------------------------- |
| Architecture    | Maxwell GM204                                                              |
| CUDA cores      | 1664                                                                       |
| VRAM            | 4GB GDDR5                                                                  |
| Memory bus      | 256-bit（实际可用 224-bit，因 GTX 970 显存分区问题）                        |
| PCIe            | 3.0 x16                                                                    |
| Power           | ~145W                                                                      |
| Recommended PSU | 500W                                                                       |
| Release         | 2014                                                                       |

## AI / LLM 用途

对于你的 AI 实验来说，这张显卡基本没有用处。

原因：

1. **仅有 4GB VRAM**

   * 无法运行有意义的现代 LLM 推理。
   * 即使是小型模型也需要仔细的量化。

2. **没有 Tensor Cores**

   * Maxwell 仅有 CUDA 核心。
   * 没有像 RTX 显卡那样的 FP16 加速。

3. **旧版 CUDA 支持**

   * 现代 PyTorch 版本通常针对较新的 NVIDIA 架构。
   * 你会遇到兼容性问题。

与你的 RTX 4070 对比：

|              | GTX 970 | RTX 4070     |
| ------------ | ------- | ------------ |
| Architecture | Maxwell | Ada Lovelace |
| VRAM         | 4GB     | 12GB         |
| CUDA cores   | 1664    | 5888         |
| Tensor cores | ❌       | ✅ 第四代     |
| FP16         | 弱      | 非常强        |
| LLM          | 否      | 是           |

## 当前游戏性能

仍然可以用于：

* 1080p 电竞游戏：
  * League of Legends
  * CS2（低画质）
  * Valorant
* 较旧的 3A 游戏：
  * GTA V
  * Witcher 3（旧版本）

不适用于：

* Cyberpunk
* 新的 3A 游戏
* Ray tracing

## 价格判断（2026）

在二手市场上：

* 大约 **200–400 元人民币**：合理
* 超过 **500 元人民币**：不具吸引力

作为一张廉价的桌面显卡，它还行，但如果是用于 AI 工作站，我建议跳过它。

你之前的 GPU 方向（RTX 3060 12GB / RTX 3090 / 多张 RTX 显卡）要合理得多，因为 VRAM 是 LLM 工作的关键限制资源。GTX 970 现在基本上只是一块显示卡，而不是计算卡。