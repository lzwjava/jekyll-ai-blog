---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU上的灰色材料是什么
translated: true
type: note
---

**问题：** 当你移除GPU（如Quadro 410）上的风扇后，芯片顶部的灰色材料是什么？它是否能让热量顺利排出？

**回答：** 这种灰色材料是**导热膏**（也称导热化合物或导热硅脂）。以下是它的成分和作用解析：

**成分：**
这是一种导热膏状物——通常是硅基化合物，填充了细小的金属或陶瓷颗粒（氧化锌、银等）。在Quadro 410及同时代的大多数GPU上，NVIDIA使用的是普通灰色硅脂。

**作用：**
GPU芯片和散热器表面在微观下都粗糙不平。如果直接贴合，两者之间会产生微小气隙——而空气是极差的热导体。导热膏填充这些微观间隙，在芯片与散热器之间形成连续的导热桥。

**热量能否通过它顺利排出？**
导热膏确实能帮助热量传导，但其本身的导热性并不优越——只是*远强于空气*。关键要点如下：

- 普通灰色硅脂的导热系数约为**3–8 W/m·K**（优质银膏可达约9–10 W/m·K）。
- 相比之下，铜的导热系数约为**400 W/m·K**。因此导热膏仍是导热链条中的薄弱环节，这也是为何需要*涂抹极薄一层*——越薄效果越好。
- 老化的干裂膏（常见于二手Quadro 410）会开裂失效，导致温度显著升高。
- 如果没有导热膏，GPU会因气隙而迅速过热。

**简而言之：** 它确实在履行促进导热的职责，但只有在新鲜且薄涂时效果最佳。若你Quadro 410上的导热膏已干裂或成碎屑状，更换新膏（即使是廉价产品）也能显著降低温度。

**参考资料：**

- [导热界面材料解析 – Thermal Grizzly](https://www.thermal-grizzly.com/en/thermal-interface-materials)
- [导热膏为何重要 – Linus Tech Tips](https://linustechtips.com/topic/thermal-paste-importance)
- [NVIDIA Quadro 410规格与散热 – TechPowerUp GPU数据库](https://www.techpowerup.com/gpu-specs/quadro-410.c1723)
