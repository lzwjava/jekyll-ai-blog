---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Tokenizer with Memory Cap
translated: false
type: note
---

Here's the command to run it on the 2 GB file with a bounded memory cap:

```bash
cd /mnt/data/bilingual-gpt

python3 scripts/train_tokenizer.py \
  --input mixed_sample_2gb.txt \
  --out-prefix tok_mixed    \
  --vocab-size 65536         \
  --max-bytes 200000000
```

**Notes:**

- `--max-bytes 200000000` = 200 MB sampling cap → peak RSS ~9 GB, safe. This is what I just validated successfully.
- `--out-prefix tok_mixed` writes `tok_mixed/vocab.json` + `tok_mixed/merges.txt`. Use a different prefix (e.g. `tok_sample`) if you don't want to overwrite the existing `tok_mixed/`.
- If you want a smaller/faster test, lower it (e.g. `--max-bytes 50000000` for 50 MB).
- **Avoid running with no `--max-bytes`** on the 2 GB file — that's what hung the machine (it needs ~35+ GB RAM).

Optional: watch memory while it runs:

```bash
watch -n2 "ps -o pid,rss,cmd -p \$(pgrep -f train_tokenizer.py | head -1)"
```
