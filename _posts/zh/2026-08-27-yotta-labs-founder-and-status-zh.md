---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Yotta Labs 创始人及状态
translated: true
type: note
---

## 问：Yotta Labs（yottalabs.ai）的创始人是谁？公司经营状况如何？

![Image](https://images.openai.com/static-rsc-4/hwu-5VuYZ9wycyE1YcK9LQoXjxtOApezQIGfPcAGWgjhUUjpsjRyswS1pwkJAVlV4w2UoBPxLypvx8nqlW4Co82PjRKu0Dz8BxLLjaLLhw1bMYgpzbWgwmSeumNHXlXmR2R7LQxaHiPKdsYmNXF98R00Oz9LgJ8CHJQkxOigVJtyqEWUK3CEimRdnZ5YZodS?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/poBG_dz0YTEJCcpIwYh2qZpQmBi8AQFPLkkkuzLxPPO6nJXXdU9NoeEvjEgMoTWB1xzN22XbvQvq4OpVlIgl2hqhtwxRD0UJPlONJZnnCUFgX9XeTooqyZJg4xhi9AFlN-BLP4UKZFP_GGxyyJgc1ckWhMk2tvBupI7lonv_cVu4bT0UJclQZLVgfRoogWyk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/snXD4wO_enKyYPguDgwUHZ0Az395qqtZbD6ys4DQF4fKNDUgdXTG0HMy4s2tCJjLSaHZyUyWux36NKOYuCayngJD2jDzhTOi-jVESq7a_KFGer5w52AahIr73xug8izsi2J72mKAy-NPs5_4uSVZJR_zF7TtAF9eXe2naBUBi6c9wHoVu3uwRgoKbGx8WNVw?purpose=fullsize)

**Yotta Labs**（不要与印度的 Yotta 数据中心公司或 Yotta 金融科技混淆）是一家位于西雅图的 AI 基础设施初创公司，正在构建 **GPU 云 + AI 编排层**。([Crunchbase][1])

### 创始人/团队

根据公司资料：

*   **李达 (Da Li)** — 创始人/CEO
*   **Johnny Liu** — 联合创始人/CTO
*   **李东 (Dong Li)** — 首席科学家/联合创始人（部分资料列出）([Crunchbase][1])

团队规模非常小（大约个位数）。LinkedIn 显示 Yotta Labs 是一家位于西雅图，员工人数在 2-10 人的公司。([LinkedIn][2])

技术背景很有意思：

*   Johnny Liu 专注于大规模机器学习系统和 HPC。([Crunchbase][3])
*   公司强调 GPU 内核、异构硬件以及在多芯片架构（NVIDIA、AMD、AWS Trainium/Inferentia）上执行。([Yotta Labs][4])

---

## 他们在做什么？

核心理念：

> AI 计算将变得碎片化，而不仅仅是“NVIDIA GPU 无处不在”。

当前情况：

```
AWS
 ├── NVIDIA
 ├── Trainium

Azure
 ├── NVIDIA
 └── AMD

Google Cloud
 └── TPU

其他 GPU 云
 └── 混合 GPU
```

每个硬件供应商都有：

*   不同的驱动程序
*   不同的内核
*   不同的调度方式
*   不同的成本效益

Yotta 希望成为 AI 计算的 **Kubernetes 式抽象层**。

他们的定位：

```
                 AI 应用
                       |
                 Yotta 层
                       |
        --------------------------------
        |              |               |
     NVIDIA          AMD          Trainium
     H100            MI300        AWS ASIC
```

他们称之为“AI 基础设施操作系统”或执行层。([Yotta Labs 文档][5])

产品包括：

*   GPU 云实例
*   推理服务
*   AI 网关
*   工作负载编排
*   量化/优化工具 ([Yotta Labs][6])

---

## 公司实力如何？

我的评估：

### 优势

### 1. 问题真实存在

时机非常好。

在 2023-2026 年期间：

*   NVIDIA 占据主导地位，但供应受限。
*   AMD MI300/MI350、AWS Trainium、Google TPU 正在改进。
*   企业不希望为每个加速器重写所有代码。

基础设施层确实变得复杂。

历史上的类似模式：

*   VMware 抽象了服务器
*   Kubernetes 抽象了容器
*   CUDA 抽象了 GPU

AI 可能需要另一个抽象层。

---

### 2. 技术方向深入

许多 GPU 云基本上就是：

```
购买 GPU
+
租赁 GPU
+
漂亮的仪表盘
```

这是一种商品业务。

Yotta 试图做得更深入：

```
编译器/运行时/内核/调度器层
```

这要困难得多，潜在价值也更大。

他们的文档强调硬件感知调度和执行抽象。([Yotta Labs 文档][5])

---

### 弱点/风险

### 1. 竞争极其激烈

他们正在与以下公司竞争：

*   CoreWeave
*   Together AI
*   Lambda
*   超大规模云服务商

尤其是 CoreWeave，拥有巨大的资本和 GPU 供应优势。

---

### 2. 平台风险

问题是：

> AI 公司会需要一个中立的抽象层吗？

可能的未来：

**情景 A：NVIDIA 持续领先**

每个人都使用 CUDA。

那么 Yotta 的价值就会降低。

**情景 B：硬件变得碎片化**

那么 Yotta 的论点就会变得更强。

---

### 3. 公司规模小

与 CoreWeave 相比：

```
CoreWeave：
- 融资数十亿
- 庞大的 GPU 集群

Yotta：
- 种子阶段
- 团队极小
```

Crunchbase 显示 Yotta 处于种子阶段，员工数量很少。([Crunchbase][1])

---

## 从工程角度看我的看法

我实际上认为这是 AI 基础设施中一个更有趣的方向。

类比：

1990年代：

```
硬件
   |
操作系统
   |
应用程序
```

2020年代 AI：

```
GPU/ASIC
   |
AI 运行时 + 调度器
   |
模型
   |
应用程序
```

最终的赢家可能不是拥有最多 GPU 的公司，而是让异构计算变得简单的公司。

这与 NVIDIA CUDA 之所以强大的原因类似：并非因为 GPU 神奇，而是因为软件开发人员不再需要考虑硬件细节。

---

对于像你（训练 GPT-2，尝试 MI300X/ROCm、DeepSpeed、GPU 维修）这样的人来说，Yotta 的领域实际上与你的交叉点非常接近：

```
硬件
   +
分布式训练
   +
LLM 推理
   +
系统工程
```

有趣的技术挑战有：

*   他们能否高效地调度 H100 + MI300 + Trainium？
*   他们能否自动选择内核？
*   他们能否使 PyTorch/vLLM/SGLang 具有可移植性？
*   他们能否胜过仅使用 AWS？

这些都是非常困难的工程问题。

参考资料：

*   Yotta Labs 关于页面：([Yotta Labs 文档][5])
*   Crunchbase 公司资料：([Crunchbase][1])
*   Yotta 推理架构：([Yotta Labs][4])
*   Yotta 官方网站：([Yotta Labs][6])

[1]: https://www.crunchbase.com/organization/yotta-labs?utm_source=chatgpt.com "Yotta Labs - Crunchbase 公司资料与融资"
[2]: https://www.linkedin.com/company/yotta-labs?utm_source=chatgpt.com "Yotta Labs | LinkedIn"
[3]: https://www.crunchbase.com/person/johnny-liu-24d9?utm_source=chatgpt.com "Johnny Liu - Crunchbase 个人资料"
[4]: https://www.yottalabs.ai/inference?utm_source=chatgpt.com "跨所有 AI 芯片优化的推理 | Yotta Labs"
[5]: https://docs.yottalabs.ai/?utm_source=chatgpt.com "关于 | Yotta Labs"
[6]: https://www.yottalabs.ai/?utm_source=chatgpt.com "用于 AI 训练与推理的 GPU 云 | Yotta Labs"