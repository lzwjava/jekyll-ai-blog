---
audio: false
generated: true
image: false
lang: zh
layout: post
title: H200 FineWeb 分词摘要
translated: true
type: note
---

以下是 H200 服务器上所有已完成工作的完整总结：

---

**服务器：** `38.80.152.249:30416` — NVIDIA H200（140 GB VRAM，CUDA 13.0）
**工作目录：** `/workspace/zz/`

### 1. 设置
- 创建 SSH 密钥并添加到 GitHub
- 克隆 `git@github.com:lzwjava/zz.git` 到 `/workspace/zz/`
- 安装 `tmux` 以保持会话持久化
- Python 依赖：`tiktoken`、`numpy`、`pyarrow`、`tqdm`、`huggingface_hub`

### 2. 数据下载
- **脚本：** `h200/download_fineweb.py`
- **数据集：** HuggingFaceFW/fineweb-edu — 44 个 parquet 分片
- **大小：** 磁盘占用 95 GB，约 25.5B 词元
- **覆盖范围：** 4 个 CommonCrawl 转储（CC-MAIN-2013-20、2013-48、2014-10、2014-15）
- **速度：** 约 20 MB/s，约 75 分钟完成

### 3. 分词
- **脚本：** `h200/tokenize_fineweb.py`
- **分词器：** GPT-2 BPE（tiktoken），每个文档前添加 `<|endoftext|>`
- **分片大小：** 每个 `.npy` 文件 1 亿个 uint16 词元
- **工作进程：** 96 个 CPU 核心
- **吞吐量：** 约 8-10M 词元/秒

### 4. 结果

| 指标 | 数值 |
|--------|-------|
| **输出分片** | 358（1 个验证 + 357 个训练） |
| **总词元数** | 约 35.8B（含 EOT 前缀） |
| **输出位置** | `/workspace/zz/datasets/tokenized/` |
| **输出文件** | `edufineweb_val_000000.npy` + `edufineweb_train_000001-000357.npy` |
| **磁盘占用** | `/workspace` 约 104 GB（总计 187 GB） |
| **实际耗时** | 约 45 分钟 |

### 5. 命令

```bash
# 下载（已完成）
cd /workspace/zz
python3 h200/download_fineweb.py

# 分词（已完成）
cd /workspace/zz
python3 h200/tokenize_fineweb.py
```

分词后的数据已准备好用于 GPT-3 消融训练 —— 支持 nanoGPT 格式。