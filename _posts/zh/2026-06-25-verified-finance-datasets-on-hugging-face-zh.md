---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face上已验证的金融数据集
translated: true
type: note
---

以下是经过验证的答案。我通过实际访问每个数据集的 Hugging Face 页面进行了核查。之前的答案中至少有 3 个失效链接。

---

## Hugging Face 上已验证的金融数据集（2026 年 6 月）

我逐一检查了每个 URL。以下是实际存在的数据集，按训练阶段分类。

---

### 第一层级：预训练语料库（对标 FineWeb 的尝试）

**`kapilrao/SEC-EDGAR`** — 最接近金融领域 FineWeb 的数据集

- 590 GB，800 万个样本，**430 亿个 token**
- 包含所有主要的 SEC EDGAR 文件（10-K、10-Q、8-K 等）
- 合作方：Datamule、Teraflop AI、Eventual
- 这是 BloombergGPT 3630 亿 token 专有语料库在开放形式下的对应版本
- <https://huggingface.co/datasets/kapilrao/SEC-EDGAR>

**`eloukas/edgar-corpus`** — 学术版，规模更小、更干净

- 10-K 年度报告，1993-2020 年，**数十亿个 token**
- 论文：“EDGAR-CORPUS: Billions of Tokens Make The World Go Round”（EMNLP 2021）
- 获得 63 个赞 — 在金融 NLP 研究中广受认可
- <https://huggingface.co/datasets/eloukas/edgar-corpus>

**`Brianferrell787/financial-news-multisource`** — 大规模新闻语料库

- 来自 24 个公开数据集的 **5710 万行以上**数据，时间跨度为 1990-2025 年
- 统一格式 — 无需爬取
- 获得 80 个赞
- <https://huggingface.co/datasets/Brianferrell787/financial-news-multisource>

**`PleIAs/SEC`** — 经清洗的 SEC 文件文本

- 属于 PleIAs 的 common_corpus 集合
- <https://huggingface.co/datasets/PleIAs/SEC>

**`JanosAudran/financial-reports-sec`** — 带结构的已解析 10-K 文件

- 1993-2020 年的 10-K 文件，分为 20 个章节及句子
- 包含基于市场反应的情感标签
- 获得 77 个赞
- <https://huggingface.co/datasets/JanosAudran/financial-reports-sec>

---

### 第二层级：指令微调 / SFT

**`Josephgflowers/Finance-Instruct-500k`** — 最大的 SFT 集合

- **超过 50 万条**数据，多任务：推理、问答、命名实体识别、情感分析、多轮对话
- Apache 2.0 许可
- 将多个金融来源整合为一个
- <https://huggingface.co/datasets/Josephgflowers/Finance-Instruct-500k>

**`sujet-ai/Sujet-Finance-Instruct-177k`** — 精选多任务数据集

- 来自 18 个 Hugging Face 来源的 **177,597 条**数据
- 7 种任务类型：情感分析、问答、命名实体识别、摘要、分类等
- 获得 83 个赞
- <https://huggingface.co/datasets/sujet-ai/Sujet-Finance-Instruct-177k>

**`nvidia/Nemotron-SpecializedDomains-Finance-v1`** — NVIDIA 的合成问答数据集

- 来自 SEC 文件（标普 500 公司，2019-2024 年）的 **32.6 万以上问答对**
- 基于模板的 6 阶段合成数据生成
- **可用于商业的许可**
- <https://huggingface.co/datasets/nvidia/Nemotron-SpecializedDomains-Finance-v1>

**`FinGPT/fingpt-sentiment-train`** — 情感分析 SFT

- 金融新闻标题 + 情感标签
- 获得 36 个赞，FinGPT 组织有 1.16K 关注者
- <https://huggingface.co/datasets/FinGPT/fingpt-sentiment-train>

**`TheTokenFactory/sec-contracts-financial-extraction-instructions`** — 结构化提取

- 7,683 个指令示例，用于从 SEC 文件中提取结构化数据
- <https://huggingface.co/datasets/TheTokenFactory/sec-contracts-financial-extraction-instructions>

---

### 第三层级：数值推理 / 数学（用于 GRPO/DPO）

**`TheFinAI/FinCoT`** — 金融领域思维链推理

- GPT-4o 生成的推理路径，带有迭代验证
- 适合用作 GRPO 奖励信号
- <https://huggingface.co/datasets/TheFinAI/FinCoT>

**`ibm-research/finqa`** — IBM 的金融问答基准

- 基于金融表格/文本的数值推理
- 获得 14 个赞，引用广泛
- <https://huggingface.co/datasets/ibm-research/finqa>

**`yale-nlp/FinanceMath`** — 数理金融问题

- 获得 19 个赞，需同意后访问
- 涵盖 DCF、Black-Scholes、比率分析
- <https://huggingface.co/datasets/yale-nlp/FinanceMath>

**`virattt/financial-qa-10K`** — 基于 10-K 文件的问答

- 示例：NVIDIA 2023 年 10-K 问答对
- 适合训练模型阅读实际文件
- <https://huggingface.co/datasets/virattt/financial-qa-10K>

---

### 第四层级：基准测试与评估

**`SALT-NLP/FLUE-FiQA`** — FLUE 基准

- 金融语言理解评估
- FiQA 子任务：金融观点挖掘
- <https://huggingface.co/datasets/SALT-NLP/FLUE-FiQA>

**`yixuantt/FinEntity`** — 实体级情感分析（EMNLP 2023）

- 首个公开的金融领域实体级情感数据集
- 情感针对新闻中的特定实体
- <https://huggingface.co/datasets/yixuantt/FinEntity>

**`takala/financial_phrasebank`** — 经典情感分析基准

- 4,840 个句子，三分类（正面/负面/中性）
- 获得 259 个赞 — Hugging Face 上最受欢迎的金融情感数据集
- CC BY-NC-SA 3.0 许可
- <https://huggingface.co/datasets/takala/financial_phrasebank>

**`zeroshot/twitter-financial-news-sentiment`** — Twitter 金融情感

- 获得 173 个赞
- <https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment>

---

### 第五层级：结构化 / 市场数据

**`defeatbeta/yahoo-finance-data`** — 价格 + 基本面数据

- 来自 Yahoo Finance、Nasdaq、美国国债的数据
- 定期更新
- 获得 96 个赞
- <https://huggingface.co/datasets/defeatbeta/yahoo-finance-data>

**`glopardo/sp500-earnings-transcripts`** — 财报电话会议记录

- 标普 500 公司 2014-2024 年财报电话会议记录
- 结合季度财务指标
- 被欧洲央行工作论文使用
- <https://huggingface.co/datasets/glopardo/sp500-earnings-transcripts>

**`Josephgflowers/Financial-NER-NLP`** — 金融命名实体识别

- 源自 FiNER-139（110 万句子，139 个 XBRL 标签）
- 重新格式化为用于 LLM 训练的自然语言提示
- <https://huggingface.co/datasets/Josephgflowers/Financial-NER-NLP>

---

### 缺失部分（诚实评估）

目前**并没有一个单一的、对标 FineWeb 的金融数据集**。最接近的情况如下：

| 类比 | 是否存在？ | 替代方案 |
|---------|---------|---------------------|
| FineWeb（网页爬取 → 清洗） | 否 | `kapilrao/SEC-EDGAR`（430 亿 token 文件数据）+ `Brianferrell787/financial-news-multisource`（5710 万行新闻数据） |
| BigCode（The Stack） | 否 | 金融代码过于小众；使用通用代码 + 金融 SFT |
| Dolma（AI2 预训练混合） | 否 | 从上述数据集中自行构建混合 |

BloombergGPT 使用 3630 亿专有 token 进行训练。在开放数据中，仅 SEC-EDGAR 即可获得约 430 亿 token，外加约 5710 万行新闻数据。如果混合得当，总计大约 500-600 亿 token — 与 BloombergGPT 的语料库规模相当。

---

### 为你的 MI300X 推荐的堆栈

```python
# 预训练（领域自适应）
pretrain = [
    "kapilrao/SEC-EDGAR",                    # 430 亿 token，文件数据
    "Brianferrell787/financial-news-multisource",  # 5710 万行，新闻数据
]

# SFT
sft = [
    "Josephgflowers/Finance-Instruct-500k",  # 50 万条多任务数据
    "nvidia/Nemotron-SpecializedDomains-Finance-v1",  # 32.6 万合成问答，可商用
    "FinGPT/fingpt-sentiment-train",         # 情感分析
]

# 推理（GRPO/DPO）
reasoning = [
    "TheFinAI/FinCoT",                       # 思维链
    "ibm-research/finqa",                    # 数值问答
]

# 评估
eval_ds = [
    "takala/financial_phrasebank",           # 情感分析基准
    "SALT-NLP/FLUE-FiQA",                   # FLUE 基准
    "yixuantt/FinEntity",                    # 实体级情感
]
```

参考资料：

- [sugatoray/llm-datasets-finance 集合](https://huggingface.co/collections/sugatoray/llm-datasets-finance) — Hugging Face 上精选的金融数据集集合
- [adlnlp/FinLLMs GitHub 仓库](https://github.com/adlnlp/finllms) — 相关工作 + 基准测试列表
- [BloombergGPT 论文](https://arxiv.org/abs/2303.17564)
- [FINALE 论文（ACL 2024）](https://aclanthology.org/2024.finnlp-2.9.pdf) — 基于思维链原理的金融指令微调
