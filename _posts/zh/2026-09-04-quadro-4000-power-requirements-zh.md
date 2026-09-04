---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 4000 电源要求
translated: true
type: note
---

**问题：** Quadro 4000 的电源线需要提供多少瓦的功率？

**回答：**

NVIDIA Quadro 4000 的总**最大功耗为 80W**：

| 来源 | 功率 |
|---|---|
| PCIe 插槽（主板） | 最高 75W |
| 6 针 PCIe 电源线 | 额外最高 75W |
| **显卡 TDP（总计）** | **最大 80W** |

因此，您的 PSU 只需通过 6 针电源线提供适中的功率即可。**标准 6 针 PCIe 连接器的额定功率为 75W**，对于这张卡来说绰绰有余。

**关键要点：** 任何带有 6 针 PCIe 连接器的现代 ATX PSU 都可以轻松应对这张卡。Quadro 4000 是一款相对低功耗的工作站显卡 — 推荐的最低电源功率为 **300W**，因此大多数系统都没有问题。

**参考资料：**
- [NVIDIA Quadro Power Guidelines (PNY)](https://www.pny.com/file%20library/company/support/product%20brochures/nvidia%20quadro/quadro-power-guidelines.pdf)
- [Quadro K4000 power info – Ten Forums](https://www.tenforums.com/graphic-cards/211663-inserted-old-pc-nvidia-quadro-k4000-but-prompts-pow.html)