---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用分块修复OOM崩溃
translated: true
type: note
---

完成。重写后的 `scripts/prepare.py` 修复了 OOM 崩溃。

## 问题原因
旧的单次读取路径在 2 GB 输入上会这样：
- `text = f.read()` → 一个约 2–4 GB 的 Python `str`
- `ids = tok.encode(text).ids` → 一个**包含 5 亿多个 `int` 对象的 Python list**（约 15–20 GB，因为 token id > 256 不会被缓存）
- `np.array(ids, dtype=dtype)` 会遍历这个巨型 list → 内存再次飙升 → OOM killer 终止进程。

## 修复内容
1. **对输入分块处理**（每次读取约 1 MiB 字符），并将每个块扩展到下一个 `\n`，确保不会截断 control-token 行、多字节字符或文档边界。BPE 合并保持文档局部性（对精度影响可忽略——大规模 tokenizer 通常就是这样分块的）。
2. **将每个块的 id 列表立即转换为小的 `uint16` 数组**，并通过 `arr.tofile()` 流式写入临时文件，因此每次迭代都会丢弃大的 Python list。峰值内存被限制在约一个块的大小。
3. **按字节偏移切分 train/val**（`split * itemsize`），并以 1 MiB 块流式复制到 `train.bin` / `val.bin`——绝不会把整个 token 流加载到 RAM。
4. 打印进度（`chunks=`、`tokens=`），并在出错时也清理临时文件。

CLI 未变，所以你的命令可以原样使用：

```bash
python3.12 -m scripts.prepare \
    --input mixed_sample_2gb.txt \
    --tok-prefix tok_mixed \
    --out-dir data \
    --val-frac 0.05
```

注意：
- vocab 正好是 65536 → `prepare.py` 使用 **uint16**（它的检查条件是 `<= 65536`，最大 id 65535 可以容纳）。训练器给出的 "vocab > 65535" 警告偏保守；你这边没问题。
- 它会覆盖之前 smoke test 生成的过期 90 KB `data/train.bin` / `data/val.bin`。
- 同一个脚本现在也能安全处理完整的 11 GB `mixed.txt`，如果你之后想用全部数据训练的话。