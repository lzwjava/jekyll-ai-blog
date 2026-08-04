---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 查看eval_datasets中的JSONL文件
translated: true
type: note
---

**问题：** 如何打开/查看 `eval_datasets` 目录中的 JSONL 文件？

**答案：**

根据你的需求，选择最快的路径：

**快速查看（命令行，无需依赖）**

```bash
head -n 5 eval_datasets/foo.jsonl | jq .
```

**统计行数**

```bash
wc -l eval_datasets/foo.jsonl
```

**以漂亮格式打印所有行中的某个字段**

```bash
jq -r '.prompt' eval_datasets/foo.jsonl | head -20
```

**Python — 流式读取，大文件时不要一次性加载**

```python
import json

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

for i, row in enumerate(read_jsonl("eval_datasets/foo.jsonl")):
    print(row)
    if i >= 5:
        break
```

**一次性加载到内存（小于1GB左右没问题）**

```python
import json
data = [json.loads(l) for l in open("eval_datasets/foo.jsonl", encoding="utf-8")]
print(len(data), data[0])
```

**pandas，如果你想要表格操作**

```python
import pandas as pd
df = pd.read_json("eval_datasets/foo.jsonl", lines=True)
df.head()
```

**使用 jq 进行过滤/搜索，无需在 Python 中加载**

```bash
jq 'select(.label == "fail")' eval_datasets/foo.jsonl
```

**验证每一行是否是有效的 JSON（捕获损坏的导出）**

```bash
python3 -c "
import json, sys
for i, l in enumerate(open('eval_datasets/foo.jsonl', encoding='utf-8')):
    l = l.strip()
    if not l: continue
    try: json.loads(l)
    except Exception as e: print(f'line {i}: {e}')
"
```

如果这是某个特定评估工具（如 lm-eval-harness、OpenAI evals 等）的 `eval_datasets` 文件夹，且模式不明确，请告诉我具体是哪个，我会给出你期望的确切字段名。

参考：

- [jq 手册](https://jqlang.github.io/jq/manual/)
- [pandas.read_json](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)
