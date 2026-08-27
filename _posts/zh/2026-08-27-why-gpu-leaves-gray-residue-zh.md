---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么GPU会留下灰色残留物
translated: true
type: note
---

**问题：** 为什么触摸旧的 Quadro 410 上的 GPU 芯片会在手指上留下灰色残留物？

**回答：**

你手指上的那层灰色物质几乎可以肯定是 **干燥、老化的导热硅脂**，原本是涂在 GPU 芯片和散热器接触板之间的。

以下是原因：

- **导热硅脂会老化。** 经过多年的热循环，硅脂会变干、开裂并粉化。旧的出厂硅脂在芯片和散热器接触板上都会变干并变色——对于像 Quadro 410 这样的老旧工作站显卡，这种硅脂可能已经用了十几年。

- **大多数导热硅脂是灰色的。** 标准硅脂使用金属氧化物（如氧化锌或铝）甚至银颗粒作为导热填料，这赋予了它们特有的灰色/银色。

- **干燥后容易剥落。** 硬化干燥的导热硅脂很容易脱落，所以仅仅触摸芯片就会将其转移到手指上。

**你应该做什么：**

既然硅脂已经老化到这种程度，它的导热效果已经很差。你应该重新为显卡涂抹硅脂：

1. 使用高浓度异丙醇（IPA）和无绒布或棉签，以轻柔画圈的方式擦除干燥的硅脂。
2. 切勿在 GPU 芯片上使用刀片、金属刮刀或研磨材料——芯片是裸露的硅，可能会被永久划伤。
3. 在重新安装散热器之前，在芯片中心涂抹一小粒豌豆大小的新导热硅脂（例如 Arctic MX-4 或 Thermal Grizzly Kryonaut）。

这对于一块旧的二手 GPU 来说是完全正常的——没有损坏，只是需要重新涂抹硅脂。

---

**参考资料：**
- [如何从 GPU 芯片上移除旧硬导热硅脂 – Overclock.net](https://www.overclock.net/threads/how-to-remove-old-hard-thermal-compound-from-gpu-die.1720856/)
- [如何更换 GPU 导热硅脂 – computerinfobits.com](https://knowledge.computerinfobits.com/hardware/gpu/thermal-paste-replacement)
- [重新涂抹你的 GPU 导热硅脂 – Gamer Hardware](https://gamerhardware.org/repaste-gpu-thermal-paste/)