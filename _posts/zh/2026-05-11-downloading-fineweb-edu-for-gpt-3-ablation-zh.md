---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为GPT-3消融实验下载FineWeb-Edu
translated: true
type: note
---

已删除文件。以下是指南：

---

# 下载 100B Tokens 的 FineWeb-Edu 用于小规模 GPT-3 消融实验

关于 `scripts/download/plan_and_download_fineweb_gpt3.py` 的详解——该脚本如何规划、下载并断点续传约 400 GB 的 FineWeb-Edu 数据（从中国境内无需 VPN）。

## 为什么是 100B tokens

100B tokens 是 GPT-3 论文在 Table 2.1 中每个 token 计数消融实验所使用的预算——足够训练出有意思的模型，又小到可以在单台工作站上完成。按照 Chinchilla 缩放律（每参数约 20 个 tokens），100B tokens 对应一个约 5B 参数的计算最优模型。对于一个 1.3B 参数的 Chinchilla 匹配模型，你大约需要 26B tokens；100B 对于该范围来说是充裕的超预算，这使它成为一个有用的消融切片。

速查表（英文 BPE，约 4 字节/token）：

| 预算   | 分片数 | 磁盘大小   | 说明                             |
| ------ | ------ | ---------- | -------------------------------- |
| 10B    | ~20    | ~40 GB     | GPT-2 级别                       |
| **100B** | **~200** | **~400 GB** | **GPT-3 消融实验（本脚本）**     |
| 300B   | ~600   | ~1.2 TB    | GPT-3 论文的完整训练集           |
| 1T     | ~2000  | ~4 TB      | 约 50B 参数的 Chinchilla 最优    |
| 1.3T   | full   | ~5.4 TB    | 完整 FineWeb-Edu                 |

## 为什么选择 FineWeb-Edu

[FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) 通过一个“教育价值”分类器过滤 FineWeb。它比原始 FineWeb 更小、更干净——对于消融实验通常报告的基准（MMLU、ARC、HellaSwag）而言，每个训练步骤的 token 质量更高。

如果你想要原始网页文本，请将 `REPO_ID` 替换为 `HuggingFaceFW/fineweb`。

## 为什么使用 hf-mirror.com

从中国大陆直接访问 `huggingface.co` 不稳定。`hf-mirror.com` 是一个社区镜像，通过未被屏蔽的 CDN 端点提供相同的 parquet 分片。该脚本：

1. 在导入 `huggingface_hub` **之前** 设置 `HF_ENDPOINT=https://hf-mirror.com`，这样 `HfApi().repo_info()` 的列表调用也会通过镜像——不仅仅是 parquet 下载。
2. 硬编码了实际文件获取的 `BASE_URL`。

如果你在中国境外，同样的脚本也能通过镜像运行——只是不会比官方端点更快。

## 架构

三个解耦的阶段：

```
list_parquet_shards()   →   select_shards()   →   download_one() 每个分片
   (HfApi，一次性)              (token 预算)         (可断点续传)
```

状态存储在 `<输出目录>/progress.json` 中。首次运行写入该文件；后续运行加载它并完全跳过 HF API 调用。

### `progress.json` 结构

```json
{
  "repo_id": "HuggingFaceFW/fineweb-edu",
  "target_tokens": 100000000000,
  "bytes_per_token": 4.0,
  "shards": [
    {"path": "data/CC-MAIN-2013-20/000_00000.parquet", "size": 2147483648,
     "dump": "CC-MAIN-2013-20", "status": "done"},
    {"path": "data/CC-MAIN-2013-20/000_00001.parquet", "size": 2147483648,
     "dump": "CC-MAIN-2013-20", "status": "pending"}
  ]
}
```

每个分片完成后原子更新（`tmp` + `os.replace`），因此 SIGKILL 或断电不会留下半写入状态。

### 实际恢复机制

两个独立层次：

1. **每个分片**（`.part` 文件 + HTTP `Range: bytes=N-`）：如果你在下载 2 GB 分片中途按 Ctrl-C，部分字节会保留在 `shard.parquet.part` 中。下次运行发现 `.part` 文件，以追加模式打开，并向服务器请求剩余部分。
2. **跨分片**（`progress.json` 中的 status 字段）：已完成的分片标记为 `done`。下次运行以 O(1) 跳过它们——无需 `os.path.exists` 遍历，无需重新从 HF 列出。

结合起来：你可以在任何时候杀死进程，最多丢失内存中缓冲的字节（< 1 MB）。

## 使用方法

```bash
# 预演——列出分片，写入 progress.json，但不下载
python scripts/download/plan_and_download_fineweb_gpt3.py --plan

# 下载（或断点续传）约 400 GB 到 datasets/fineweb-edu/
python scripts/download/plan_and_download_fineweb_gpt3.py

# 自定义输出位置
python scripts/download/plan_and_download_fineweb_gpt3.py \
    --output-dir /mnt/data/fineweb-edu

# 丢弃已保存的计划，重新从 HF 列表选取
python scripts/download/plan_and_download_fineweb_gpt3.py --refresh-plan
```

首次运行时你会看到类似这样的输出：

```
Listing shards in HuggingFaceFW/fineweb-edu...
Wrote new plan to datasets/fineweb-edu/progress.json.

Plan: ~100,000,000,000 tokens @ 4.0 bytes/token (small-scale GPT-3 ablation):
  shards:        198  (0 done)
  download size: 398.4 GB  (0.0 B already on disk)
  est. tokens:   107,000,000,000
  dumps covered: 1 (CC-MAIN-2013-20)

Downloading to datasets/fineweb-edu via https://hf-mirror.com ...
  [1/198] data/CC-MAIN-2013-20/000_00000.parquet (2.0 GB)
      progress: 2.0 GB / 398.4 GB  18.3 MB/s  ETA 360.1 min
```

Ctrl-C 后重新运行：

```
Loaded plan from datasets/fineweb-edu/progress.json (198 shards).

Plan: ~100,000,000,000 tokens @ 4.0 bytes/token (small-scale GPT-3 ablation):
  shards:        198  (47 done)
  download size: 398.4 GB  (94.0 GB already on disk)
  ...
  [1/198] done  data/CC-MAIN-2013-20/000_00000.parquet (2.0 GB)
  ...
  [48/198] data/CC-MAIN-2013-20/000_00047.parquet (2.0 GB)
      attempt 1/3 failed: ...  ← 会自动从 .part 恢复
```

## 运行前须知

- **磁盘**：需要 400 GB 空闲空间。分片在磁盘上不会进一步压缩；一个 parquet 文件 ≈ 一个分片 ≈ 约 2 GB。
- **带宽**：从 hf-mirror.com 持续 20 MB/s 时，约需 5.5 小时。家庭网络连接可能更慢。
- **token 估算为启发式**：`bytes / 4.0`。实际分词器计数可能偏差 ±10–15%，取决于你使用 GPT-2 BPE、tiktoken 还是 SentencePiece。如果你已测量过，请覆盖 `BYTES_PER_TOKEN`。
- **单个 CC dump**：FineWeb-Edu 的第一个分片位于 `CC-MAIN-2013-20` 下。198 个分片超过该快照包含的数量，因此计划将按 dump 排序顺序跨越多个 dump。如果你希望获得主题均衡的数据，请改为随机选择分片——当前排序是确定性的，但未进行领域均衡。
- **对数据集演变不具备幂等性**：如果 HuggingFace 重新分片 FineWeb-Edu，`progress.json` 中的路径可能会失效。请使用 `--refresh-plan` 重新构建。

## 下一步

下载的 parquet 文件是原始文本。要将它们转换为训练语料库，请将 `scripts/extract/extract_fineweb.py` 指向 `datasets/fineweb-edu/`。该脚本通过 `pyarrow.iter_batches` 流式读取 parquet 的 `text` 列，无需将整个文件加载到内存中。