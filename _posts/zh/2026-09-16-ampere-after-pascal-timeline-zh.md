---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 帕斯卡之后的安培时间线
translated: true
type: note
---

**问题：** 在 NVIDIA 的 GPU 架构时间线中，Ampere 是否排在 Pascal 之前？

**答案：** 不，恰恰相反。Pascal（2016 年）首先问世，随后是 Volta（2017 年）、Turing（2018 年），然后才是 Ampere（2020 年）。

以下是完整的现代产品线顺序：

| 年份 | 架构 | 代表性 GPU |
|------|-------------|--------------|
| 2016 | **Pascal** | GTX 10 系列、Tesla P100 |
| 2017 | **Volta** | Tesla V100 |
| 2018 | **Turing** | RTX 20 系列、T4 |
| 2020 | **Ampere** | RTX 30 系列、A100 |
| 2022 | **Hopper** | H100 |
| 2022–23 | **Ada Lovelace** | RTX 40 系列 |
| 2024 | **Blackwell** | B200、GB200 |

因此，**Ampere 比 Pascal 晚了 4 代**，而不是更早。Ampere 的 A100 配备了 HBM2e 显存、第三代 Tensor Core、BF16 和 TF32 支持、用于推理的 2:4 稀疏性以及 MIG（多实例 GPU）分区——相比 Pascal 是一次重大飞跃。

**参考文献：**
- [NVIDIA GPU 架构 — NVIDIA 官方](https://www.nvidia.com/en-us/technologies/)
- [Pascal 微架构 — 维基百科](https://en.wikipedia.org/wiki/Pascal_(microarchitecture))
- [NVIDIA 数据中心 GPU 发展历程 — ServerSimply](https://www.serversimply.com/blog/evolution-of-nvidia-data-center-gpus)