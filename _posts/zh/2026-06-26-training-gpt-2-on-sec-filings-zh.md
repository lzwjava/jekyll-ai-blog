---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于SEC申报文件训练GPT-2
translated: true
type: note
---

以下是完整说明：

== 数据集 ==
SEC-EDGAR — 来自SEC的EDGAR申报系统中的所有10-K年度报告。

- 17个parquet分片 → 使用GPT-2分词器（tiktoken，词汇表50257）进行分词
- 16个训练分片：1,555,060,445个token（1.55B）
- 1个验证分片：100,000,000个token
- 数据类型：uint16，以.npy文件存储在 /mnt/data/zz/datasets/sec-edgar-tok/

== 模型 ==
GPT-2 124M（标准nanoGPT架构）

- 12层，12个注意力头，768嵌入维度
- 123.59M参数
- 无偏置（LLaMA风格）
- 词汇表：50304（50257向上取整以提高效率）

== 训练 ==

- 有效批次：每个步骤32,768个token（4 batch × 1024 block × 8 grad_accum）
- 47,400步 = 约1.55B个token = 1个完整周期
- GPT-3风格优化器：lr=6e-4，热身2000步，余弦衰减至6e-5
- 混合精度（float16），融合AdamW
- 未使用编译（Python 3.11 inductor存在bug）

== 时间 ==

- 约700ms/步（未编译）
- 47,400 × 0.7s ≈ 33,180s ≈ 9.2小时
- 预计今晚/凌晨完成

== 预期结果 ==

- 损失从约10.98（随机初始化）开始，第20步时已降至8.85
- 对于金融文本，验证损失应收敛到约3.0-3.5范围
  （参考：github-code达到了3.466，但那个数据集噪声较大；
   SEC-EDGAR更干净，结构化的金融散文）
- 模型将学习SEC申报语言：财务表格、风险披露、MD&A部分、会计术语
- 训练后你会得到：out-sec-edgar-124m/ckpt.pt（最新检查点）

== 用途 ==
这是一个面向金融/SEC申报的领域特定语言模型。适用于：

- 生成逼真的10-K风格文本
- 作为基础模型微调用于金融NLP任务
- 在相关语料库上继续预训练

局限性：124M参数规模较小——别指望达到GPT-4级别的连贯性。
它能生成听起来合理的SEC文本，但在复杂推理或长程一致性方面会表现不佳。
