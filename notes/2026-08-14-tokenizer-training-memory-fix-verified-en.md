---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenizer Training Memory Fix Verified
translated: false
type: note
---

Done. Here's the summary:

## ✅ Fixed, patched, and verified

### Changes to `scripts/train_tokenizer.py`

- **`--max-bytes N`** option added (default `None` = unlimited, so behavior is unchanged unless you pass it).
- Switched from `tok.train(files=...)` to **`tok.train_from_iterator(...)`** with a streaming generator that reads files **line by line** and stops once ~`N` bytes have been consumed — so the corpus is never fully loaded into memory.

### Safe test on the 2 GB file

Ran with `--max-bytes 200000000` (200 MB) plus a memory monitor:

| Metric | Before (2 GB, no cap) | After (200 MB cap) |
| --- | --- | --- |
| Peak RSS | ~35 GB and climbing (killed) | **~9.1 GB** |
| System available | crashed (54→13 GB then freeze) | steady ~42 GB, healthy |
| Result | never finished (hung) | **completed, vocab size 65536** |

Output written to `/tmp/toktest/out2/` (`vocab.json` 1.2 MB + `merges.txt` 783 KB), special tokens intact:

```
<|endoftext|> <|lang_en|> <|lang_zh|> <|mix_0|> <|mix_25|> <|mix_50|> <|mix_75|> <|mix_100|>
```

### Recommendation

- For a real run on the full 11.5 GB `mixed.txt`, use `--max-bytes` at **~150–200 MB** (a 65k BPE doesn't need more; exactly what we just validated). That should limit peak RSS to roughly ~9–10 GB — well within your 62 GB.
- On the box now: 49 GB available, swap back down to 6.5 GB used (from the earlier stress), all normal.

The earlier freeze was **not a code bug** — it was `tok.train()` loading the whole 2 GB corpus into the Rust trainer (~18× file size in RAM) and thrashing the machine into OOM. This is now avoidable.
