---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing CLI Agent Performance Tradeoffs
translated: false
type: note
---

**Question:** For a minimal OpenCode/Claude Code CLI agent, Python vs Rust speed difference is negligible since the bottleneck is LLM API latency — but shouldn't we still profile? And for data-heavy (big Excel) or compute-heavy workloads, Rust could be meaningfully faster, right?

**Answer:**

Yes, exactly right on all counts. Let me break this down precisely.

## The Bottleneck Hierarchy

For an LLM agent CLI, the latency stack looks like this:

```
LLM API call:        2,000 – 30,000 ms   ← dominates everything
Network I/O:         50 – 500 ms
File I/O:            1 – 50 ms
JSON parsing:        0.1 – 5 ms
Python startup:      50 – 150 ms         ← actually visible on CLI!
Rust startup:        1 – 5 ms
```

So for a Claude Code-style tool, **Python startup latency is the only real gap** — and even that's only felt if you invoke the binary hundreds of times in tight loops (like a shell loop calling the agent per-file).

---

## Where Rust Actually Wins

### 1. Big Excel / Data Processing

Excel files via `openpyxl` in Python are notoriously slow on large sheets:

```python
# Python: openpyxl reading 100k rows — can take 10-30s
import openpyxl
wb = openpyxl.load_workbook("big.xlsx")  # slow, memory heavy
```

Rust with `calamine` crate reads the same in <1s:

```rust
use calamine::{open_workbook, Reader, Xlsx};

let mut wb: Xlsx<_> = open_workbook("big.xlsx").unwrap();
let sheet = wb.worksheet_range("Sheet1").unwrap();
for row in sheet.rows() {
    // processes 100k rows in ~200ms
}
```

Python workaround: use `pandas` + `openpyxl` engine or better, `polars` which is Rust-backed:

```python
import polars as pl
df = pl.read_excel("big.xlsx")  # polars uses Rust under the hood
```

So Python with Polars largely closes the gap for DataFrames. But if you're doing **custom row-by-row logic**, Rust still wins.

### 2. Compute-Heavy (regex scanning, AST parsing, file search)

Claude Code's killer feature is fast codebase indexing. If you're scanning 50k files for symbols:

```
Python grep-like scan of 50k files:   ~8s
Rust ripgrep-style scan:               ~0.3s
```

This is why `ripgrep` exists and why tools like `ast-grep` are Rust. The parallelism + zero-copy string scanning is where Rust shines.

### 3. Parallel Tool Calls

If your agent runs multiple tool calls concurrently (read 10 files, run 3 shell commands), Python's GIL limits true CPU parallelism. Rust's `tokio` + `rayon` gives you both async I/O and CPU parallelism cleanly.

---

## How to Actually Profile This

Don't guess. Here's the minimal profiling setup for a CLI agent:

**Python — profile your agent's non-LLM time:**

```python
import cProfile
import pstats
import io

pr = cProfile.Profile()
pr.enable()

# your agent's tool-use / file-handling code here
result = process_repo("./my_project")

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(20)
print(s.getvalue())
```

Or use `py-spy` for zero-overhead sampling on a running process:

```bash
py-spy record -o profile.svg -- python agent.py
```

**Rust — `cargo bench` with criterion:**

```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_file_scan(c: &mut Criterion) {
    c.bench_function("scan_repo", |b| {
        b.iter(|| scan_repository("./test_repo"))
    });
}

criterion_group!(benches, bench_file_scan);
criterion_main!(benches);
```

**Wall-clock comparison for the whole agent loop:**

```bash
# measure everything except LLM time
hyperfine \
  'python agent.py --dry-run --no-llm' \
  './target/release/agent --dry-run --no-llm' \
  --warmup 3
```

`hyperfine` gives you mean, stddev, and a clean comparison table.

---

## Practical Decision Matrix for Your Use Case

| Workload | Python Good Enough? | Rust Worth It? |
|---|---|---|
| LLM API orchestration | ✅ always | overkill |
| Small file reads (<1k files) | ✅ | no |
| Large Excel (>50k rows, custom logic) | ⚠️ use polars | ✅ yes |
| Full codebase indexing (>10k files) | ❌ slow | ✅ yes |
| Regex/AST scanning at scale | ❌ | ✅ yes |
| JSON parsing of API responses | ✅ | marginal |
| CLI startup in tight loops | ⚠️ 100ms overhead | ✅ 5ms |

---

## My Take for Your Situation

For your `ww`/`zz`/`iclaw` style CLI agents: **start Python, profile with `py-spy`, only rewrite the hot path in Rust if profiling shows >10% of wall time in non-LLM code.** 

The one case where I'd start in Rust immediately: if you're building something like a codebase indexer, file watcher, or semantic search over large repos — that's where Rust pays from day one. Tools like `ast-grep`, `ripgrep`, and `oxc` (JS parser) exist exactly for this reason.

For pure LLM agent orchestration (like a minimal Claude Code clone), Python with `asyncio` is fine — the `await anthropic.messages.create()` swallows everything else.