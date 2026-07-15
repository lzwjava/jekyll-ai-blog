---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX PRO 6000价格飙升
translated: true
type: note
---

问题："RTX A6000 Pro"（即RTX PRO 6000 Blackwell——实际上并没有名为"A6000 Pro"的显卡）在过去几个月里是否从约5万人民币跳涨到了约10万人民币？

回答：大致如此，多个来源已证实。先做两点澄清：

**命名**：老款RTX A6000（Ampere架构，2020年，48GB GDDR6）价格基本没变。实际暴涨的是**RTX PRO 6000 Blackwell**（96GB GDDR7，2025年3月发布）——国内俗称"6000 Pro"，可能被误传为"A6000 Pro"。向客户报价前请先确认你追踪的是哪款卡。

**价格走势（RTX PRO 6000 Blackwell，美国官方市场）**：

| 日期 | 美元 | 人民币（约，官方汇率） |
|---|---|---|
| 2025年3月（发布） | $8,000–8,565 | ~54,500 |
| 2026年5月 | $8,900–11,500（零售飙升） | ~60,600–78,300 |
| 2026年6月13日 | $13,250（英伟达官方市场） | ~89,789 |

因此：**约15个月内上涨55-65%**，官方/市场价从约5.45万人民币涨至约9万人民币。英伟达已将RTX Pro 6000 Blackwell工作站GPU的官方市场价上调至13,250美元，较2025年3月发布时的建议零售价高出约55%。

与您提到的"10万人民币"之间的差距，若计入**中国大陆到岸成本**即可缩小。由于这些显卡面临出口管制阻力，多数产品经由新加坡/马来西亚/香港中转进入中国，并叠加关税、增值税（13%）及中间商加价。据一项估算，即使在美国发布价仍为约8,500美元时，到岸成本已达约7.5万人民币——更不用说2026年6月涨价至13,250美元后。将同样的加价链套用到当前13,250美元的官方价，实际交付到中国大陆的卡（尤其是服务器版）价格接近或超过10万人民币（Newegg一个报价为14,999美元，约合102,000人民币）。

所有来源均指出根本原因是：**GDDR7显存短缺**，而非制造成本——涨价中仅一小部分反映制造成本上升，其余均来自GDDR7显存市场的供需压力。

如果您正在为GPU集群预算进行配置，建议直接查当前灰市报价（淘宝/深圳eBay卖家）而非官方建议零售价，因为这才是您实际采购的价格——我找到的深圳eBay报价在运输/关税转嫁前已约为10,300–10,345美元（约8.8-8.9万人民币）。

参考来源：
- [Nvidia Raises RTX Pro 6000 Blackwell MSRP to $13,250 - MLQ News](https://mlq.ai/news/nvidia-raises-rtx-pro-6000-blackwell-msrp-to-13250-a-55-hike-in-one-year/)
- [Tom's Hardware — 55% increase over MSRP](https://www.tomshardware.com/pc-components/gpus/nvidia-raises-rtx-pro-6000-blackwell-gpu-pricing-to-usd13-250-55-percent-increase-over-msrp-in-a-years-time)
- [RTX Pro 6000 Blackwell 大陆到手价 - 知乎](https://zhuanlan.zhihu.com/p/1916163513161868969)
- [AI巨量需求抽干库存 - 新浪科技 (May 2026)](https://finance.sina.cn/stock/jdts/2026-05-18/detail-inhyhpyq4093606.d.html)