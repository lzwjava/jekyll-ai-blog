---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanoGPT 训练的数据准备
translated: true
type: note
---

根据您更新的日志，这是您“60GB text data”发生情况的完整图景：

## 完整情况

您正在经历**两个不同的阶段**的数据准备：

### 阶段 1：Raw → Tokenized Shards（完成）
```
Raw text (60GB) → Tokenized .npy shards (28GB)
├── 149 training shards
├── 1 validation shard  
└── Format: NumPy arrays (.npy)
```

### 阶段 2：.npy → .bin 转换（进行中）
```
Tokenized .npy (28GB) → .bin format for nanoGPT
└── Concatenates all shards into single binary file(s)
```

## 为什么有两个格式？

| 格式       | 用途                          | 大小       |
|------------|-------------------------------|------------|
| `.npy` shards | Parallel tokenization, checkpoint-friendly | 28GB total |

## 理解 60GB → 28GB 比率

```
60GB raw text
    ↓ (tokenization)
~48B tokens (40M tokens/sec × 20 min)
    ↓ (binary serialization)
28GB .npy files
    ↓ (conversion)
28GB .bin files
```

**压缩比率**：约 2.14× (60/28)
- 文本分词的正常现象
- BPE tokens 平均每个 ~0.6-0.8 字节
- 您的计算：48B tokens × 0.58 字节 = 27.8GB ✓

## 剩余工作

从您的日志来看，您正在将 `.npy` 转换为 `.bin`：
```python
# The script you're running likely does:
for shard in 150_files:
    data = np.load(shard)      # Load token IDs
    data.astype(np.uint16).tofile(output)  # Write binary
```

## 预期最终输出
- **一个或两个 `.bin` 文件**：
  - `train.bin` (~27-28GB)
  - `val.bin` (~0.2-0.3GB)
- 准备好使用 memory mapping 进行 nanoGPT 训练
- 无数据丢失 — 只是格式优化

## 快速验证
```bash
# Check original raw size
du -sh /raw/data/path/

# Check .npy shards total
du -sh /output/npy_shards/

# After conversion
ls -lh *.bin
```

**底线**：您的 60GB raw text → 28GB tokenized data 是正确的。2.14× 压缩是正常的，将转换为 `.bin` 是训练前的最后一步。没有任何数据丢失 — 您只是在为 nanoGPT 训练期间高效的 memory-mapped I/O 准备数据格式。