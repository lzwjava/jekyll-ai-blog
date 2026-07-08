---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BigCode Python专用模型训练指南
translated: true
type: note
---

问题：如何只获取一种编程语言（例如 Python）进行训练？BigCode 能提供这样的支持吗？

回答：

是的。**BigCode 的数据集是最好的来源之一**，如果你想训练一个仅支持 Python 的模型。

主要选项如下：

| 数据集                    | 仅限 Python？               | 质量        | 规模          |
| -------------------------- | --------------------------- | ----------- | -------------- |
| The Stack v2               | 是（按语言筛选）            | 非常好      | TB 级别        |
| The Stack                  | 是                          | 好          | 大             |
| CodeParrot                 | 是                          | 好          | 数百 GB        |
| GitHub 公共仓库            | 是（自行爬取/筛选）         | 各有差异    | 巨大           |

### 选项 1 — The Stack v2（推荐）

The Stack 存储了包含语言信息的元数据。

示例：

```python
from datasets import load_dataset

ds = load_dataset(
    "bigcode/the-stack-v2",
    split="train",
)

python_ds = ds.filter(lambda x: x["lang"] == "Python")
```

或者如果使用 parquet 文件：

```python
import pyarrow.parquet as pq

table = pq.read_table(file)
python_only = table.filter(table["lang"] == "Python")
```

数据集已经按语言对文件进行了标注，因此你无需自行检测。

---

### 选项 2 — CodeParrot

如果你只关心 Python：

```python
load_dataset("codeparrot/codeparrot-clean")
```

它几乎全是 Python 源代码。

这比 The Stack 小得多，也更容易用于实验。

---

### 选项 3 — 构建自己的数据集

许多训练代码大语言模型的人的流程：

```
GitHub
    ↓
克隆仓库
    ↓
仅保留 *.py 文件
    ↓
去重
    ↓
移除自动生成/供应商文件
    ↓
分词
    ↓
训练
```

这样你可以完全掌控。

---

### 你实际上需要多少 Python 数据？

对于小型解码器模型：

| 模型   | 令牌数   |
| ------ | -------- |
| 10M    | 1–5B     |
| 100M   | 10–30B   |
| 760M   | 30–80B   |
| 1.5B   | 50–150B  |

Python 的信息密度相对较高，因为其词汇和语法受限。与同等能力的自然语言模型相比，通常需要的令牌数更少。

---

### 一个简单的预处理流程

```text
The Stack v2
      │
      ├── 语言 == Python
      │
      ├── 移除重复项
      │
      ├── 移除自动生成的文件
      │
      ├── 可选：移除笔记本/测试文件
      │
      ├── 分词器
      │
      └── NanoChat 训练
```

对于你使用 NanoChat 进行的实验，这是一个直接且实用的流程。

参考资料：

* [The Stack v2](https://huggingface.co/datasets/bigcode/the-stack-v2?utm_source=chatgpt.com)
* [CodeParrot Clean Dataset](https://huggingface.co/datasets/codeparrot/codeparrot-clean?utm_source=chatgpt.com)
* [BigCode 项目](https://www.bigcode-project.org/?utm_source=chatgpt.com)