---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI芯片先驱打造塔拉斯未来
translated: true
type: note
---

Ljubisa Bajic 是一位经验丰富的半导体企业家和架构师，目前担任 AI 芯片初创公司 **Taalas** 的 CEO 和联合创始人。他因在 AMD 和 Nvidia 等行业巨头处的丰富背景，以及创立资金充裕的 AI 硬件公司 Tenstorrent 而广受认可。

这是一个对他职业背景和当前企业的全面概述。

### 🧑‍💼 职业背景：从 AMD 到 Tenstorrent

Ljubisa Bajic 的职业生涯深深植根于半导体行业，专注于 VLSI design 和 computer architecture。在推出自己的企业之前，他在全球最大的两家芯片设计公司积累了超过十年的经验：

- **AMD：** 他在 AMD 工作了近十年，担任各种角色，包括 IC Design and Architecture 总监，从事 power management 和 DSP design 工作。
- **Nvidia：** 他还在 Nvidia 担任 Senior Architect，进一步深化了其在 graphics 和 accelerator design 方面的专长。

这种深厚的行业经验促使他在 2016 年创立了 **Tenstorrent**。作为联合创始人兼 CEO，他从零开始打造公司，从自家地下室起步，与两位同事以及传奇芯片架构师 Jim Keller 的早期天使投资开始。在他的领导下，Tenstorrent 开发了 full-stack AI compute solutions 并筹集了大量资金。2022 年底的一次引人注目的角色互换中，Bajic 与 Jim Keller 交换职位，成为 Tenstorrent 的 CTO 和总裁，随后于 2023 年 3 月完全离开公司，以追求新愿景。

### 🚀 Taalas：定制硅芯片的新篇章

Ljubisa Bajic 于 2023 年 8 月创立了 **Taalas**，不久前刚刚离开 Tenstorrent。他担任该公司的联合创始人兼 CEO，领导的团队包括联合创始人 Lejla Bajic（COO）和 Drago Ignjatovic（CTO）。

Taalas 总部位于加拿大多伦多，因其对 AI 硬件的颠覆性方法而迅速获得广泛关注和资金。

- **公司愿景：** Taalas 旨在通过大幅降低其成本来“commoditize AI”。Bajic 认为，这需要计算能力和效率的 **1,000x 改进**，这是一个用当前 general-purpose hardware 无法实现的目标。该公司的理念总结在他的一句话中：*“We should not be simulating intelligence on general purpose computers, but casting intelligence directly into silicon”*。
- **核心技术：** 与设计用于运行多种不同模型的传统 AI accelerators 不同，Taalas 为 **specific AI models** 创建定制芯片。
    - 该过程涉及一个自动化流程，直接将 deep learning models（如 Transformers 或 LLMs）实施到硅片中。
    - 这些芯片，公司称之为“Hardcore Models”，效率极高，一个芯片即可在芯片上包含整个 AI model，而无需外部内存，可能匹敌小型 GPU 数据中心的性能。
- **关键融资里程碑：** 该公司在短时间内获得了大量投资者的信心。
    - **2024 年：** 退出 stealth mode，并宣布从 Quiet Capital 和 Pierre Lamond 等投资者处筹集了两轮 **$50 million**。
    - **2026 年：** 在最近的发展中，Taalas 完成了一轮巨额 **$219 million** 融资，Fidelity 参与其中，展示了其技术强劲的势头。

以下是 Taalas 的关键细节总结：

| **属性** | **详情** |
| :--- | :--- |
| **创立时间** | August 2023 |
| **总部** | Toronto, Canada |
| **CEO & 联合创始人** | Ljubisa Bajic |
| **主要投资者** | Fidelity, Quiet Capital, Pierre Lamond |
| **总融资额** | ~$269 million（2024 年和 2026 年多轮） |
| **核心创新** | "Hardcore Models" - 针对 specific AI models 的定制硅芯片 |
| **首款产品** | HC1 chip，在 Llama3.1-8B 上实现超过 16,000 tokens/second |

希望这个全面概述对您有帮助。您想让我提供更多关于 Taalas 首款芯片 HC1 的技术规格细节吗？