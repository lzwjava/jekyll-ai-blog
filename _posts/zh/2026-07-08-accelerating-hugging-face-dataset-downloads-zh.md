---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 加速Hugging Face数据集下载
translated: true
type: note
---

**问题：** 有没有更好的方式来下载 Hugging Face 模型？20 MB/s 太慢了。如果在广州的家里用两台台式机，一台下载 Parquet 文件 1–20，另一台下载 21–40，这样会有帮助吗？

**回答：**

确实如此。**20 MB/s 相当慢**，尤其是下载数百 GB 的训练数据时。例如：

* 20 MB/s ≈ 72 GB/小时
* 1 TB 大约需要 **14–15 小时**
* 10 TB 则需要近 **6 天**

对于大语言模型预训练数据集来说，下载速度很快就会成为瓶颈。

### 方案一：并行下载（推荐）

如果数据集由多个 Parquet 分片组成（如 FineWeb、FineWeb-Edu、BigCode 等），那么你的思路是可行的。

机器 A：

```bash
下载 shard_00000.parquet
...
下载 shard_00019.parquet
```

机器 B：

```bash
下载 shard_00020.parquet
...
下载 shard_00039.parquet
```

之后：

```bash
rsync -av machineB:/data/*.parquet /data/
```

或者将它们复制到 SSD 上。

由于每个 Parquet 文件是独立的，后续合并完全没有问题。

---

### 方案二：使用 `hf_transfer`（速度更快）

安装：

```bash
pip install "huggingface_hub[hf_transfer]"
```

启用：

```bash
export HF_HUB_ENABLE_HF_TRANSFER=1
```

然后使用：

```bash
huggingface-cli download \
    HuggingFaceFW/fineweb-edu \
    --repo-type dataset
```

`hf_transfer` 会开启大量并发 HTTP 连接，如果你的网络不是瓶颈，通常比默认下载器**快 2–5 倍**。

---

### 方案三：aria2c

不再使用单一 HTTP 流：

```bash
aria2c \
    -x16 \
    -s16 \
    URL
```

或者并行运行多个下载任务：

```bash
cat urls.txt | xargs -n1 -P16 aria2c
```

---

### 方案四：在云端下载（通常是最佳选择）

如果你最终要在 RunPod、Lambda 或其他云 GPU 上进行训练：

* 直接在云端下载
* 存储到持久化卷
* 避免从家上传

云数据中心到 Hugging Face 的速度通常能达到 **100–1000 MB/s**。

---

### 方案五：Hugging Face 镜像（适用于中国）

如果你身在广州，到 Hugging Face 的国际路由可能会成为限制因素。

许多人使用镜像站：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

性能因运营商和时段而异，但中国大陆用户普遍反馈有显著提升。

---

### 方案六：增加下载工作线程数

Hugging Face Python API 支持多工作线程：

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="HuggingFaceFW/fineweb-edu",
    repo_type="dataset",
    max_workers=32,
)
```

将默认值提升到 16–32 个工作线程可以显著提高吞吐量。

---

## 两台台式机值得吗？

值得，尤其是在以下情况下：

* 你的网络服务商为每台机器分配独立的带宽
* 数据集有成百上千个 Parquet 分片
* 两台机器都写入本地 SSD

例如：

台式机 1：

```
0000.parquet
...
0999.parquet
```

台式机 2：

```
1000.parquet
...
1999.parquet
```

然后合并目录。这是一种简单有效的策略。

---

### 针对你的工作流程

由于你在下载**数 TB 级别的预训练数据集**（FineWeb、BigCode 等），我建议优先考虑：

1. `hf_transfer`
2. `max_workers=32`
3. 将分片拆分到多台机器
4. 条件允许时直接在云端下载

同时使用这四种方法，相比单一的 20 MB/s 流，可以大幅缩短下载时间。
