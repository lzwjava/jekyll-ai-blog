---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何租用100块H100 GPU
translated: true
type: note
---

问题：如何租用100块H100 GPU来运行实验？

让我搜索当前可用的选项。

答案：在2026年，租用100块H100 GPU进行实验非常可行。以下是关于你的选项以及如何开始的完整说明。

---

## 💰 价格概览（100块H100）

在2026年，租用H100 GPU的价格通常在每GPU小时 **2.00至10.00美元** 之间，具体取决于供应商。对于100块GPU，你的每小时成本会有显著差异：

| 供应商 | 每GPU/小时 | **100块GPU/小时** | 最佳适用场景 |
| --- | --- | --- | --- |
| GMI Cloud | $2.00–$2.40 | ~**$200–$240/小时** | 预算实验 |
| io.net | $2.10–$3.50 | ~**$210–$350/小时** | 快速部署 |
| Lambda Labs | ~$2.49–$2.99 | ~**$249–$299/小时** | 研究/简单设置 |
| RunPod | $2.89–$3.29 | ~**$289–$329/小时** | 灵活配置 |
| CoreWeave | ~$6.16 | ~**$616/小时** | 企业级/InfiniBand |
| AWS (p5) | ~$6.88 | ~**$688/小时** | 完整企业级堆栈 |

AWS和Google Cloud针对相同硬件收取的费用比专业GPU云供应商高出2–5倍。

---

## 🏆 100块GPU的最佳供应商选项

### 1. **io.net** — 部署最快，性价比最高

io.net运营着一个去中心化的GPU云，汇聚了来自130多个国家数据中心超过32万块GPU。H100集群在2分钟内即可部署完成，相比AWS和Google Cloud可节省50–70%的成本。非常适合快速启动100块GPU。

### 2. **GMI Cloud** — 每GPU价格最低

GMI Cloud提供1,000 GPU小时，价格为2,100美元（PCIe）或2,400美元（SXM）。同时提供可扩展的集群配置。

### 3. **Lambda Labs** — 简单且对研究人员友好

Lambda专注于GPU云服务，定价简单明了（每块H100约2.49美元/小时），没有复杂的计费结构——深受研究人员和小团队欢迎。

### 4. **CoreWeave / AWS** — 适用于严肃的分布式训练

Azure的ND H100 v5系列将高带宽InfiniBand网络与H100 GPU相结合，非常适合跨多个节点的分布式训练。如果你需要紧密的节点间通信，多付的额外费用是值得的。

---

## 🛠️ 租用100块H100的实际步骤

**步骤1 — 选择SXM还是PCIe**

- **H100 SXM**：最适合多GPU分布式训练（NVLink，GPU间900 GB/s带宽）
- **H100 PCIe**：更便宜，适用于并行的独立任务

**步骤2 — 选择供应商并创建账户**

- 预算型：[io.net](https://io.net) 或 [GMI Cloud](https://gmicloud.ai)
- 企业级/InfiniBand：CoreWeave 或 AWS

**步骤3 — 申请集群**

- 100块GPU = 12–13 × 8-GPU节点
- 对于大型集群，直接联系销售部门获取预留价格

**步骤4 — 考虑预留/竞价实例价格**
大多数价格对比默认采用按需付费。承诺1–3年使用期，云供应商会提供大幅折扣——Lambda Labs的预留H100价格为1.89美元/小时，已接近市场竞价实例价格。

**步骤5 — 设置你的工作负载**

- 使用PyTorch DDP或DeepSpeed等框架进行多节点训练
- 确保已配置节点间网络（InfiniBand / RoCE）

---

## 💡 100块GPU实验的成本估算

| 持续时间 | 预算供应商（~$2.40/GPU-小时） | 超大规模云（~$6.88/GPU-小时） |
| --- | --- | --- |
| 1小时 | ~$240 | ~$688 |
| 1天 | ~$5,760 | ~$16,512 |
| 1周 | ~$40,320 | ~$115,584 |

H100的租赁价格已接近多年低点，使得2026年成为租用而非购买的好时机。

---

参考文献：

- [GMI Cloud: 2026 H100价格指南](https://www.gmicloud.ai/en/blog/2026-cost-of-renting-or-uying-nvidia-h100-gpus-for-data-centers)
- [io.net: 2026年H100租赁完整指南](https://io.net/p/h100-gpu-cloud-where-to-rent-complete-pricing-guide-for-2026)
- [Spheron: NVIDIA H100新闻与价格2026](https://www.spheron.network/blog/nvidia-h100-news-2026/)
- [IntuitionLabs: H100租赁价格对比（15+供应商）](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
