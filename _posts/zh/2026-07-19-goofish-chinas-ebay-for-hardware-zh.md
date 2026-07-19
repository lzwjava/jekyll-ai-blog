---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Goofish: 中国硬件版eBay'
translated: true
type: note
---

问题：[https://www.goofish.com/?locale=en](https://www.goofish.com/?locale=en) 是什么？

答案：

[Goofish（闲鱼）](https://www.goofish.com/?locale=en&utm_source=chatgpt.com) 是阿里巴巴旗下二手交易平台 **闲鱼** 的国际版域名。它相当于中国的 **eBay + Facebook Marketplace**，但与阿里巴巴生态系统深度整合。([维基数据][1])

它在中国尤其以以下商品闻名：

*   **二手电子产品**
    *   GPU：RTX 3090、RTX 4090、A6000、Tesla 显卡
    *   CPU、服务器、MacBook
    *   手机、相机
*   **电脑硬件**
    *   矿卡 GPU
    *   工作站配件
    *   工程样品
    *   退役企业级硬件
*   **收藏品**
*   **二手商品**
*   **工厂尾货/清仓商品** ([Savvyoo][2])

对于你寻找 AI 硬件来说，这正是许多中国用户买卖以下物品的地方：

```
RTX 3090 24GB
A6000 48GB
Tesla P100
Tesla V100
MI50
MI100
EPYC 服务器
DDR4 ECC 内存
NVMe SSD
```

价格可能远低于京东/天猫的原因是许多卖家是：

*   出售旧设备的个人
*   清算显卡的小型 GPU 矿工
*   销售二手企业硬件的 IT 商家
*   清理库存的公司

示例：

```
京东：
RTX 3090 全新/官方渠道：非常昂贵或已售罄

Goofish：
RTX 3090 二手：
¥4000-8000 人民币，视成色而定
```

（价格波动剧烈。）

交易模式：

```
买家
  |
  | 支付宝托管
  |
闲鱼平台
  |
  |
卖家
```

款项由阿里巴巴支付系统托管，直至交易完成。([阿里巴巴集团][3])

然而，与京东/天猫不同：

|              | Goofish                | 京东           |
| ------------ | ---------------------- | -------------- |
| 卖家         | 主要为个人             | 零售商         |
| 价格         | 较低                   | 较高           |
| 保修         | 通常无                 | 较好           |
| 风险         | 较高                   | 较低           |
| 议价         | 常见                   | 少见           |
| 稀有硬件     | 资源丰富               | 匮乏           |

购买 GPU 时的常见检查：

```bash
# 购买 RTX 3090 前
1. 索要 GPU-Z 截图
2. 索要 FurMark / 3DMark 测试结果
3. 检查显存错误
4. 检查挖矿历史
5. 测试温度
6. 优先选择本地自提
```

既然你已经在关注中国的二手 GPU 市场，Goofish 基本上就是主战场。这是许多中国 AI 爱好者寻找廉价 VRAM 的地方。([Trip.com][4])

虽然有英文界面，但大多数商品列表和卖家沟通仍以中文为主。国际买家通常需要具备中文能力、中国地址或使用代购/转运服务。([Savvyoo][2])

参考来源：

*   [阿里巴巴闲鱼概览](https://www.alibabagroup.com/en-US/about-alibaba-businesses-1747081802473799680?utm_source=chatgpt.com)
*   [闲鱼（维基数据）](https://www.wikidata.org/wiki/Q32187808?utm_source=chatgpt.com)

[1]: https://www.wikidata.org/wiki/Q32187808?utm_source=chatgpt.com "闲鱼 - 维基数据"
[2]: https://savvyoo.com/sites-apps/xianyu/?utm_source=chatgpt.com "闲鱼指南：二手购物、代购与安全 – Savvyoo"
[3]: https://www.alibabagroup.com/en-US/about-alibaba-businesses-1747081802473799680?utm_source=chatgpt.com "闲鱼 - 阿里巴巴集团"
[4]: https://www.trip.com/guide/info/xianyu.html?utm_source=chatgpt.com "闲鱼外国人指南：如何用英语买卖 | Trip.com"