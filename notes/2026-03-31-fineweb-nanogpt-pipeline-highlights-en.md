---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb to nanoGPT Pipeline Review Highlights
translated: false
type: note
---

Here's my detailed review of the whole setup:

---

## 🔍 Review: FineWeb → nanoGPT Pipeline on DigitalOcean

### The Good

1. **Streaming approach is correct.** Using `load_dataset(..., streaming=True)` avoids loading the full dataset into RAM. This is the right call for large datasets.

2. **HF works without proxy from DigitalOcean.** Confirmed — it started downloading immediately, no mirror needed.

3. **The pipeline concept is sound:** Download → Extract text → Tokenize → `train.bin`/`val.bin` → nanoGPT. This matches how Karpathy's original prepare.py works.

4. **Config looks reasonable.** GPT-2 124M (12L/12H/768d) with `sample-10BT` is a solid baseline. Your previous logs show it trained well on an RTX 4070.

---

### The Problems

**1. Server is too small for this job.**

- 1 vCPU, **1.9GB RAM**, 50GB disk
- The HF `datasets` library has ~500MB+ overhead even in streaming mode (parquet decompression, arrow buffers, python interpreter)
- It wrote 115MB / 1.3M lines before OOM-killed
- **Verdict:** This droplet can't handle the full `sample-10BT` download

**2. `--break-system-packages` is a hack.**

```bash
pip install --break-system-packages ...
```

This works but violates Ubuntu's PEP 668 policy. Future `apt` updates may break your packages. Better to use a venv:

```bash
python3 -m venv /root/zz/venv
source /root/zz/venv/bin/activate
pip install huggingface_hub datasets tiktoken numpy tqdm
```

**3. No HF token set.**

```
Warning: You are sending unauthenticated requests to the HF Hub.
```

Unauthenticated = rate-limited. For `sample-10BT` (~tens of GB), you'll hit limits fast. Add a token:

```bash
# Either:
export HF_TOKEN=hf_xxxxx
# Or:
huggingface-cli login
```

**4. The existing scripts in the repo are fragmented.**

- `wget_fineweb_*.sh` download raw parquet shards — redundant if using `datasets` streaming
- `extract_fineweb.py` reads parquet with pandas — redundant if streaming works
- `rename_fineweb.py` fixes `?download=true` suffixes — only needed for wget approach
- **You're maintaining two pipelines** (wget + HF library). Pick one and delete the other.

**5. Tokenizer mismatch risk.**

The existing `extract_fineweb.py` writes raw text. Your `prepare.py` needs to tokenize with GPT-2 BPE (`tiktoken`). Make sure:

- The tokenizer vocab matches (GPT-2 = 50,257 tokens → stored as `uint16`, max 65,535 ✅)
- `<|endoftext|>` is handled as a special token, not regular text
- No double-encoding (don't encode, then encode again)

**6. No `prepare.py` in the repo.**

The repo has download scripts and training logs, but **no tokenization script**. You need one. The one in the answer I gave earlier is correct, but it should live in the repo.

**7. Train config uses `max_iters=600000` but `sample-10BT` has ~10B tokens.**

At effective batch = 512 × 1024 = 524K tokens/iter:

- 600K iters × 524K tokens = **314B tokens** — way more than the dataset
- You'd need to set `max_iters` to ~19,000 (10B ÷ 524K) or loop the dataset
- Your previous `train_log_fineweb3.txt` used `max_iters=12000` which is ~6.3B tokens — more realistic

**8. No disk space check.**

`sample-10BT` raw text is ~20-30GB. Tokenized `train.bin` will be ~15-20GB. The 50GB disk will be tight. Check before downloading.

---

### Recommended Fix

| Issue | Fix |
| --- | --- |
| RAM too low | Resize to 4GB+ droplet, or download locally |
| No venv | `python3 -m venv venv && source venv/bin/activate` |
| No HF token | `huggingface-cli login` |
| Duplicate pipelines | Delete `wget_*.sh`, use `datasets` only |
| Missing prepare.py | Add the tokenizer script I wrote earlier |
| max_iters mismatch | Set to ~19K for 10BT, or ~12K if looping |
| Disk space | Check with `df -h` before downloading |

---

### Bottom Line

The approach is right, but the execution has rough edges: undersized server, no venv, no auth token, missing tokenizer script, and a config that assumes more data than you'll download. Clean those up and it'll work smoothly.

Want me to fix any of these on the server?
