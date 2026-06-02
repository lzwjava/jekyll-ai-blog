---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 内存耗尽导致系统卡死
translated: true
type: note
---

你的问题**并非**出在GPU（4070 Ti在这里几乎没被使用）。这个脚本**纯粹依赖CPU+内存**，在约1.4亿个token后出现卡死+GUI冻结，几乎可以确定是因为**内存耗尽**导致系统开始频繁进行磁盘交换，这会使一切冻结数分钟甚至数小时。

### 为什么发生在约1.4亿–2亿个token时

每个token → 以uint16存储 → 占2字节。

- 1.4亿个token ≈ 280 MB
- 10亿个token ≈ 2 GB
- 100亿个token（完整的FineWeb-10B）≈ 20 GB
- 1000亿+个token（像许多FineWeb/Edu下载的数据集）≈ 200+ GB

但看看你在Python中的`all_tokens = []`列表：Python列表有巨大的开销。在64位Python上，每个整数对象约占28–32字节（即使该值可以用uint16容纳）。

构建列表时的实际内存使用情况：

- 约1.5亿个token放在一个Python列表中 → 约1.5亿 × 28–32字节 ≈ **4–5 GB**，仅用于列表对象本身
- 然后你执行`np.array(..., dtype=np.uint16)` → 紧凑数组又需要约300 MB
- 转换期间的内存峰值总计 ≈ 5–6 GB + 操作系统 + 桌面环境开销

你有62.6 GB内存，为什么在仅1.4亿个token时就冻结了？

因为你的输入文件`train_fineweb.txt`可能**远比你想象的要大**。

人们常常下载FineWeb-100B甚至1T样本，并将其命名为“train_fineweb.txt”。如果你的文件是，比如说，流行的100B token的FineWeb-Edu样本（约200–300 GB的文本文件），那么脚本将不停地读取，`all_tokens`列表将增长到数百亿甚至数千亿个token → 数百GB的内存占用 → 内存不足 → 交换空间抖动 → 整个桌面完全冻结。GPU风扇旋转是因为脚本（勉强）还活着，Python卡在`extend()`或最终的`np.array()`转换中。

### 解决方案（选择其一）

#### 最佳修复：直接流式处理到.bin文件，避免将所有token保留在内存中

这个版本几乎不使用内存（即使是TB大小的文本，峰值内存使用也<1 GB）：

```python
# stream_tokenize_to_bin.py
import os
import numpy as np
import tiktoken

enc = tiktoken.get_encoding("gpt2")
CHUNK_SIZE = 1_000_000  # 每个块处理的字符数，可根据需要调整

def process_file(input_path: str, train_bin: str, val_bin: str, val_ratio=0.0005):
    temp_train = train_bin + '.tmp'
    temp_val = val_bin + '.tmp'

    total_tokens = 0
    val_tokens_written = 0
    val_target = None  # 我们在第一次遍历后或估算后决定

    with open(input_path, "r", encoding="utf-8", errors='ignore') as f, \
         open(temp_train, "wb") as train_f, \
         open(temp_val, "wb") as val_f:

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            tokens = enc.encode_ordinary(chunk)
            tokens_u16 = np.array(tokens, dtype=np.uint16)

            total_tokens += len(tokens_u16)

            # 即时估算验证集分割（足够准确）
            if val_target is None and total_tokens > 10_000_000:
                val_target = int(total_tokens * val_ratio / (1 - val_ratio))

            if val_tokens_written < val_target:
                split_point = min(len(tokens_u16), val_target - val_tokens_written)
                val_f.write(tokens_u16[:split_point].tobytes())
                train_f.write(tokens_u16[split_point:].tobytes())
                val_tokens_written += split_point
            else:
                train_f.write(tokens_u16.tobytes())

            if total_tokens % 50_000_000 == 0:
                print(f"已处理 {total_tokens/1e6:.1f}M 个token")

    # 重命名临时文件
    os.rename(temp_train, train_bin)
    os.rename(temp_val, val_bin)
    print(f"完成！总计约 {total_tokens/1e9:.2f}B 个token")
    print(f"train.bin 和 val.bin 已准备就绪（无内存爆炸）")

if __name__ == "__main__":
    txt_file = "train_fineweb.txt"
    process_file(txt_file, "train.bin", "val.bin")
```

这个版本直接流式写入磁盘，内存中最多只保留一个块的数据。

#### 如果你确实想要原始脚本风格但要确保安全

添加内存监控并对输出进行分片：

```python
# 用这个替代单个巨型列表
MAX_TOKENS_PER_SHARD = 500_000_000  # 每个分片约1 GB

shard_idx = 0
all_tokens = []

for chunk in iter(lambda: f.read(chunk_size), ""):
    if not chunk:
        break
    tokens = enc.encode_ordinary(chunk)
    all_tokens.extend(tokens)

    if len(all_tokens) >= MAX_TOKENS_PER_SHARD:
        arr = np.array(all_tokens, dtype=np.uint16)
        arr.tofile(f"train_shard_{shard_idx:04d}.bin")
        print(f"已保存分片 {shard_idx} - {len(arr)/1e6:.1f}M 个token")
        all_tokens.clear()
        shard_idx += 1
```

之后只需合并分片：`cat train_shard_*.bin > train.bin`

### 快速检查你的文件实际大小

在终端中运行这些命令：

```bash
du -h train_fineweb.txt          # 人类可读的大小
wc -c train_fineweb.txt          # 字节数
ls -lh train_fineweb.txt
```

FineWeb-10B的文本约20–25 GB，100B的约200–250 GB，等等。

### 总结

你的脚本崩溃是因为Python列表消耗的内存比最终的numpy数组多15–20倍。处理大型FineWeb文件时，你很快就会超过50+ GB内存 → 交换 → 桌面冻结。

使用上面的流式处理版本 — 它可以在不到2 GB内存的情况下处理1TB+的文本文件，并在单个CPU核心上几小时内完成。

你的4070 Ti在这里是无辜的；它正在等待那些因为内存耗尽而永远无法送达的数据。
