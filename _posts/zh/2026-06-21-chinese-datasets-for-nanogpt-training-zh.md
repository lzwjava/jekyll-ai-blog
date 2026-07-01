---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于nanoGPT训练的中文数据集
translated: true
type: note
---

**问题：** 我们能用哪些中文数据集来训练 nanoGPT？**问题：** 哪些中文数据集可用于训练 nanoGPT？

**答案：**

对于 nanoGPT 规模的训练（字符/BPE 分词器、单 GPU、快速迭代），你需要干净、易于分词、且分块大小适中的数据集。以下是按实际用途排序的完整资源图景：

---

## 第一梯队 — 从这里开始（nanoGPT 就绪）

### 1. 中文维基百科转储

经典起点。干净、结构化，约 1.6GB / 约 0.4B 个 token。

```bash
# 通过 HuggingFace datasets 下载
pip install datasets
python -c "
from datasets import load_dataset
ds = load_dataset('wikipedia', '20231101.zh', split='train')
ds.to_json('zh_wiki.jsonl')
"
```

优势：快速启动、干净的散文、多样的主题。对于严肃的预训练来说太小，但非常适合 nanoGPT 实验。

### 2. `thu-coai/zh_cls_fudan-news` / THUCTC

74 万篇新闻文章，干净的中文。良好的领域特定语料库。

### 3. CLUECorpus2020

从 Common Crawl 过滤出的 100GB 中文网络文本。适用于中等规模运行。

- HuggingFace: `clue/clue_corpus_small_14g`（14GB 子集）

```bash
python -c "
from datasets import load_dataset
ds = load_dataset('clue', 'clue_corpus_small_14g')
"
```

---

## 第二梯队 — 更高质量，更多工作

### 4. **Fineweb-Edu-Chinese**（OpenCSG）

在 C-Eval 和 CMMLU 基准测试上经过验证，预训练期间精度提升显著 — 目前最高质量的中文网络语料库。

```bash
# HuggingFace: opencsg/Fineweb-Edu-Chinese
from datasets import load_dataset
ds = load_dataset("opencsg/Fineweb-Edu-Chinese", split="train", streaming=True)
```

包含 1.88 亿个文本，约 420B 个 token，通过教育价值评分模型过滤，阈值为 3 分。对于完整加载 nanoGPT 来说太大 — 请流式传输子集。

### 5. **MAP-CC**

开源中文预训练数据集，包含 800B 个 token，并提供了清洗中文网络语料库的详细流程。对于 nanoGPT 来说过于庞大，但如果你打算扩展到 MI300X 则非常出色。

### 6. **SkyPile / WuDao / YaYi**

YaYi、SkyPile 和 WuDao 精心整理了开源内容 — 但数量有限。WuDao 规模大但存在质量一致性问题以及换行符格式问题。

---

## 第三梯队 — 特定用途

### 7. **Cosmopedia-Chinese**（OpenCSG）

合成教科书风格数据，非常适合指令跟随。更适合微调而非原始预训练。

### 8. **百度百科**

百度百科语料库几乎涵盖所有知识领域，与维基百科相当但大了 10 倍。HuggingFace 上存在抓取版本。

---

## 中文 nanoGPT 的实际设置

与英文 nanoGPT 的关键区别：**分词**。字符级别可行但效率较低（中文汉字 = 1 个 token，还算合理）。使用中文词表的 BPE（例如来自 `sentencepiece`）效果更好。

```python
# 最小字符级预处理（类似 nanoGPT 的 shakespeare_char）
import json

texts = []
with open("zh_wiki.jsonl") as f:
    for line in f:
        obj = json.loads(line)
        texts.append(obj["text"])

corpus = "\n".join(texts)
chars = sorted(set(corpus))
print(f"词表大小: {len(chars)}")  # 中文汉字约 5000-8000

# 编码/解码
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s if c in stoi]
decode = lambda l: ''.join([itos[i] for i in l])
```

或者使用 `tiktoken` / `sentencepiece` 配合中文感知的分词器：

```bash
pip install sentencepiece
python -c "
import sentencepiece as spm
spm.SentencePieceTrainer.train(
    input='zh_wiki.txt',
    model_prefix='zh_bpe',
    vocab_size=8000,
    character_coverage=0.9995,  # 对中文至关重要
    model_type='bpe'
)
"
```

---

## 我对你设置的建议

| 目标 | 数据集 | 大小 |
| ------ | -------- | ------ |
| 快速实验 (RTX 4070) | 中文维基百科 | ~1.6GB |
| 中等规模运行 (RTX 4070) | CLUECorpus small | ~14GB |
| 严肃预训练 (MI300X) | Fineweb-Edu-Chinese | ~420B 个 token |
| 质量优先 | MAP-CC 子集 | 可配置 |

从中文维基百科开始 → 验证训练循环正常 → 扩展到 CLUECorpus → 如果想在 MI300X 上推进，使用 `streaming=True` 流式传输 Fineweb-Edu-Chinese。

**参考资料：**

- [OpenCSG 中文语料库论文](https://huggingface.co/papers/2501.08197)
- [中文 Tiny LLM 预训练综述](https://arxiv.org/html/2404.04167v1)
- [OpenCSG 数据集对比（Medium）](https://medium.com/@OpenCSG/what-datasets-are-available-for-chinese-large-models-heres-our-complete-comparative-analysis-0c0ad2bff74f)
- [Fineweb-Edu-Chinese 在 HuggingFace 上](https://huggingface.co/datasets/opencsg/Fineweb-Edu-Chinese)
- [CLUECorpus2020](https://huggingface.co/datasets/clue)
