---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解码中国RTX 3090黑话
translated: true
type: note
---

问题：如何理解二手GPU市场中的“目前3090只有猛禽 雕 魔龙”？

回答：

这是中文显卡卖家的行话，意思是：

> “目前RTX 3090只有ROG Strix、（某个‘雕’系列）和Gaming X Trio/魔龙系列有货。”

详细解释：

* **3090** → NVIDIA GeForce RTX 3090 24GB。

* **猛禽** → 通常指华硕 ROG Strix GeForce RTX 3090。
  * “ROG 猛禽”是华硕的高端游戏型号。
  * 散热器大、PCB用料好、功耗上限高。
  * 二手市场通常较贵。

* **雕** → 通常指技嘉 AORUS GeForce RTX 3090 XTREME（“大雕”/AORUS）。
  * 技嘉AORUS显卡因鹰标被昵称为“雕”。
  * “大雕” = AORUS XTREME旗舰型号。
  * “小雕”有时指AORUS MASTER。

* **魔龙** → 通常指微星 GeForce RTX 3090 GAMING X TRIO（中文昵称“魔龙”）。
  * 微星Gaming X Trio系列。
  * 散热不错，PCB相对可靠。

所以卖家实际上是在说：

```
RTX 3090 可选型号：

华硕 ROG Strix 3090     = 猛禽
技嘉 AORUS 3090         = 雕
微星 Gaming X Trio 3090 = 魔龙
```

这些都是**大型三风扇AIB显卡**，不包括NVIDIA公版或更便宜的型号。

对于AI/LLM工作负载，这些型号之间的差异远没有游戏玩家在意的那么大：

| 型号                  | VRAM        | AI性能 | 散热    | 典型二手价值 |
| --------------------- | ----------- | ------- | ------- | ------------ |
| ROG Strix 3090        | 24GB GDDR6X | 相同    | 优秀    | 最高         |
| AORUS 3090            | 24GB GDDR6X | 相同    | 优秀    | 高           |
| MSI Gaming X Trio 3090| 24GB GDDR6X | 相同    | 良好    | 高           |
| 便宜的3090型号        | 24GB GDDR6X | 相同    | 各异    | 更便宜       |

对于LLM推理/微调，重要的因素是：

1. **24GB显存**
2. **显存温度**
3. **电源稳定性**
4. **是否用于挖矿**

一块¥5000–6000、散热良好的二手RTX 3090，对AI来说往往比多花钱买“猛禽/雕/魔龙”品牌更有价值。GPU芯片和显存容量完全相同。

参考：

* [ASUS ROG 显卡](https://rog.asus.com/graphics-cards/?utm_source=chatgpt.com)
* [GIGABYTE AORUS 显卡](https://www.gigabyte.com/Graphics-Card/AORUS-Graphics-Cards?utm_source=chatgpt.com)
* [MSI 显卡](https://www.msi.com/Graphics-Cards?utm_source=chatgpt.com)
