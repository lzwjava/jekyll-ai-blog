---
audio: false
generated: true
image: false
lang: en
layout: post
title: View JSONL Files in eval_datasets
translated: false
type: note
---

Question: How do I open/view a JSONL file in an `eval_datasets` directory?

Answer:

Fastest paths, pick based on what you need:

**Quick peek (CLI, no deps)**
```bash
head -n 5 eval_datasets/foo.jsonl | jq .
```

**Line count**
```bash
wc -l eval_datasets/foo.jsonl
```

**Pretty-print one field across all lines**
```bash
jq -r '.prompt' eval_datasets/foo.jsonl | head -20
```

**Python — stream, don't load whole file if it's large**
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

**Load whole thing into memory (fine if <1GB-ish)**
```python
import json
data = [json.loads(l) for l in open("eval_datasets/foo.jsonl", encoding="utf-8")]
print(len(data), data[0])
```

**pandas, if you want tabular ops**
```python
import pandas as pd
df = pd.read_json("eval_datasets/foo.jsonl", lines=True)
df.head()
```

**Filter/search with jq without loading in Python**
```bash
jq 'select(.label == "fail")' eval_datasets/foo.jsonl
```

**Validate every line is valid JSON (catches corrupt exports)**
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

If it's a specific eval harness's `eval_datasets` folder (lm-eval-harness, OpenAI evals, etc.) and the schema's non-obvious, tell me which one and I'll give you the exact field names to expect.

References:
- [jq manual](https://jqlang.github.io/jq/manual/)
- [pandas.read_json](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html)