---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face上最佳金融数据集
translated: true
type: note
---

**问题：** Hugging Face 上哪些金融领域数据集最适合训练 LLM，类似于代码领域的 BigCode 或通用文本领域的 FineWeb？

**回答：**

## Hugging Face 上的金融数据集 —— 按用例分层

### 第一层：大规模预训练语料

**[financial-datasets/financial-reports](https://huggingface.co/datasets/financial-datasets/financial-reports)**

- SEC 文件（10-K、10-Q、8-K）、财报电话会议记录
- 适用于对正式金融语言进行领域自适应预训练

**[Sujet-Finance/Sujet-Finance-Instruct-177k](https://huggingface.co/datasets/Sujet-Finance/Sujet-Finance-Instruct-177k)**

- 17.7 万条指令对，涵盖情感分析、问答、命名实体识别、摘要
- 金融专用指令微调

**[TheFinAI/Fino1_Reasoning_Path](https://huggingface.co/datasets/TheFinAI/Fino1_Reasoning_Path)**

- 金融问题的思维链推理轨迹
- 适合用于数值推理的 GRPO/DPO

---

### 第二层：任务专用 SFT 数据

| 数据集 | 大小 | 用途 |
|---|---|---|
| `zeroshot/twitter-financial-news-sentiment` | ~1.1 万 | 情感分析（FinSentiment） |
| `nickmuchi/financial-classification` | ~5000 | 新闻分类 |
| `FinGPT/fingpt-sentiment-train` | ~7.6 万 | 情感 SFT（FinGPT 风格） |
| `FinGPT/fingpt-forecaster` | ~20 万 | 价格走势预测 |
| `FinGPT/fingpt-fiqa_qa` | ~1.7 万 | 金融问答（FiQA） |
| `TheFinAI/flare-fiqasa` | ~1000 | 少样本问答基准 |

FinGPT 组织拥有最完整的 SFT 集合：`huggingface.co/FinGPT`

---

### 第三层：原始金融文本（用于预训练）

**SEC EDGAR 全文** —— 不直接在 HF 上，但可通过以下方式获取：

```bash
# Edgar 全文搜索批量下载
wget https://efts.sec.gov/LATEST/search-index?q=%22%22&dateRange=custom&startdt=2020-01-01&enddt=2024-01-01&_source=file_date,period_of_report,entity_name,file_num,form_type&hits.hits._source=true
```

更好的方法：使用 `edgartools` Python 库：

```bash
pip install edgartools
```

```python
from edgar import Company
c = Company("AAPL")
filings = c.get_filings(form="10-K")
text = filings[0].obj().text  # 原始 10-K 文本
```

**[eloukas/edgar-corpus](https://huggingface.co/datasets/eloukas/edgar-corpus)**

- 6500 多份 10-K 年度报告（2000–2020 年）
- 约 2.5 亿个 token 的正式 SEC 文本

---

### 第四层：数值 / 量化金融

**[TheFinAI/flare-sm-acl18](https://huggingface.co/datasets/TheFinAI/flare-sm-acl18)**

- 利用新闻标题 + 价格方向进行股票走势预测

**[luqia/FinanceMath](https://huggingface.co/datasets/luqia/FinanceMath)**

- 金融数学应用题及解答
- 适合训练模型进行 DCF、Black-Scholes 等计算

---

### BigCode 在金融领域的对应情况

BigCode 的价值在于 **规模 + 去重 + 质量过滤**。金融领域尚无同等水平的资源。目前最接近的正在构建的资源：

- **FinPile**（论文，尚未公开）—— 13 亿 token 的金融语料
- **BloombergGPT 在** 3630 亿 token 的专有语料上训练 —— 其数据从未公开

因此诚实的答案是：**金融领域没有 FineWeb 的等价物**。你需要自行从以下内容构建：

```
EDGAR 10-K/10-Q/8-K (eloukas/edgar-corpus)     ~2.5 亿 token
财报电话会议记录 (Motley Fool, SA)               ~1 亿 token
财经新闻 (Reuters, Bloomberg 头条)               ~5000 万 token
金融教材 / CFA 资料 (PDF 爬取)                   ~2000 万 token
FinGPT SFT 数据 (用于对齐)                       ~50 万对
```

---

### 针对你的设置推荐流程

考虑到你使用 MI300X 以及拥有 nanoGPT 的训练经验：

```python
# 快速领域自适应预训练栈
datasets = [
    "eloukas/edgar-corpus",           # 预训练主干
    "FinGPT/fingpt-sentiment-train",  # SFT 层
    "TheFinAI/Fino1_Reasoning_Path",  # 用于 GRPO 的推理轨迹
]

# 加载并混合
from datasets import load_dataset, interleave_datasets

edgar = load_dataset("eloukas/edgar-corpus", split="train")
fingpt = load_dataset("FinGPT/fingpt-sentiment-train", split="train")

mixed = interleave_datasets([edgar, fingpt], probabilities=[0.8, 0.2])
```

对于银行 AI 用例（你的背景）：预训练阶段侧重 EDGAR + 财报电话会议，然后对 FinGPT 情感/问答进行 SFT，最后对 Fino1 推理轨迹进行 DPO/GRPO。这是目前开放数据中可用的最接近生产级金融 LLM 的堆栈。

**参考文献：**

- [FinGPT datasets on HuggingFace](https://huggingface.co/FinGPT)
- [eloukas/edgar-corpus](https://huggingface.co/datasets/eloukas/edgar-corpus)
- [TheFinAI/Fino1_Reasoning_Path](https://huggingface.co/datasets/TheFinAI/Fino1_Reasoning_Path)
- [Sujet-Finance-Instruct-177k](https://huggingface.co/datasets/Sujet-Finance/Sujet-Finance-Instruct-177k)
- [BloombergGPT paper](https://arxiv.org/abs/2303.17564)
