---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 访问Hugging Face上的BigCode数据集
translated: true
type: note
---

**问题：** 在哪里可以找到 https://huggingface.co/bigcode 背后的实际文本/代码数据？

**答案：**

该 URL 只是组织主页。实际数据位于该组织的 **数据集（Datasets）** 标签页下：https://huggingface.co/bigcode — 点击“Datasets”，或直接访问 https://huggingface.co/datasets?other=bigcode。主要语料库：

- **The Stack v2**（最大的，约 67TB 原始数据）：https://huggingface.co/datasets/bigcode/the-stack-v2 — 以及变体 `the-stack-v2-dedup` 和 `the-stack-v2-train-full-ids`（实际的 StarCoder2 训练混合集，约 900B tokens）
- **The Stack v1**（约 3TB 去重后）：https://huggingface.co/datasets/bigcode/the-stack-dedup
- **starcoderdata**（约 800GB，已清洗的 StarCoder1 训练集 — 实际使用中最实用的一个）：https://huggingface.co/datasets/bigcode/starcoderdata

在读取数据之前有两个注意事项：

**1. 它们是受限的（gated）。** 你需要一个 HF 账号，在数据集页面上点击“同意并访问（Agree and access）”，然后在本地进行身份验证：

```bash
pip install -U huggingface_hub datasets
hf auth login   # 粘贴来自 https://huggingface.co/settings/tokens 的 token
```

**2. The Stack v2 不包含文件内容。** 它只提供元数据 + Software Heritage blob ID；实际文本保存在 SWH 的 S3 存储桶中，需要单独下载（并需要 AWS 凭证）：

```python
import os, boto3, smart_open
from datasets import load_dataset

session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
s3 = session.client("s3")

def download_blob(blob_id, encoding):
    url = f"s3://softwareheritage/content/{blob_id}"
    with smart_open.open(url, "rb", compression=".gz",
                         transport_params={"client": s3}) as f:
        return f.read().decode(encoding)

ds = load_dataset("bigcode/the-stack-v2", "Python",
                  split="train", streaming=True)
for row in ds:
    print(download_blob(row["blob_id"], row["src_encoding"])[:500])
    break
```

对于你的用例（在 4070 或 MI300X 上进行 nanoGPT 规模的训练），可以跳过这种复杂性 — **The Stack v1 和 starcoderdata 直接包含文本内容**，因此流式加载就可以正常工作：

```python
from datasets import load_dataset

# 流式加载，不要下载 800GB
ds = load_dataset("bigcode/starcoderdata", data_dir="python",
                  split="train", streaming=True)
row = next(iter(ds))
print(row["content"][:1000])   # 实际的源代码文本
```

或者使用 CLI 将单个语言子集下载到磁盘：

```bash
hf download bigcode/the-stack-dedup \
  --repo-type dataset \
  --include "data/python/*" \
  --local-dir ./stack-python
```

文件是 parquet 格式，下载后也可以直接用 `pyarrow`/`polars` 读取。对于分词和训练流程，nanoGPT 中 `data/openwebtext/prepare.py` 的模式可以直接移植：流式加载 → tokenizer.encode → 追加到内存映射的 `.bin` 文件。

规模参考：仅 starcoderdata 的 `python` 子集就有约 60B tokens — 远超 760M 参数运行所需（Chinchilla 最优约为 15B tokens），因此在你的 916GB 工作站上流式加载一个切片是正确的做法，在 Air 上更是如此。

**参考资料：**

- [Hugging Face 上的 bigcode 数据集](https://huggingface.co/bigcode)
- [The Stack v2 数据集卡片（包含 S3 下载代码片段）](https://huggingface.co/datasets/bigcode/the-stack-v2)
- [starcoderdata 数据集卡片](https://huggingface.co/datasets/bigcode/starcoderdata)