---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕TUF RTX 3090二手评测
translated: true
type: note
---

问题：这个华硕TUF RTX 3090 24GB二手显卡的成色如何？

回答：

这实际上是一块**相当不错的RTX 3090二手卡**，尤其适合AI/大语言模型工作。

![Image](https://images.openai.com/static-rsc-4/Womafy_aUANL9LTQQXwk1pBydE4WNCQLUR4qSm-bDNbmI-FF2SnjAK1AVRwcg7UT8n1F3NRODhkOyplxl-ALnOjQHa4BRn9ixi2M-vKS49kN0p2zeqSazSJuGqQrvlP75NbyFCq1mquoGqO_nQSuO5fEij_3nyaFFPIPk0VpUJHRErKrPa-v0WzVHq__qDNq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/138Sr2uAC0-4r1FkZ6HjRlHg5Hd44wwVeKlyLlXOfnKAQnhIPFtb5iI3sEV50-qzFEpsGNXHFwzsJgWHRKzVXpRQU3dpXnl2cX5pq2SkFTHssrqNP4FcG3ZnexvQyAdsFSsZLP2kuJboDb2mugRlxlIXJ0UWz3_7u5oMVG-v_KElK5K49HSN5Mpuod0XEpl7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/7dJZNcD8z0KgZv6VEjhKQAsnqjx-wS33y9haeJWFV4gf5OvIMPOcjhk6R_IbiqMtL3ErVKmz1jYdUpWO9C-yvypRq9CnMBmMakI9WkareiYUZ7wwg4Qyfz1fhWfSd6zlXNioU-DD4kp6VYMcyJdrp7w36k5MLyi-6gWlipGTJOXcTf4zm7PHQce0aGODzHIP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/SbHRyoaQ5iAypJfMNRBiCjDEdfuZLLWlJqXdc2pzrFwXL3vopX_n297Bm9lqfS7v_9-O51s2QiXg-vM19dzD10nSI2XIGWnalFF9QzxkuCKsX5nDgtDNQ8dcirP3I6GeyWMdMDrHyXbLoRn2g3alGcyB5Z544OotHBH818AG8vZ2EflDaPKCwR-5ldttGhob?purpose=fullsize)

规格参数：

* GPU：华硕 TUF Gaming GeForce RTX 3090 24GB
* 显存：**24GB GDDR6X**（购买它的主要原因）
* 架构：Ampere
* 计算能力：8.6
* 张量核心：328
* FP16张量性能：约142 TFLOPS
* 显存带宽：约936 GB/s

对于AI任务：

| 模型负载                     | RTX 3090 24GB |
| --------------------------- | ------------- |
| Llama/Qwen 7B推理            | ✅ 优秀        |
| 14B模型量化版                | ✅ 良好        |
| 32B Q4推理                  | ✅ 可行        |
| 7B-14B模型的LoRA微调         | ✅ 非常好      |
| 全参数微调                   | ❌ 太小        |
| GPT-2 760M / nanoGPT训练    | ✅ 舒适        |

与你的RTX 4070对比：

|              | RTX 4070                  | RTX 3090              |
| ------------ | ------------------------- | --------------------- |
| 显存          | 12GB                      | **24GB**              |
| 显存带宽      | 504 GB/s                  | **936 GB/s**          |
| FP16张量性能 | 约60 TFLOPS               | **142 TFLOPS**        |
| 功耗          | 200W                      | 350W                  |
| CUDA          | 同代支持                   | 相同                  |

对于大语言模型开发，3090是一个巨大的提升，因为**显存是瓶颈**。

---

卖家声称：

> 3dmark测试99.3
> 烤鸡温度70度左右

好的迹象：

✅ 对于3090来说，烤机温度70°C非常不错。
3090通常运行温度：

* GPU核心：75-85°C
* 显存结温：95-110°C

缺失的信息：

**需要知道显存温度。**

3090的GDDR6X显存在PCB两侧都很热。

询问卖家：

```
GPU-Z截图：
- GPU温度
- 显存结温
- 热点温度
- ASIC质量
- BIOS版本
```

关键数据：

* 显存结温 < 90°C → 优秀
* 90-100°C → 正常
* > 105°C → 避免购买

---

年限：

> 20年的卡

意思是2020年的卡。

所以大约用了6年。

风险：

* 风扇轴承老化
* 导热垫干涸
* 可能有挖矿经历

不过华硕TUF是3090中较好的设计之一：

* 大型散热器
* 良好的VRM供电
* 散热优于许多鼓风机/公版卡

---

价格决定一切。

2026年中国二手市场大致行情：

* RTX 3090普通版：2500-3200元
* 华硕TUF/STRIX：2800-3500元
* 可疑低价：<2200元

我的估值：

| 价格         | 判断                           |
| ------------ | ------------------------------ |
| <2500元      | 🔥 值得买                      |
| 2500-3000元  | 👍 不错                         |
| 3000-3500元  | 只有成色极好才考虑             |
| >3500元      | 不具吸引力                      |

---

针对你的使用场景（大语言模型训练、ROCm实验、本地模型）：

我的推荐排名：

1. RTX 3090 24GB ⭐⭐⭐⭐⭐
2. RTX 4090 24GB ⭐⭐⭐⭐⭐（太贵）
3. RTX 3090 Ti 24GB ⭐⭐⭐⭐
4. RTX 4070 Ti Super 16GB ⭐⭐⭐
5. RX 7900 XT 20GB ⭐⭐⭐（ROCm有优势但生态较弱）

3090的杀手特性很简单：

**在二手市场价格买到24GB CUDA显存。**

对于AI工程，一块3090往往胜过一块更新的12GB/16GB显卡，因为许多模型根本放不下。

购买前，我建议你索要：

```
1. GPU-Z完整截图
2. FurMark/OCCT下的显存温度
3. 运行：
   nvidia-smi -q -d MEMORY
4. 是否有挖矿历史？
5. 原始发票？
```

如果价格在**2800-3000元**左右，这是一个强有力的候选。