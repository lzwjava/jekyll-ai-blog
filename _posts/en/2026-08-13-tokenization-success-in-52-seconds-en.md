---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenization Success in 52 Seconds
translated: false
type: note
---

Done — it finished cleanly in **52 seconds** (no OOM, no hang).

## Result
- **Output:** `tok_mixed/` (`vocab.json` + `merges.txt`)
- **Vocab size:** 65536
- **Specials** preserved losslessly: `<|endoftext|>`, `<|lang_en|>`, `<|lang_zh|>`, `<|mix_0|>`, …, `<|mix_100|>`

```bash
ls -la tok_mixed/
```

## Notes
- The `WARNING: vocab > 65535` is fine — it just means `prepare.py` will use `uint32` and produce slightly larger `.bin` files. If you want the more compact `uint16` binaries, re-run with `--vocab-size 65536`... wait, that's the same. To stay at 65535 you'd use `--vocab-size 65535` (or lower). It's purely a file-size tradeoff, not a correctness issue.
- 200 MB gave a very fast, low-memory run. If you later find the merges under-train on rarer subwords, you can move up to the 2 GB sample — it's just memory-vs-quality tuning.

Want me to check the vocab contains proper Chinese char merges (sanity check the joint BPE worked) or fix the uint32/uint16 warning?