---
audio: false
generated: true
image: false
lang: en
layout: post
title: New Max-Chars Length Control
translated: false
type: note
---

Done. Yes — you can control output length, two ways now:

## Two length controls in `scripts/mix_bilingual.py`

| Option | Controls | Example |
|--------|----------|---------|
| `--limit N` | Max **documents** written (already existed) | `--limit 2000` |
| `--max-chars N` | Total output **length in characters** (new) | `--max-chars 100000` |

## New `--max-chars`

- Stops writing once the accumulated output (docs + control tokens + newlines) exceeds `N` characters.
- Works alongside or without `--limit` (whichever trips first wins).
- Tested: `--max-chars 500` → wrote 7 docs (566 chars) and stopped.

Your command becomes:

```bash
python3.12 -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0 \
    --max-chars 1000000
```

Two caveats worth knowing:

- `--max-chars` counts **characters**, so Chinese text (multi-byte UTF-8) yields a larger byte size on disk. If you specifically need a byte/like-token cap instead, I can switch it to count UTF-8 bytes (`len(txt.encode("utf-8"))`) or add both options.
- `--max-chars` reads the source generators and writes docs greedily, so it stops at the **first doc boundary past** the cap (it never truncates mid-document). That keeps every output line a valid wrapped doc.

Want me to also add `--max-bytes` (UTF-8 byte cap), or is the char-based cap what you needed?
