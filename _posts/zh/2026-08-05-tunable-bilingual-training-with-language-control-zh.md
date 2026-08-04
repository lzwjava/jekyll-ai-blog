---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可调双语训练与语言控制
translated: true
type: note
---

**问题：** 如何构建一个带有可调语言比例参数的双语（英文/中文）训练集，为 nanoGPT/nanochat 做准备，并在生成时暴露一个语言控制旋钮？

**答案：**

**1. 选择数据源**

- 英文：`HuggingFaceFW/fineweb-edu`（sample-10BT 对于 nanoGPT 规模的训练来说足够了）
- 中文：`HuggingFaceFW/fineweb-2`（cmn_Hani 配置）或 `opencsg/chinese-fineweb-edu-v2` —— 后者约有 420B 个 token，基于 Qwen 的质量评分器，并包含 25% 的平行英文数据

两者都是 jsonl 格式的 `text` 分片，因此同一个脚本可以处理两者。

**2. 使用比例旋钮 + 语言控制 token 混合**

```python
#!/usr/bin/env python3
# mix_bilingual.py
import argparse, json, random

LANG_TOK = {"en": "<|lang_en|>", "zh": "<|lang_zh|>"}

def stream(path, key="text"):
    with open(path) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)[key]

def mix(en_path, zh_path, zh_frac, seed, limit):
    rng = random.Random(seed)
    en_it, zh_it = stream(en_path), stream(zh_path)
    n = 0
    while limit is None or n < limit:
        zh = rng.random() < zh_frac
        try:
            txt = next(zh_it) if zh else next(en_it)
        except StopIteration:
            break
        yield f"{LANG_TOK['zh' if zh else 'en']}\n{txt}"
        n += 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--en", required=True)
    ap.add_argument("--zh", required=True)
    ap.add_argument("--zh-frac", type=float, default=0.5)  # <- 这是你的分布参数
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    with open(a.out, "w") as f:
        for doc in mix(a.en, a.zh, a.zh_frac, a.seed, a.limit):
            f.write(doc + "\n<|endoftext|>\n")
```

`--zh-frac` 控制文档的采样概率。由于中文文档每个 token 对应的字符数更少，但字节数相似，因此在 tokenize 一次后测量实际的 token 比例，并调整 `zh_frac` —— 不要将文档计数当作 token 计数来使用。

**3. Tokenizer —— 不要为此使用 GPT-2 BPE**

GPT-2/tiktoken 的字节级 BPE 会将中文拆分为每个字符 3 个 token（UTF-8 字节回退），浪费上下文和计算资源。在混合语料上联合训练一个新的 BPE，使其能够形成真正的中文字符/词合并：

```python
from tokenizers import ByteLevelBPETokenizer
tok = ByteLevelBPETokenizer()
tok.train(files=["mixed.txt"], vocab_size=65536, min_frequency=2,
          special_tokens=["<|endoftext|>", "<|lang_en|>", "<|lang_zh|>"])
tok.save_model("tok_mixed")
```

如果你直接使用 nanochat，可以跳过这一步 —— 只需将 `tok_train.py` 指向混合分片目录（rustbpe 的训练方式相同，只需将控制 token 添加到其特殊 token 列表中）。

**4. nanoGPT 风格的 `prepare.py`**

```python
import numpy as np
from tokenizers import ByteLevelBPETokenizer

tok = ByteLevelBPETokenizer("tok_mixed/vocab.json", "tok_mixed/merges.txt")
vocab_size = tok.get_vocab_size()
dtype = np.uint16 if vocab_size < 65536 else np.uint32  # 如果词表大小 > 65535，注意此处

ids = tok.encode(open("mixed.txt").read()).ids
n = len(ids)
np.array(ids[: int(n*0.9)], dtype=dtype).tofile("train.bin")
np.array(ids[int(n*0.9):], dtype=dtype).tofile("val.bin")
print(vocab_size, n, dtype)
```

**5. nanochat 路径**

nanochat 涵盖了 tokenization、预训练、微调、评估和推理，全部在单个 GPU 节点上完成，`scripts/base_train.py` 通过 `nanochat.dataloader` 读取分片 —— 它从 `tokenizing_distributed_data_loader_bos_bestfit` 中提取数据。将你的 `mixed.txt` 分片（按照它期望的分片大小拆分）喂给它，而不是原始的 FineWeb-Edu，然后运行标准流程：

```bash
python -m scripts.tok_train --data_dir mixed_shards/
python -m scripts.base_train --depth=20
```

**6. 生成时的语言控制**

由于你为每个文档都添加了 `<|lang_en|>` / `<|lang_zh|>` 标签，模型学习了标签 → 条件分布映射（与 CTRL 的控制码 / NLLB 的语言 token 技巧相同）。通过在生成前添加标签来偏置生成：

```python
LANG_TOK = {"en": "<|lang_en|>", "zh": "<|lang_zh|>"}

def generate(model, tok, lang, prompt, max_new_tokens=200, temperature=0.8):
    ids = tok.encode(f"{LANG_TOK[lang]}\n{prompt}").ids
    x = torch.tensor([ids], device=device)
    y = model.generate(x, max_new_tokens=max_new_tokens, temperature=temperature)
    return tok.decode(y[0].tolist())
```

**7. 如果你想要一个连续混合比例旋钮（不仅仅是二元的 en/zh）**

二元标签只能给你“纯英文”或“纯中文”输出。要实现真正的连续旋钮，你需要带有标注比例的代码切换训练文档。取一个平行英中语料库（例如 WMT News Commentary zh-en），按选定比例 `r` 交错句子，并加上一个分桶的控制标签：

```python
buckets = [0, 25, 50, 75, 100]
tag = f"<|mix_{min(buckets, key=lambda b: abs(b - r*100))}|>"
```

在这些分桶示例上进行训练，然后在生成时 `<|mix_75|>` 会使输出偏向约 75% 的中文句子交错。这需要句子级别的双语数据（而不仅仅是单语的 FineWeb）—— 这才是真正的限制，而不是建模本身。

参考资料：

- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [nanochat scripts/base_train.py](https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py)
- [HuggingFaceFW/fineweb-2（多语言，包含 cmn_Hani）](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2)
- [opencsg/chinese-fineweb-edu-v2](https://opencsg.com/datasets/OpenCSG/chinese-fineweb-edu-v2)
- [CLUECorpus2020 论文](https://arxiv.org/pdf/2003.01355)
