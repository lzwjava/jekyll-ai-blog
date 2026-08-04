---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tunable Bilingual Training with Language Control
translated: false
type: note
---

Question: How do I build a bilingual (English/Chinese) training set with a tunable language-ratio parameter, prep it for nanoGPT/nanochat, and expose a language-control knob at generation time?

Answer:

**1. Pick sources**

- EN: `HuggingFaceFW/fineweb-edu` (sample-10BT is plenty for a nanoGPT-scale run)
- ZH: `HuggingFaceFW/fineweb-2` (cmn_Hani config) or `opencsg/chinese-fineweb-edu-v2` — it's ~420B tokens with a Qwen-based quality scorer and includes 25% parallel English data

Both are jsonl-with-`text` shards, so the same script works for either.

**2. Mix with a ratio knob + language control-tokens**

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
    ap.add_argument("--zh-frac", type=float, default=0.5)  # <- this is your distribution param
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    with open(a.out, "w") as f:
        for doc in mix(a.en, a.zh, a.zh_frac, a.seed, a.limit):
            f.write(doc + "\n<|endoftext|>\n")
```

`--zh-frac` controls doc-sampling probability. Since Chinese docs tokenize to fewer *characters* per token but similar bytes, measure actual token ratio after tokenizing once and nudge `zh_frac` — don't trust doc-count as a token-count proxy.

**3. Tokenizer — don't use GPT-2 BPE for this**

GPT-2/tiktoken byte-BPE fragments Chinese into 3 tokens/char (UTF-8 byte-fallback), wasting context and compute. Train a fresh BPE jointly on the mixed corpus so it can form real Chinese-char/word merges:

```python
from tokenizers import ByteLevelBPETokenizer
tok = ByteLevelBPETokenizer()
tok.train(files=["mixed.txt"], vocab_size=65536, min_frequency=2,
          special_tokens=["<|endoftext|>", "<|lang_en|>", "<|lang_zh|>"])
tok.save_model("tok_mixed")
```

If you're going through nanochat directly, skip this step — just point `tok_train.py` at the mixed shard dir (rustbpe trains the same way, it just needs the control tokens added to its special-token list).

**4. nanoGPT-style `prepare.py`**

```python
import numpy as np
from tokenizers import ByteLevelBPETokenizer

tok = ByteLevelBPETokenizer("tok_mixed/vocab.json", "tok_mixed/merges.txt")
vocab_size = tok.get_vocab_size()
dtype = np.uint16 if vocab_size < 65536 else np.uint32  # watch this if vocab > 65535

ids = tok.encode(open("mixed.txt").read()).ids
n = len(ids)
np.array(ids[: int(n*0.9)], dtype=dtype).tofile("train.bin")
np.array(ids[int(n*0.9):], dtype=dtype).tofile("val.bin")
print(vocab_size, n, dtype)
```

**5. nanochat path**

nanochat covers tokenization, pretraining, finetuning, evaluation, and inference on a single GPU node, with `scripts/base_train.py` reading shards via `nanochat.dataloader` — it pulls from `tokenizing_distributed_data_loader_bos_bestfit`. Feed it your `mixed.txt` shards (split into the shard sizes it expects) instead of raw FineWeb-Edu, then run the normal pipeline:

```bash
python -m scripts.tok_train --data_dir mixed_shards/
python -m scripts.base_train --depth=20
```

**6. Generation-time language control**

Because you tagged every doc with `<|lang_en|>` / `<|lang_zh|>`, the model learns the tag → conditional distribution mapping (same trick as CTRL's control codes / NLLB's language tokens). Bias generation by prepending the tag:

```python
LANG_TOK = {"en": "<|lang_en|>", "zh": "<|lang_zh|>"}

def generate(model, tok, lang, prompt, max_new_tokens=200, temperature=0.8):
    ids = tok.encode(f"{LANG_TOK[lang]}\n{prompt}").ids
    x = torch.tensor([ids], device=device)
    y = model.generate(x, max_new_tokens=max_new_tokens, temperature=temperature)
    return tok.decode(y[0].tolist())
```

**7. If you want a continuous mixing-ratio knob (not just binary en/zh)**

Binary tags only give you "pure EN" or "pure ZH" output. For a real continuous knob you need code-switched training docs with a labeled ratio. Take a parallel EN-ZH corpus (WMT News Commentary zh-en), interleave sentences at a chosen ratio `r`, and prefix with a bucketed control tag:

```python
buckets = [0, 25, 50, 75, 100]
tag = f"<|mix_{min(buckets, key=lambda b: abs(b - r*100))}|>"
```

Train on these bucketed examples, then at generation time `<|mix_75|>` biases output toward ~75% Chinese sentence interleaving. This needs sentence-aligned bilingual data (not just monolingual FineWeb) — that's the real constraint, not the modeling.

References:
- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [nanochat scripts/base_train.py](https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py)
- [HuggingFaceFW/fineweb-2 (multilingual, includes cmn_Hani)](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2)
- [opencsg/chinese-fineweb-edu-v2](https://opencsg.com/datasets/OpenCSG/chinese-fineweb-edu-v2)
- [CLUECorpus2020 paper](https://arxiv.org/pdf/2003.01355)