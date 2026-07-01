---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诺贝尔奖得主Jumper离开谷歌加入Anthropic
translated: true
type: note
---

**问题：** 诺贝尔奖得主离开谷歌加入Anthropic发生了什么？AlphaFold及其创造者的背景是什么？要构建一个“zhiwei-fold”——个人蛋白质结构预测模型，需要什么？

**回答：**

## 人物：Demis Hassabis → 不，是 John Jumper

你朋友提到的诺贝尔奖得主几乎可以肯定是 **John Jumper** —— AlphaFold 2 的共同创造者，他与 Demis Hassabis 和 David Baker 共同分享了 2024 年诺贝尔化学奖。确认了。大新闻，新鲜出炉（2026年6月19日）。以下是完整情况：

---

## 实际发生了什么

John Jumper 在 Google DeepMind 担任副总裁/工程研究员近九年。2026年6月，他宣布将在休假后离开并加入 Anthropic。

Jumper 与 Hassabis 共同获得2024年诺贝尔化学奖的一半（因开发AlphaFold2），另一半授予 David Baker（因计算蛋白质设计）。AlphaFold2 已被190多个国家的超过200万科学家使用，加速了疟疾疫苗、癌症治疗和耐药菌的研究。

你朋友的判断是正确的——这是一个人才信号，而不仅仅是一次人事变动。

---

## 为什么这很重要（你朋友的核心观点是对的）

在 Jumper 宣布离职的前一天，Noam Shazeer ——《Attention Is All You Need》的合著者兼 Gemini 联合负责人 —— 离开了 OpenAI。谷歌在一周内失去了其两个标志性 AI 科学成就的架构师。

根据 SignalFire 的 2025 年人才状况报告，DeepMind 的工程师离开去 Anthropic 的可能性是反向流动的近 11 倍。Andrej Karpathy 也于 2026 年 5 月加入了 Anthropic 的预训练团队。

问题似乎既不是声望也不是金钱——Shazeer 尽管据说有一笔价值数十亿美元的交易，还是离开了。如果连这都留不住那些创造了公司最著名成就的人，那么问题可能不在于薪酬。

信号：Anthropic 的使命密度正在超越谷歌的资源，成为一种招聘工具。

---

## AlphaFold：它触及大众了吗？

你说得对，它不是面向消费者的，但影响是真实的：

截至 2024 年 1 月，AlphaFold 团队发布了 2.14 亿个蛋白质结构预测。制药公司的药物发现管道使用了它。它将数十年的结构生物学工作压缩成一个可自由查询的数据库。你不会直接感觉到它，但疟疾疫苗的研究人员会。

王垠的框架（诺贝尔/图灵奖本质上意义不大）在哲学上是连贯的——奖项滞后于实际洞察力数年，并且奖励可读性而非深度。但 AlphaFold 是一个罕见的案例，其中奖项确实与一个真实、可验证且具有可衡量的下游用途的突破相匹配。

---

## zhiwei-fold：需要什么？

这是有趣的部分。以下是你未来 6 个月内的一个现实路径：

### AlphaFold2 实际上是什么（架构）

```
输入：氨基酸序列（L 个残基）
  → 通过 Jackhmmer/HHblits 进行多序列比对 (MSA)
  → 配对表示 + MSA 表示
  → Evoformer（48 个模块）：残基对上的注意力 + MSA 行/列
  → 结构模块：3D 框架上的不变点注意力 (IPA)
输出：每个残基的 3D 坐标 + pLDDT 置信度
```

关键洞察：蛋白质折叠是一个基于进化共变信号的 **几何注意力问题**。MSA 编码了哪些残基共同进化 → 哪些残基在空间上接近。

### 最低起点

你不需要从头重新训练 AlphaFold2。从这里开始：

```python
# ESMFold — 单序列折叠，无需 MSA
# Meta 的模型，操作简单得多
pip install fair-esm

import esm
model, alphabet = esm.pretrained.esmfold_v1()
model.eval().cuda()

sequence = "MKTIIALSYIFCLVFA"  # 示例
with torch.no_grad():
    output = model.infer_pdb(sequence)

with open("output.pdb", "w") as f:
    f.write(output)
```

ESMFold 用大型蛋白质语言模型（ESM-2，3B 参数）换掉了 MSA 的复杂性。在 RTX 4070 上是一个不错的起点。

### 现实的 zhiwei-fold 路线图

| 阶段 | 任务 | 硬件 | 时间线 |
| ------ | ------ | ---------- | -------- |
| 1 | 在自定义序列上运行 ESMFold 推理 | RTX 4070 | 第 1 周 |
| 2 | 在领域特定蛋白质数据集（例如抗菌肽）上微调 ESM-2 嵌入 | RTX 4070 | 第 1 个月 |
| 3 | 在上面训练一个轻量级结构头（GVP-GNN 或 IPA） | MI300X | 第 2-3 个月 |
| 4 | 数据集：UniProt + PDB + AlphaFold DB 筛选子集 | 任意 | 持续进行 |
| 5 | 评估：TM 分数 vs 实验 PDB 结构 | 任意 | 每次迭代 |

### 关键数据集

```bash
# AlphaFold DB（子集）
wget https://ftp.ebi.ac.uk/pub/databases/alphafold/latest/UP000005640_9606_HUMAN_v4.tar

# PDB 结构
rsync -rlpt -v -z --delete \
  rsync.rcsb.org::ftp_data/structures/divided/pdb/ ./pdb/

# 用于 ESM 预训练数据的 UniRef50
wget https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz
```

### nanoGPT 类比

你已经了解 nanoGPT。将 zhiwei-fold 视为：

- **分词器** → 氨基酸词汇表（20 种标准氨基酸 + 特殊标记）
- **嵌入** → ESM-2 蛋白质语言模型（你的“预训练权重”）
- **Transformer** → Evoformer（成对注意力，不仅仅是序列注意力）
- **头部** → 输出 3D 框架而非 logits 的结构模块

与 GPT 的根本区别：你预测的是 **几何**（每个残基的旋转矩阵+平移），而不是 token 分布。损失函数是 FAPE（框架对齐点误差）而非交叉熵。

---

## 总结

你朋友的社会解读是正确的——Jumper 的离开是一个关于 Anthropic 轨迹的重力信号，而不仅仅是一份简历的洗牌。对你来说：蛋白质折叠领域确实是可接近的。ESMFold 可以在消费级 GPU 上运行，数据集是公开的，你的 MI300X（192GB HBM3）足够微调 ESM-2 3B。如果你像对待 nanoGPT 那样对待它——从推理开始，理解架构，然后从有意义的子集训练一个小版本——那么 6 个月内实现 zhiwei-fold 是现实的。

参考文献：

- [John Jumper Wikipedia](https://en.wikipedia.org/wiki/John_M._Jumper)
- [AlphaFold Nobel Laureate Joins Anthropic — TechTimes](https://www.techtimes.com/articles/318754/20260620/alphafold-nobel-laureate-john-jumper-joins-anthropic-after-nine-years-deepmind.htm)
- [John Jumper Leaves DeepMind for Anthropic — The Next Web](https://thenextweb.com/news/john-jumper-nobel-deepmind-leaves-anthropic-alphafold)
- [ESMFold GitHub](https://github.com/facebookresearch/esm)
- [AlphaFold DB](https://alphafold.ebi.ac.uk/)
