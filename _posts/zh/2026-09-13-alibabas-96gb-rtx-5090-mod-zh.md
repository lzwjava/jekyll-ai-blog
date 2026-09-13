---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 阿里96GB RTX 5090改装版
translated: true
type: note
---

**问题：**“魔改”是什么意思？阿里巴巴上的一家中国制造商是如何将 RTX 5090 改装成 96GB 显存的？

**回答：**

**什么是魔改？**

魔改是一个中文俚语，由“魔”（mó，意为“恶魔般的/神奇的”）和“改”（gǎi，意为“修改/改变”）组合而成。它的字面意思是**“极限/激进改装”**——一种强烈且非常规的改造，几乎达到超自然或“疯狂科学家”级别。在中国科技圈中，这个词常用于描述通过 DIY 或工厂工程手段将硬件性能远远推超出原始规格的情况。你可以把它理解为中文版的“科学怪人式改装”或“极限超频/改装文化”。

---

**阿里巴巴上的 96GB RTX 5090“魔改”版**

深圳市速桥智能科技有限公司将原版 32GB RTX 5090 升级为 96GB 显存，并将改装后的显卡以约 3，888 美元的价格在阿里巴巴上出售。以下是其技术实现方式：

**1. 定制 PCB（印刷电路板）**

RTX 5090 96GB 很可能采用了定制 PCB，使制造商能够以“叠层模式”安装显存芯片，通过在电路板两侧放置显存焊盘，将 PCB 上的总显存容量翻倍。

**2. 更换/升级显存芯片**

改装者将原有的 GDDR7 芯片替换为更高容量的模块，并使用先进的 BGA（球栅阵列）焊接技术重新配置 PCB。

**3. 对 GPU 核心进行重新植球**

卖方可以单独采购 GB202 芯片，或者从零售版 RTX 5090 显卡上拆下核心，然后重新植球到定制 PCB 上——中国的工作室此前已用这种方法将 RTX 4090 改装至 48GB 显存。

**4. 为什么这在技术上可行**

拥有 96GB GDDR7 显存的 RTX Pro 6000 Blackwell 与 RTX 5090 使用相同的 GB202 芯片，但启用了更多的流处理器（SM）。这证明 96GB 配置在 GB202 架构上是可行的。

**5. 背景与注意事项**

这一创新正值美国加强对英伟达 AI 级芯片对华出口限制之际，迫使许多中国企业探索替代方案——由此催生了围绕游戏显卡的蓬勃发展的改装经济。然而，阿里巴巴的商品页面上标注的是 GDDR6X 显存而非 GDDR7，这是一个值得注意的警示信号，同时固件/显存初始化问题也需要解决。这并非首例——中国工厂此前已生产过 RTX 3090 48GB 和 RTX 4090 48GB 等改装显卡。

---

**参考资料：**

- [Tom's Hardware – 阿里巴巴上出现中国改装的 RTX 5090 96GB](https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original)
- [eTeknix – 搭载 96GB 显存的 RTX 5090](https://www.eteknix.com/rtx-5090-with-96-gb-of-vram-appears-on-alibaba-for-almost-4000/)
- [igor'sLAB – RTX 5090 96GB 改装：技术上可行但未经证实](https://www.igorslab.de/en/rtx-5090-with-96-gb-vram-appears-on-alibaba-modification-technically-plausible-but-unconfirmed/)
- [ThePCEnthusiast – 阿里巴巴上的 RTX 5090 96GB](https://thepcenthusiast.com/rtx-5090-96gb-vram-mod-alibaba/)
