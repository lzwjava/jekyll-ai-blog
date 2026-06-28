---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenizer mismatch causes garbage output
translated: false
type: note
---

**Question:** The whole BST class is my prompt — the model only generated from `boolean search(int key) {` onward, and *everything* it produced is `.S.S.S` garbage. Why?

**Answer:**

Right — so the model generated **zero** coherent tokens. That changes the diagnosis entirely. This isn't repetition collapse late in generation; the model is incoherent from token one. That points to **the model genuinely doesn't know how to generate code** — undertrained, or worse, a checkpoint/data problem.

The `.S` attractor is just where a broken model's distribution dumps probability mass (`S` = high-frequency BPE token). The repetition penalty I mentioned won't help here because there's no good signal underneath to recover.

## The most likely culprit: BPE meta mismatch

Look at this line in your output:

```
No meta.pkl found, assuming GPT-2 encodings...
```

If you trained `out-github-code-124m` with a **custom tokenizer** (your own `meta.pkl`, char-level, or a code-specific BPE) but `sample.py` can't find it and falls back to **GPT-2 BPE**, then the token IDs the model learned mean something completely different from what `tiktoken` is feeding it. The model is being prompted in a foreign language. Output would look exactly like this — locally plausible fragments, globally nonsense.

Check:

```bash
ls -la /mnt/data/nanoGPT/data/*/meta.pkl
# and whatever your train data dir was
cat /mnt/data/nanoGPT/out-github-code-124m/config.* 2>/dev/null
# or inspect the checkpoint's saved config
python3 -c "
import torch
ck = torch.load('out-github-code-124m/ckpt.pt', map_location='cpu')
print('iter:', ck.get('iter_num'))
print('best_val_loss:', ck.get('best_val_loss'))
print('vocab_size:', ck['model_args'].get('vocab_size'))
print(ck.get('config'))
"
```

The two tells:

1. **`vocab_size`**. If it's `50304`/`50257` → GPT-2 BPE, and the fallback is correct, so the problem is training. If it's something else (e.g. `8192`, custom, or char-level ~`100`), then the GPT-2 fallback is wrong and that *alone* explains the garbage.

2. **`best_val_loss`**. For GPT-2 BPE on code, you want val loss roughly **< 2.0** for usable output, ideally ~1.5. If it's stuck at 3–5, the model never learned.

## Decision tree

```
vocab_size == 50257/50304 ?
├── NO  → tokenizer mismatch. Restore the right meta.pkl into out_dir
│         (or point sample.py at it). This is almost certainly your bug.
└── YES → check best_val_loss
          ├── > 3.0  → undertrained / diverged. Check loss curve.
          └── < 2.0  → should generate coherent code; if not, suspect
                        a corrupted/early checkpoint or wrong out_dir.
```

## If it's the tokenizer

nanoGPT loads `meta.pkl` from `out_dir` first, then falls back. Copy your training tokenizer's meta into the checkpoint dir:

```bash
# wherever your prepare.py wrote it
cp /mnt/data/nanoGPT/data/github_code/meta.pkl out-github-code-124m/
```

Then re-run sampling. If output snaps into real Java, that was it.

## If it's training

Pull the loss curve and look for divergence:

```bash
python3 -c "
import torch
ck = torch.load('out-github-code-124m/ckpt.pt', map_location='cpu')
print('iter', ck['iter_num'], 'val', ck['best_val_loss'])
"
```

124M on code, Chinchilla-optimal is ~2.5B tokens. If you stopped at, say, 50M tokens or a few thousand iterations, it's nowhere near coherent. Also check whether loss **diverged** (NaN/spike) — common on MI300X/ROCm with too-high LR or fp16 instability; try bf16 and lower LR.

## My bet

`No meta.pkl found, assuming GPT-2 encodings` + total incoherence from the first generated token = **tokenizer mismatch** is the strongest hypothesis. Verify `vocab_size` first; it's a 10-second check that resolves 80% of the probability mass. Run the checkpoint-inspection snippet above and paste the output if you want me to pin it down.

**References:**

- [nanoGPT sample.py — meta.pkl loading / GPT-2 fallback](https://github.com/karpathy/nanoGPT/blob/master/sample.py)
- [nanoGPT data prepare.py — where meta.pkl is written](https://github.com/karpathy/nanoGPT/blob/master/data/shakespeare_char/prepare.py)
