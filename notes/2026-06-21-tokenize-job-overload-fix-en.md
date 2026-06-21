---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tokenize Job Overload Fix
translated: false
type: note
---

OK, here's the situation:

1. The machine is alive (ping works, port 22 is open)
2. sshd accepts TCP but never sends its SSH banner — classic sign of severe memory/CPU starvation
3. This is almost certainly caused by the tokenize job itself

Looking at the script, I see the likely culprits:

ISSUE 1 — MEMORY EXPLOSION:
The script spawns 16 workers via `mp.Pool`. Each worker calls `pq.read_table()` which loads an entire parquet file into memory (~270MB each for 10GB/38 files), then builds a massive Python list via `all_tokens.extend(tokens)`. 16 workers in parallel = easily 5-10+ GB of RAM just for the workers, plus the main process. If the machine has limited RAM, this will either OOM-kill workers silently (making `pool.imap` hang forever) or cause extreme swap thrashing that freezes the system.

ISSUE 2 — COLUMN NAME MISMATCH (potential):
Line 2 of the docstring says "Tokenizes 'code' column" but line 37 reads `columns=["content"]`. If the parquet files actually use a `code` column, each worker would crash with a `KeyError`, the pool would hang, and the main process would sit there forever waiting on `pool.imap`.

ISSUE 3 — HANGING mp.Pool:
If any worker crashes (OOM, KeyError, etc.), `pool.imap` can silently hang in Python — no error, no output, just... nothing. This matches the symptom of "prints 'Tokenizing with 16 workers...' then nothing."

WHAT TO DO:

You need to physically go to the machine (or wait for it to swap enough to respond). Once there:

1. Check if the process is still running or crashed:
   ps aux | grep tokenize

2. Check dmesg for OOM kills:
   dmesg | tail -20

3. Check the actual column name in the parquet files:
   python3.11 -c "import pyarrow.parquet as pq; t = pq.read_table('/mnt/data/zz/datasets/github-code/0000.parquet'); print(t.schema.names)"

4. Then either:
   - Reduce workers: --workers 2
   - Or I can fix the script to use streaming (pq.ParquetFile + iter_batches) instead of loading entire files into memory

Yes — you need to stand up and go check. The machine is too overloaded to SSH into. Once you can see the screen, check `dmesg | tail` and `free -h` first. If it's OOM, just kill the python process and I'll fix the script to be memory-efficient before you rerun it.
