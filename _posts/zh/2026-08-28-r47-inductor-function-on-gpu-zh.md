---
audio: false
generated: true
image: false
lang: zh
layout: post
title: R47电感在GPU上的功能
translated: true
type: note
---

**问题：** GPU（如NVIDIA Quadro 410）上的 **R47** 元件起什么作用？

**回答：**

在GPU PCB上，“R47”最常见的身份是**功率电感（线圈/扼流圈）**——尽管前缀“R”可能造成误解，但它并非电阻。

在SMD电感标注规范中，“R”用作**小数点**。因此 **R47 = 0.47 µH**（微亨）。这是低于1 µH电感值的标准标注方式。

**它的作用是什么？**

标注为R47的元件是一个**储能电感**，属于将PCIe电源输入的12V电压转换为GPU核心或显存所需更低稳压电压的电路的一部分——例如，将12V转换为显存电压。

在某些显卡上，R47电感是显存（如HBM）内部电压稳压器的一部分——输出端通常约为0.8V。

**结合APM8720 + VP57F（您之前的问题）的上下文：**

R47电感与这些元件**协同工作**，作为**VRM（电压调节模块）**降压转换器电路的一部分：

- **APM8720** = PWM控制器（大脑）
- **VP57F MOSFET** = 开关晶体管（肌肉）
- **R47（0.47 µH电感）** = 储能线圈（将开关电源平滑为纯净直流）
- 其旁边的电容 = 滤除纹波电压

在GPU显卡上，通常可以找到多个R22（0.22 µH）和一两个R47（0.47 µH）电感。R47的规格通常约为0.0033 Ω直流电阻和10A额定电流。

**简而言之：** R47是一个**0.47 µH功率电感**——它是GPU电压调节电路的关键部件，确保向GPU核心或显存稳定、纯净地供电。

**参考资料：**

- [SMD电感标注指南 — Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/smd-inductor-identification-reading-markings-testing-guide)
- [GPU上烧毁的R47 — iFixit](https://www.ifixit.com/Answers/View/232421/Burned+resistor+on+GPU)
- [GTX 1080上损坏的R47 — AnandTech论坛](https://forums.anandtech.com/threads/fried-resistor-and-vrm-on-gtx-1080.2543963/)
- [GTX 770 R47电感 — HardForum](https://hardforum.com/threads/gtx-770-series-need-inductor-update-fixed-it.1953238/)
