---
audio: false
generated: true
image: false
lang: en
layout: post
title: OOM Kill from Tokenizer RAM Spike
translated: false
type: note
---

That's the answer. The journal shows exactly what happened. Here's the diagnosis:

## What caused the "freeze" — it was an out-of-memory (OOM) kill, not a stuck loop

From `journalctl` on **Aug 13, 02:31:25**:

```
kernel: postgres invoked oom-killer ... cpuset=...app-ghostty...task=python3.12,pid=441877
kernel: Out of memory: Killed process 441877 (python3.12)
        total-vm:43106372kB, anon-rss:38136604kB   <-- ~43 GB VM, ~38 GB RSS
```

The process that got killed was `python3.12` **using ~38–43 GB of RAM** — that's your `train_tokenizer.py` run. `mixed.txt` was finished being built at 02:19, and the tokenizer job died at 02:31.

### Why it *looked* frozen instead of just crashing
Your machine has **62 GB RAM but only 2 GB swap**. As the trainer ballooned past ~40+ GB and ate into the page cache, the kernel had to constantly reclaim memory. With effectively no swap to spill to, the whole desktop started thrashing/gasping for memory — unresponsive for minutes — until the OOM killer finally stepped in and killed the python process (or you hard-rebooted first).

### Why the tokenizer ate ~40 GB
`tokenizers.ByteLevelBPETokenizer.train()` trains in Rust but builds a full **in-memory word-frequency table over the entire corpus** before doing merges. `mixed.txt` is **11.5 GB / 66.7 million lines** of mixed EN/ZH text. Counting* every unique token/word across 66M lines of a CJK-heavy corpus creates an enormous internal hash table — easily tens of GB well before the merge step. It's not an infinite loop; it's just genuinely consuming that much memory.

## How to fix it so it doesn't happen again

1. **Don't train the BPE on all 11.5 GB.** You don't need the full dataset to learn a 65K BPE vocab — a few hundred MB to ~1 GB *random sample* of `mixed.txt` gives essentially the same merges at a fraction of memory. Sample it first (e.g. `shuf -n` or `random.sample`).

2. **Add real swap** (2 GB is far too small for 62 GB RAM):
   ```bash
   sudo fallocate -l 32G /swapfile2 && sudo chmod 600 /swapfile2
   sudo mkswap /swapfile2 && sudo swapon /swapfile2
   ```
   Any future overshoot will spill to disk instead of freezing the laptop.

3. **Lower memory per run:** reduce `--vocab-size` or raise `--min-frequency`; both shrink the working set.

4. **If you must use the whole corpus,** switch to a more memory-efficient trainer like **SentencePiece** (its unigram/BPE trainer streams and uses far less RAM than `tokenizers`' byte-level trainer on 10GB+ inputs).

5. **Wrap it in a watchdog/progress log** so next time you can tell "working" from "thrashing" — e.g. run under `timeout` or print periodic RSS via `resource.getrusage`.

So: the laptop didn't have a bug, and the script wasn't infinitely stuck — **`train_tokenizer.py` ran out of RAM on an 11.5 GB corpus with only 2 GB of swap, the machine thrashed and appeared frozen, and the kernel OOM-killed the process.** Restarting was the only escape given the lack of swap. Sampling the input (and/or adding swap) will make it run to completion cleanly.