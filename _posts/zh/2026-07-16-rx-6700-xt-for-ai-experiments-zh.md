---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RX 6700 XT 用于AI实验
translated: true
type: note
---

**问题：Radeon RX 6700 XT 12GB (RDNA2) 简介，尤其针对 AI/GPU 用途。**

**答：**

AMD Radeon RX 6700 XT 是 **2021 年推出的中端 RDNA2 游戏 GPU**。如今它受人关注的主要原因是 **12GB 显存和低廉的二手价格**。([AMD][1])

![Image](https://images.openai.com/static-rsc-4/uqfwGc9FmLotS2eGklN8aE7wFb0903FJAXVjBNw3w78MgUF4-dpGkahN9No92ibvIcxrT9JOeJFZgZeRXzQjQHlgBQVDGc4gZLh8IrdIUDRATBoP7gDaALAlEw_4tdX3Ls2Vho3n8z_5cOLMGi-PO-960-NX9DX4EFuvojBqVKhlM7C9qIYkcVOWheljBvFK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LsWTcLgSl7waB4CP_z16klf8AB60wnMvWjCKu3cbQwrvkbgFiimr1vR2LW0oseJQrxZiIN2_jEEw65zZF3iqHVeG-ZA8voIPnBQSkOaqtEXAMMNUt9GDIb900nl_Onxr9kEG3BwAJqY9t9aTdIsUKvWFKaSxBkqXI5q-LVS6wLYfeaiLqDP2SnUxOa4paKup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/p_7iLWvbkhCQ1u-hhcIbacVSW_sblGiCQ8ItJ4oTmCotz1Sg94yj-bJwHvo_SE9Evom-WOBkD8Biqiq2It7eDJp83gIZjydB7izxI1kgrbmO4Z4qVqKj28L6BlWV27urzVZoarVibyM312KGB1ZNp83bzw9zLkotHGr-q9hIsCfWf_63ewdlI-k5SxoV9W-g?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eu-rFoI5eRR2vn4AnzFFXnV5F7gYxwLfaS8v-WN8IPhQS6L-V97tX6tut9kp2d0Unh4OL6RLkWzzy1UzaG7iYunRkPNT9o8WXC-RFHf8YpmBufthrfVrbhZu5lbazoRYVNR-YVSa2xBz0vaK7NKErgWu5hFQknN96J4PwqHDsR0MvMdw1EU57lmABi0HPjsN?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yLWwyCNXrwgUwZXwwQsDdnh7Niz8X0oigxu8hVDMJNpNo2uR3Scr8kI6XTH1YzO-g2s4dMYTXGVWPWmRofvL9ZYAPZTnvq61kcSM90kjIxkV3nBGmEbeimmTbiKwoxX6CyYY6kc2eGiFIb0EZ2oJipYvjM1URDN76xEG4qnELqP8i7JnIJSk_CG8FQ3WuHwa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/E2bYslRQcjAsGFohdpPUP5Ohhd99Mte0x-_P1DKYNlTQh8bJsO2A5Cc0-rcom33VlFYpTBkdwehhQdFlPQ5dSBNuouqrObbLbJ5Q2hIT_a9kTM8-Wh63G7wLjT4Kg41jU0D8BhuC47ZEmYTJKbYKBPiN7YP813DaCb78CavVL9_5PNB_UjA-2yYpB4Ee2Fz8?purpose=fullsize)

## 硬件规格

| 项目               |   RX 6700 XT |
| ----------------- | -----------: |
| 架构               |        RDNA2 |
| 芯片               |      Navi 22 |
| 制程               |          7nm |
| 显存               |   12GB GDDR6 |
| 显存位宽           |      192-bit |
| 带宽               |     384 GB/s |
| Infinity Cache    |         96MB |
| 计算单元           |           40 |
| 流处理器           |         2560 |
| FP32              | ~13.2 TFLOPS |
| 功耗               |        ~230W |
| PCIe              |     PCIe 4.0 |

([AMD][2])

它被设计为 **1440p 游戏显卡**，性能定位在 RTX 3060 Ti / RTX 3070 级别（视负载而定）。([AMD][1])

---

## 与你的 RTX 4070 对比

你的 RTX 4070：

|              | RX 6700 XT | RTX 4070      |
| ------------ | ---------- | ------------- |
| 显存         | 12GB       | 12GB          |
| 显存类型     | GDDR6      | GDDR6X        |
| 架构         | RDNA2      | Ada Lovelace  |
| AI 生态      | 弱         | 优秀          |
| CUDA         | ❌          | ✅             |
| Tensor 核心  | ❌          | ✅             |
| FP16 AI      | 尚可       | 强很多        |
| 功耗         | 230W       | 200W          |

对于 AI：

**RTX 4070 >>> RX 6700 XT**

因为 CUDA + Tensor 核心 + 成熟的 PyTorch 支持远比显存大小重要。

---

## 用于 LLM / ROCm 实验

这也是 RX 6700 XT 变得复杂的地方。

### 优点：

* 12GB 显存
* 便宜
* Linux 支持
* 可以运行一些 OpenCL / ROCm 实验

### 缺点：

RDNA2 消费级显卡并非 ROCm 的最佳选择。

ROCm 生态在以下显卡上表现更好：

* MI50
* MI100
* MI200
* MI300
* Radeon Pro VII

你的 MI50 16GB 实际上比 RX 6700 XT 更适合 ROCm。

RX 6700 XT 拥有类似的显存：

```
RX 6700 XT
12GB GDDR6

MI50
16GB HBM2 ECC
```

但 MI50 拥有：

* HBM2 带宽（约 1TB/s 级别）
* ECC
* Instinct 驱动路径

---

## 本地 LLM 大小

显存：

```
7B 模型
FP16：
7B × 2 bytes ≈ 14GB
```

所以 RX 6700 XT 无法舒适地加载 7B FP16 模型。

但：

```
7B Q4：
~4-5GB
```

可行。

示例：

```
Qwen2.5-7B-Q4
Llama-3.1-8B-Q4
Mistral-7B-Q4
```

应该都能装下。

---

## 价格评估

你的预算范围：

```
¥1000-1500
```

是合理的。

具体：

### ¥1000

划算。

你将获得：

* 12GB 显存
* 接近 RTX 3070 级别的游戏性能
* 一张便宜的实验卡

### ¥1500

吸引力下降。

因为二手 RTX 3060 12GB / RTX 3070 有时与之竞争，而 RTX 拥有 CUDA。

---

## 我对 AI 实验的排名

针对你的使用场景：

```
RTX 4070 12GB
    |
    | 好得多
    v
RTX 3060 12GB
    |
    v
RX 6700 XT 12GB
    |
    v
RX 580 / 更老的 AMD
```

但针对 ROCm 学习：

```
MI50 16GB
    >
Radeon Pro VII 16GB
    >
RX 6700 XT
```

---

## 结论

RX 6700 XT 12GB：

* 游戏：⭐⭐⭐⭐⭐
* 性价比：⭐⭐⭐⭐
* LLM 推理：⭐⭐⭐
* ROCm 学习：⭐⭐
* 训练：⭐

对于你的情况（RTX 4070 + MI50 实验），我**不会购买 RX 6700 XT，除非你能找到约 ¥1000 的价位**。它主要是一张便宜的 12GB 显存卡，并非严肃的 AI 卡。

参考：

* AMD Radeon RX 6700 XT 规格 ([AMD][2])
* AMD RX 6700 XT 发布信息 ([AMD][1])

[1]: https://www.amd.com/en/newsroom/press-releases/2021-3-3-amd-unveils-amd-radeon-rx-6700-xt-graphics-card-d.html?utm_source=chatgpt.com "AMD Unveils AMD Radeon RX 6700 XT Graphics Card, Delivering Exceptional 1440p PC Gaming Experiences"
[2]: https://www.amd.com/en/products/graphics/desktops/radeon/6000-series/amd-radeon-rx-6700-xt.html?utm_source=chatgpt.com "Radeon™ RX 6700 XT Graphics Card"