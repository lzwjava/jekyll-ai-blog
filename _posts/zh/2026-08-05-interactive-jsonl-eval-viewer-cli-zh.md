---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 交互式JSONL评估查看器CLI
translated: true
type: note
---

问题：如何可视化检查JSONL评估数据集中的条目（而不仅仅是输出原始文本）？

回答：

鉴于您优先使用命令行，这里提供一个基于终端的交互式查看器，使用 `rich` 实现——彩色显示、分页，可以逐条或一次性查看所有记录：

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
python3 view_jsonl.py eval_datasets/foo.jsonl 10          # 前10条记录，完整美化打印
python3 view_jsonl.py eval_datasets/foo.jsonl 20 prompt   # 仅显示"prompt"字段，20条记录
```

**并排差异样式（比较 prompt、completion 和 gold）**
```bash
jq -r '"PROMPT: \\(.prompt)\nGOLD: \\(.answer)\n---"' eval_datasets/foo.jsonl | less -R
```

**在目视检查之前先看统计信息——字段存在情况、长度分布**
```python
import json, statistics
rows = [json.loads(l) for l in open("eval_datasets/foo.jsonl", encoding="utf-8")]
keys = set().union(*(r.keys() for r in rows))
print("keys:", keys)
lens = [len(r.get("prompt", "")) for r in rows]
print(f"n={len(rows)} mean_len={statistics.mean(lens):.0f} max={max(lens)}")
```

如果你真的想要一个在浏览器中可滚动/可搜索的工具（例如检查数百个多轮对话，终端换行会让人头疼），我可以构建一个单文件HTML工件，加载 `.jsonl` 并允许过滤/搜索/跳转——告诉我一声，我会构建它。否则 `less -R` + `jq` 可以覆盖90%的评估调试。

参考：
- [rich docs](https://rich.readthedocs.io/en/stable/introduction.html)
- [jq manual](https://jqlang.github.io/jq/manual/)