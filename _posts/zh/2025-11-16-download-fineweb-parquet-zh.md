---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 下载特定FineWeb数据集文件
translated: true
type: note
---

你只想从某个 Common Crawl 数据集中下载并使用几个 parquet 文件（比如 CC-MAIN-2013-20），而不是完整的 15T token 的 FineWeb 庞大数据集——这完全合理！以下是 2025 年最简单的实现方式。

### 方法一：使用 huggingface_hub 直接下载（推荐，速度最快）
这种方法只下载你需要的 parquet 文件，并以全速下载（如果启用 hf-transfer，速度可达 ~GB/s）。

```bash
# 1. 安装/升级
pip install -U "huggingface_hub[hf_transfer]"

# 2. 启用快速下载（非常重要！）
export HF_HUB_ENABLE_HF_TRANSFER=1   # Linux/macOS
# 或在 Windows PowerShell 中：
# $env:HF_HUB_ENABLE_HF_TRANSFER = "1"

# 3. 仅下载你需要的几个 parquet 文件
huggingface-cli download HuggingFaceFW/fineweb \
    data/CC-MAIN-2013-20/000_00000.parquet \
    data/CC-MAIN-2013-20/000_00001.parquet \
    data/CC-MAIN-2013-20/000_00002.parquet \
    --repo-type dataset --local-dir fineweb-2013-20
```

完成！现在你的 `fineweb-2013-20/` 文件夹中就有了三个约 2.15 GB 的 parquet 文件。

### 方法二：使用单行 Python 脚本下载特定文件
```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb",
    repo_type="dataset",
    allow_patterns=[
        "data/CC-MAIN-2013-20/000_00000.parquet",
        "data/CC-MAIN-2013-20/000_00001.parquet",
        # 如需更多文件，请在此添加
    ],
    local_dir="fineweb-2013-20"
)
```

### 如何本地读取 Parquet 文件
```python
import pandas as pd
# 或使用 pyarrow 以获得更快速度和更低内存占用
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# 最快的方法（流式读取，无需将所有数据加载到 RAM 中）
dataset = ds.dataset("fineweb-2013-20/data/CC-MAIN-2013-20/", format="parquet")

for batch in dataset.to_batches(batch_size=1024):
    df = batch.to_pandas()
    for text in df["text"]:
        # 执行任何你需要的操作：分词、过滤、写入 jsonl 等
        print(text[:200])  # 示例
```

或者简单地使用 pandas（适用于少量文件）：
```python
df = pd.read_parquet("fineweb-2013-20/data/CC-MAIN-2013-20/000_00000.parquet")
print(df.columns)  # ['text', 'id', 'dump', 'url', 'date', 'file_path', 'language', 'language_score', 'token_count']
print(df.iloc[0]["text"])
```

### CC-MAIN-2013-20 的快速统计信息
- 约 207 个 parquet 文件 × 约 2.15 GB ≈ 总计 422 GB
- 约 440 亿个 token（适合中小型实验）
- 已由 Hugging Face 完成清洗、去重和过滤

这就是你所需要的全部步骤。只需选择你需要的任意数量的 `_0000XX.parquet` 文件（它们是经过打乱的），仅下载这些文件，然后立即开始训练或过滤。
