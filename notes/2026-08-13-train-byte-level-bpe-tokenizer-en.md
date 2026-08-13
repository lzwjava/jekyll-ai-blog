---
audio: false
generated: true
image: false
lang: en
layout: post
title: Train Byte-Level BPE Tokenizer
translated: false
type: note
---

The script trains a fresh byte-level BPE tokenizer on your mixed corpus. To use `mixed_sample_2gb.txt`, just pass it as `--input`:

```bash
python -m scripts.train_tokenizer \
    --input mixed_sample_2gb.txt \
    --out-prefix tok_mixed \
    --vocab-size 65536
```

### What this does

- Trains a **byte-level BPE** tokenizer jointly on the mixed EN/ZH data, so Chinese gets real char/word merges instead of ~3 tokens/char.
- Registers control tokens (`<|endoftext|>`, `<|lang_en|>`, `<|lang_zh|>`, plus `<|mix_0|>`..`<|mix_100|>`) as special tokens so they're never split.
- Saves a tokenizer directory (`tok_mixed/`) containing `vocab.json` + `merges.txt`.

### Options

| Flag | Default | Purpose |
| ------ | --------- | --------- |
| `--input` | (required) | path to a file, or a directory of `.txt`/`.jsonl` shards |
| `--out-prefix` | `tok_mixed` | output dir name |
| `--vocab-size` | `65536` | vocab size (keep ≤65536 so `prepare.py` stays on uint16) |
| `--min-frequency` | `2` | min pair frequency to merge |
| `--special-tokens` | default list | override special tokens |

### Notes

- It also accepts a **directory** of shards, so you could point it at your shard dir instead of a single file.
- The script's docstring notes: if you're going through **nanochat**, skip this script and use nanochat's `tok_train.py` on the mixed shard dir (it uses the same rustbpe), just add the control tokens to its special-token list.

Want me to run it now with `mixed_sample_2gb.txt`?
