---
audio: false
generated: true
image: false
lang: en
layout: post
title: Interactive JSONL Eval Viewer CLI
translated: false
type: note
---

Question: How do I visually inspect entries in a JSONL eval dataset (not just dump raw text)?

Answer:

Given you're CLI-first, here's a terminal-based interactive viewer with `rich` — colorized, paginated, one record at a time or all at once:

```python
#!/usr/bin/env python3
# view_jsonl.py
import json
import sys
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.pretty import Pretty

console = Console()

def load(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def show(path, n=None, key=None):
    for i, row in enumerate(load(path)):
        if n is not None and i >= n:
            break
        if key:
            content = str(row.get(key, "<missing>"))
            console.print(Panel(content, title=f"[{i}] {key}", border_style="cyan"))
        else:
            console.print(Panel(Pretty(row, expand_all=True), title=f"record {i}", border_style="cyan"))

if __name__ == "__main__":
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    key = sys.argv[3] if len(sys.argv) > 3 else None
    show(path, n, key)
```

```bash
pip install rich
python3 view_jsonl.py eval_datasets/foo.jsonl 10          # first 10 records, full pretty-print
python3 view_jsonl.py eval_datasets/foo.jsonl 20 prompt   # just the "prompt" field, 20 records
```

**Side-by-side diff style (compare prompt vs completion vs gold)**
```bash
jq -r '"PROMPT: \\(.prompt)\nGOLD: \\(.answer)\n---"' eval_datasets/foo.jsonl | less -R
```

**Stats before you eyeball anything — field presence, length distribution**
```python
import json, statistics
rows = [json.loads(l) for l in open("eval_datasets/foo.jsonl", encoding="utf-8")]
keys = set().union(*(r.keys() for r in rows))
print("keys:", keys)
lens = [len(r.get("prompt", "")) for r in rows]
print(f"n={len(rows)} mean_len={statistics.mean(lens):.0f} max={max(lens)}")
```

If you actually want something scrollable/searchable in a browser (e.g. checking hundreds of multi-turn conversations where terminal wrapping gets painful), I can spin up a single-file HTML artifact that loads the `.jsonl` and lets you filter/search/jump — say the word and I'll build it. Otherwise `less -R` + `jq` covers 90% of eval debugging.

References:
- [rich docs](https://rich.readthedocs.io/en/stable/introduction.html)
- [jq manual](https://jqlang.github.io/jq/manual/)