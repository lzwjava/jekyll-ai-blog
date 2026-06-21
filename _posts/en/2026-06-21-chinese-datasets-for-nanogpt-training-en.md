---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Datasets for nanoGPT Training
translated: false
type: note
---

**Question:** What Chinese datasets can we use to train nanoGPT?**Question:** What Chinese datasets can be used to train nanoGPT?

**Answer:**

For nanoGPT-scale training (character/BPE tokenizer, single GPU, fast iteration), you want datasets that are clean, easily tokenizable, and come in manageable chunks. Here's the full landscape ranked by practical utility for your use case:

---

## Tier 1 — Start Here (nanoGPT-ready)

### 1. Chinese Wikipedia Dump

The classic starting point. Clean, structured, ~1.6GB / ~0.4B tokens.

```bash
# Download via HuggingFace datasets
pip install datasets
python -c "
from datasets import load_dataset
ds = load_dataset('wikipedia', '20231101.zh', split='train')
ds.to_json('zh_wiki.jsonl')
"
```

Good for: fast bootstrapping, clean prose, diverse topics. Too small for serious pretraining but perfect for nanoGPT experiments.

### 2. `thu-coai/zh_cls_fudan-news` / THUCTC

740K news articles, clean Chinese. Good domain-specific corpus.

### 3. CLUECorpus2020

100GB of Chinese web text filtered from Common Crawl. Practical for medium-scale runs.

- HuggingFace: `clue/clue_corpus_small_14g` (14GB subset)

```bash
python -c "
from datasets import load_dataset
ds = load_dataset('clue', 'clue_corpus_small_14g')
"
```

---

## Tier 2 — Higher Quality, More Work

### 4. **Fineweb-Edu-Chinese** (OpenCSG)

Validated on C-Eval and CMMLU benchmarks, showing sharp accuracy gains during pretraining — the highest quality Chinese web corpus right now.

```bash
# HuggingFace: opencsg/Fineweb-Edu-Chinese
from datasets import load_dataset
ds = load_dataset("opencsg/Fineweb-Edu-Chinese", split="train", streaming=True)
```

188 million texts, ~420B tokens, filtered by an educational value scoring model with a 3-point threshold. Way too big for nanoGPT in full — stream a subset.

### 5. **MAP-CC**

Open-source Chinese pretraining dataset with 800B tokens, with detailed procedures for cleaning Chinese web corpora. Overkill for nanoGPT but excellent if you want to scale up to your MI300X.

### 6. **SkyPile / WuDao / YaYi**

YaYi, SkyPile, and WuDao meticulously curate open-source content — though limited in quantity. WuDao is large but has quality consistency issues and formatting problems with line breaks.

---

## Tier 3 — Targeted Use Cases

### 7. **Cosmopedia-Chinese** (OpenCSG)

Synthetic textbook-style data, great for instruction following. Better for fine-tuning than raw pretraining.

### 8. **Baidu Baike**

The Baidu Baike corpus covers nearly all knowledge domains, comparable to Wikipedia but 10x larger. Scraped versions exist on HuggingFace.

---

## Practical nanoGPT Setup for Chinese

The key difference from English nanoGPT: **tokenization**. Character-level works but inefficient (Chinese char = 1 token, reasonable). BPE with a Chinese vocab (e.g. from `sentencepiece`) is better.

```python
# Minimal character-level prep (like nanoGPT's shakespeare_char)
import json

texts = []
with open("zh_wiki.jsonl") as f:
    for line in f:
        obj = json.loads(line)
        texts.append(obj["text"])

corpus = "\n".join(texts)
chars = sorted(set(corpus))
print(f"Vocab size: {len(chars)}")  # ~5000-8000 for Chinese chars

# encode / decode
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s if c in stoi]
decode = lambda l: ''.join([itos[i] for i in l])
```

Or use `tiktoken` / `sentencepiece` with a Chinese-aware tokenizer:

```bash
pip install sentencepiece
python -c "
import sentencepiece as spm
spm.SentencePieceTrainer.train(
    input='zh_wiki.txt',
    model_prefix='zh_bpe',
    vocab_size=8000,
    character_coverage=0.9995,  # critical for Chinese
    model_type='bpe'
)
"
```

---

## My Recommendation for Your Setup

| Goal | Dataset | Size |
|------|---------|------|
| Quick experiment (RTX 4070) | Chinese Wikipedia | ~1.6GB |
| Medium run (RTX 4070) | CLUECorpus small | ~14GB |
| Serious pretraining (MI300X) | Fineweb-Edu-Chinese | ~420B tokens |
| Quality over quantity | MAP-CC subset | configurable |

Start with Chinese Wikipedia → verify your training loop works → scale to CLUECorpus → if you want to push on MI300X, stream Fineweb-Edu-Chinese with `streaming=True`.

**References:**

- [OpenCSG Chinese Corpus paper](https://huggingface.co/papers/2501.08197)
- [Chinese Tiny LLM pretraining survey](https://arxiv.org/html/2404.04167v1)
- [OpenCSG dataset comparison (Medium)](https://medium.com/@OpenCSG/what-datasets-are-available-for-chinese-large-models-heres-our-complete-comparative-analysis-0c0ad2bff74f)
- [Fineweb-Edu-Chinese on HuggingFace](https://huggingface.co/datasets/opencsg/Fineweb-Edu-Chinese)
- [CLUECorpus2020](https://huggingface.co/datasets/clue)
