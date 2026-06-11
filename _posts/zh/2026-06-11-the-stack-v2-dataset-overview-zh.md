---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Stack v2数据集概览
translated: true
type: note
---

**问题：** 请介绍 The Stack v2 数据集（huggingface.co/datasets/bigcode/the-stack-v2）。

**答案：**

Stack v2 是 StarCoder2 的预训练语料库，由 BigCode 项目（Hugging Face + ServiceNow）构建。如果你想了解生产级代码大语言模型如何获取数据，这个数据集值得研究——它直接关系到你的 nanoGPT/nanochat 训练工作，可作为严肃数据集工程的参考范例。

**规模与 v1 的差异**

完整数据集未压缩时为 67.5TB（v1 为 6.4TB），去重后为 32.1TB（v1 为 2.9TB），完整训练集包含约 9000 亿 tokens（v1 约 2000 亿）。覆盖 658 种编程和标记语言中的超过 30 亿个文件。

关键架构变化：v1 直接抓取 GitHub；v2 源自 Software Heritage 存档——通过遍历 SWH 2023-09-06 图数据集，从 1.042 亿个 GitHub 仓库中收集了 32.8 亿个唯一文件，仓库元数据来自 GH Archive。这提供了来源（SWHIDs）、更好的治理能力和退出机制。

**注意：这是索引，而非文件本体**

HF 数据集仅包含 SWHID（blob ID）和元数据——实际文件内容存储在 Software Heritage 的 S3 存储桶中，批量下载需与 Software Heritage/INRIA 签订协议。工作流程为：从 HF 流式传输 parquet 索引，然后自行从 `s3://softwareheritage/content/{blob_id}` 获取 blob：

```python
import os, boto3
from smart_open import open as sopen
from datasets import load_dataset

s3 = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
).client("s3")

def fetch(row):
    url = f"s3://softwareheritage/content/{row['blob_id']}"
    with sopen(url, "rb", compression=".gz", transport_params={"client": s3}) as f:
        return {"content": f.read().decode(row["src_encoding"])}

ds = load_dataset("bigcode/the-stack-v2", split="train", streaming=True)
ds = ds.map(fetch)
```

（需要 `pip install 'smart_open[s3]' datasets boto3`。数据集也是受限访问的——需先在 HF 上接受使用条款。）

**四个版本**

共有 4 个版本：完整版 `the-stack-v2`；`the-stack-v2-dedup`（近似去重版）；`the-stack-v2-train-full-ids`（启发式过滤版，涵盖 600+ 语言，按仓库分组）；`the-stack-v2-train-smol-ids`（同上，但仅筛选 17 种语言）。对于 nanoGPT 规模的代码模型实验，`smol-ids` 是实用选择。仓库分组具有重要意义：它允许使用完整仓库上下文（跨文件依赖）进行预训练，这也是 StarCoder2 能良好处理仓库级代码补全的原因之一。

**值得借鉴的数据处理流程**

- 去重：在精确去重基础上进行近似去重；约 40% 的宽松许可证文件属于近似重复——仅此一点就证明，构建任何代码语料库时都应采用 MinHash/LSH 管道。
- 过滤：删除二进制文件、空文件、无法解码的文件以及超过 10MB 的文件；通过 `go-enry`/linguist 进行语言检测，每个文件带有 `is_vendor` 和 `is_generated` 标记。
- 许可证：仓库级许可证来自 GH Archive，但对于 96.93% 无许可证的仓库，ScanCode 会从 LICENSE/README 样式文件中检测文件级许可证，并将其沿目录树传播。每行数据带有 `detected_licenses`（SPDX）和 `license_type`。
- 每行有用的元数据：`star_events_count`、`fork_events_count`、`revision_date`、`branch_name`——足以让你实现自己的质量加权采样（例如，提高高星仓库权重、按时间过滤）。

**对你工作的特殊意义**

如果你打算将 nanoGPT-on-FineWeb 式的运行迁移至 MI300X 上训练代码模型，这就是规范的开源语料库。StarCoder2 论文（arXiv:2402.19173）实质上是数据集工程手册：涵盖去重比率、语言过滤启发式方法、PII 编辑、仓库上下文打包。请注意，数据卡片本身也警告数据集可能仍包含公开仓库中发布的电子邮件、IP 地址和 API/SSH 密钥——因此，如果你在其上训练，请在 tokenize 之前运行自己的密钥清除流程（例如 detect-secrets 或 BigCode PII 管道）。

**参考文献：**

- [bigcode/the-stack-v2 — Hugging Face](https://huggingface.co/datasets/bigcode/the-stack-v2)
- [StarCoder 2 and The Stack v2: The Next Generation (arXiv:2402.19173)](https://huggingface.co/papers/2402.19173)
- [BigCode Project](https://www.bigcode-project.org/)