---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 访问华为Atlas 350战略
translated: true
type: note
---

问题：**如何获取华为昇腾950 / Atlas 350的访问权限？我应该自己购买，还是使用大学的资源？**

回答：

是的——但有一个重要的区别：

### 1. 你很可能指的是 **Atlas 350**，而不是“昇腾950板卡”

当前的产品代际大致如下：

```text
昇腾 950
├── 昇腾 950PR   → 推理场景
│      └── Atlas 350 加速卡
│
└── 昇腾 950DT   → 训练/大规模计算
       └── Atlas 950 SuperPoD
```

华为在2026年7月正式展示了 **Atlas 950 SuperPoD**，这是一个拥有1024个NPU的巨型系统，并非个人开发者能买来放在桌下的设备。（[华为][1]）

对你来说更值得关注的是 **Atlas 350**。它于2026年3月推出，搭载 **昇腾 950PR**，根据公开规格，拥有112 GB HBM，约1.4 TB/s带宽和1.56 PFLOPS FP4。（[iThome][2]）

---

## 2. 你能自己购买 Atlas 350 吗？

**技术上可以。但实际上，我不建议你把它作为第一步。**

Atlas 350 通过华为的生态/合作伙伴渠道销售，不像 RTX 5090 那样可以直接在零售渠道购买。

已有多个厂商发布了完整的 Atlas 350 系统，包括：

* 昆仑
* 华勤
* 神州鲲泰
* 长江计算
* 宝德
* 百信
* 软通华方

（[iThome][2]）

此外，二手市场也有一些卡流通，但这里正是需要小心的地方：你不仅仅需要加速卡。

你还需要：

```text
Atlas 350
   ↓
兼容的主机/服务器
   ↓
CANN
   ↓
昇腾驱动/运行时
   ↓
PyTorch / vLLM-Ascend / MindSpore
   ↓
你的模型
```

**软件栈才是真正的入门成本**。

最近一项关于华为昇腾部署的实地研究发现，即使是经验丰富的工程师也会遇到算子不支持、并行性问题、数值问题、图编译问题以及设备级可靠性问题。（[arXiv][3]）

因此，我 **不建议你首先从阿里巴巴/闲鱼/eBay上购买一张二手 Atlas 卡**。

---

# 3. 对你来说，大学访问实际上是一个非常好的策略

如果你的目标是：

> “我想认真学昇腾，并在其上训练/部署大语言模型。”

那么我会按以下顺序排列你的选项：

```text
大学/研究实验室
        ↓
华为昇腾云/合作伙伴云
        ↓
租用昇腾服务器
        ↓
购买 Atlas 350
        ↓
购买整套 950 系统
```

对于个人工程师来说，**大学/实验室的访问权限可能回报率最高**。

为什么？

因为大学可能已经拥有：

```text
Atlas 集群
     +
CANN
     +
MindSpore
     +
PyTorch Ascend
     +
vLLM-Ascend
     +
华为工程师/生态支持
```

你只需要 SSH 访问即可。

这比花费十多万人民币购买硬件，然后发现你真正的问题是：

```text
“为什么这个算子编译不过？”
```

而不是：

```text
“950 有多快？”
```

要好得多。

---

# 4. 而且这实际上与你现在的研究方向相关

鉴于你已经在做类似的工作：

```text
nanoGPT
GPT-2 训练
Qwen
vLLM
ROCm / MI300X
PyTorch
分布式训练
LLM 推理
```

我不建议你将昇腾视为：

> “我需要一台昇腾机器。”

而是应该这样看待：

> **“我需要一个昇腾集群的 1-3 个月访问权限。”**

然后复现你现有的某个工作负载。

例如：

```bash
# NVIDIA
CUDA_VISIBLE_DEVICES=0 python train.py

# AMD
ROCR_VISIBLE_DEVICES=0 python train.py

# 昇腾
python train.py
```

并进行研究：

```text
PyTorch
   │
   ├── CUDA
   │
   ├── ROCm
   │
   └── 昇腾 NPU
          │
          └── CANN
```

这比单纯拥有这块卡要有价值得多。

---

## 5. Atlas 350 对你来说其实相当有趣

112 GB HBM 才是关键。

你的 RTX 4070 拥有：

```text
12 GB VRAM
```

Atlas 350：

```text
112 GB HBM
```

因此概念上：

```text
4070
12 GB
│
├── 小型 LLM
├── QLoRA
└── 推理

Atlas 350
112 GB
│
├── 更大的模型
├── FP8 / FP4 推理
├── 长上下文
├── 多模态
└── 严肃的 LLM 服务
```

而且华为明确将 Atlas 350 定位在 **LLM 推理、多模态生成和推荐**，而不是作为消费级 GPU。（[iThome][2]）

如果你对 **LLM 推理基础设施** 感兴趣，这确实是一个不错的目标。

---

# 6. 如果我是你，我会这样做

我会这样做：

```text
第1步
找到拥有昇腾 910/950 的中国大学/实验室
        ↓
第2步
获取 SSH 访问权限
        ↓
第3步
学习 CANN + torch_npu
        ↓
第4步
运行 Qwen / DeepSeek / vLLM-Ascend
        ↓
第5步
移植你现有的一个训练/推理实验
        ↓
第6步
分析 AscendC 算子
        ↓
第7步
然后才考虑购买 Atlas 350
```

**不要为了拥有硬件而优化，要为了深入接触整个软件栈而优化。**

而且这里有一个特别有趣的机会：华为表示其 CANN 生态系统正变得更加开放，已有数十个开源社区项目。（[华为][1]）

对于已经在做底层 LLM 工作的人来说，**昇腾 + CANN + AscendC + vLLM-Ascend** 可能比单纯再买一块 NVIDIA GPU 更有意思。

如果你的目标具体是 **“我想在广州/深圳找到某个地方，能实际 SSH 到一台昇腾 950/Atlas 350 机器”**，我可以搜索当前提供访问权限的 **大学、实验室、云服务商和华为合作伙伴项目**。

[1]: https://www.huawei.com/cn/news/2026/7/atlas-950-superpod?utm_source=chatgpt.com "昇腾950超节点真机亮相2026世界人工智能大会"
[2]: https://www.ithome.com/0/931/355.htm?utm_source=chatgpt.com "华为 Atlas 350 加速卡上市，搭载全新昇腾 950PR 处理器 - IT之家"
[3]: https://arxiv.org/abs/2607.08215?utm_source=chatgpt.com "On the Limitations of Non-GPU AI Accelerators for Large-Model Inference: A Field Study of MoE and Multimodal Serving on Huawei Ascend"