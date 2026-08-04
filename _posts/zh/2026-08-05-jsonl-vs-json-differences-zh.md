---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JSONL 与 JSON 的区别
translated: true
type: note
---

问：为什么叫JSONL而不是JSON，它们有什么区别？

答：

**JSONL = "JSON Lines"** — 每行一个有效的JSON值，以换行符分隔。它不是一个单一的JSON文档。

```
{"id": 1, "prompt": "what is 2+2", "answer": "4"}
{"id": 2, "prompt": "capital of france", "answer": "paris"}
{"id": 3, "prompt": "1+1", "answer": "2"}
```

对比标准 **JSON** —— 单个顶层值（通常是一个包裹所有对象的数组）：

```json
[
  {"id": 1, "prompt": "what is 2+2", "answer": "4"},
  {"id": 2, "prompt": "capital of france", "answer": "paris"},
  {"id": 3, "prompt": "1+1", "answer": "2"}
]
```

**为什么存在JSONL —— 它在评估/训练数据中胜出的实际原因：**

1. **Streaming/append-friendly（流式/追加友好）**。你可以`open(path, "a")`，在生成评估结果时逐行追加，而无需重新解析或重写整个文件。JSON数组要追加元素则需要重写整个结构（或小心翼翼地操作括号）。

2. **无需完整解析文件**。对巨型JSON数组执行`json.load()`意味着在访问任何一条记录之前，必须将整个树加载到内存中。JSONL允许你逐行流式处理——这就是我给你的生成器模式（`for line in f: json.loads(line)`）从未在内存中保留超过一条记录的原因。

3. **崩溃恢复能力强**。如果JSONL写入中途被截断（OOM、kill -9），你只丢失最后不完整的一行——文件其余部分仍然有效。而截断的JSON数组从第一个缺失的括号开始就是损坏的垃圾数据，`json.loads`会在整个文件上失败。

4. **基于行的工具开箱即用**。`wc -l`、`grep`、`head`、`tail`、`split`、`sed`、`awk`、`jq`（流模式）都能自然地按行操作。这就是为什么每个主流评估框架（OpenAI evals、lm-eval-harness、你自己的评估脚本）以及每个LLM训练流水线（预训练语料、SFT数据集、RLHF偏好对）都将其标准化——在你运行月级2B token规模的场景下，你实际上就是在用`cat`和`shuf`来打乱、分片和拼接训练数据。

5. **易并行化**。用`split -n l/8 data.jsonl`将一个JSONL文件拆成N个块给N个工作进程——每个块都是独立有效的。而拆分JSON数组则需要理解其结构。

**JSONL vs JSON 的权衡：**

| | JSON | JSONL |
|---|---|---|
| 结构 | 一个树形结构，顶层任意嵌套 | 独立记录的扁平列表 |
| 解析成本 | 使用前必须解析整个文件 | 逐行增量解析 |
| 追加 | 需要重写 | 只需写入新行 |
| 损坏影响范围 | 整个文件 | 一行 |
| 美观打印/可读性 | 更适合深层嵌套的单个对象 | 更适合表格/记录形状的数据 |
| 工具支持 | jq、完整JSON解析器 | 相同工具 + 所有Unix行工具 |
| 本身不是有效JSON | — | 正确——.jsonl文件对整个文件执行json.loads()会失败；必须先按行分割 |

底线：JSON用于单个结构化文档；JSONL用于数据集——这正是每个评估/训练语料库都使用它的原因。

参考文献：
- [JSON Lines规范](https://jsonlines.org/)