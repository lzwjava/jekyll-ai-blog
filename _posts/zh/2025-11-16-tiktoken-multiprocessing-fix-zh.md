---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决Tiktoken多进程序列化错误
translated: true
type: note
---

在使用 `datasets.map(..., num_proc>1)` 配合自定义分词器（如 nanoGPT 的 FineWeb 脚本中使用的 Tiktoken 编码器）时，您遇到的错误非常常见——分词器会加载 BPE 文件（`cl100k_base.tiktoken` 或类似文件），而这个文件句柄**无法被序列化**传递到 Linux 基于 fork 的多进程子进程中。

子进程会立即崩溃 → 出现“某个子进程意外终止”的错误。

### 快速修复（99% 的情况有效）

编辑 `data/fineweb/prepare.py`，强制分词操作仅在**主进程**中运行：

```python
# 在 80-85 行附近找到 .map() 调用，将 num_proc=8 改为 num_proc=1

tokenized = raw_datasets.map(
    tokenize,
    num_proc=1,               # ← 修改这一行（或直接删除该参数）
    desc="tokenizing the splits",
)
```

这样速度会变慢（单核运行），但能稳定运行。在 FineWeb-10B 数据集上，根据 CPU/磁盘性能，大约需要 30-60 分钟。

### 更优修复（保持多进程，速度更快）

让分词器在工作进程内部延迟加载，而不是在全局作用域中加载。

将当前的分词器创建代码（约 40-50 行）替换为以下模式：

```python
import tiktoken

# 删除全局的 encoder = tiktoken.get_encoding("cl100k_base")

def get_encoder():
    """在每个子进程中延迟加载分词器"""
    return tiktoken.get_encoding("cl100k_base")

def tokenize(example):
    enc = get_encoder()                                   # ← 每个进程独立加载
    ids = enc.encode_ordinary(example["text"])
    ids.append(enc.eot_token)  # 或按原脚本操作
    return {"ids": ids, "len": len(ids)}
```

然后保持 `num_proc=8`（或任意数值）。这样每个工作进程在 fork 后会加载自己的 .tiktoken 文件副本 → 避免序列化问题。

### 更快的替代方案（推荐用于重复运行）

从 Hugging Face 预下载 10B/100B 的 FineWeb-Edu 分片，使用 Karpathy 更新的脚本直接处理 parquet/arrow 文件，而不是巨型 .txt 文件：

```bash
# 速度更快且完全避免此错误
python data/fineweb/prepare_fineweb.py --version 10B
# 或 100B
```

新脚本（约 2024 年添加）使用官方的 HF 数据集，且支持多进程安全操作。

### 总结

| 解决方案                        | 速度      | 复杂度     | 推荐度         |
|-------------------------------|-----------|------------|----------------|
| `num_proc=1`                  | 较慢      | 单行修改   | 快速修复       |
| 在 tokenize() 内部延迟加载编码器 | 较快      | 小幅改动   | 适用于 .txt 文件 |
| 使用新的 prepare_fineweb.py 脚本 | 最快      | 新命令     | 强烈推荐       |

任选一种方案即可立即解决此错误。请告知您选择哪种方式，如果需要我会提供具体补丁！
