---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘使用情况分析与重复数据
translated: true
type: note
---

磁盘仅使用了124GB，而非240GB。具体明细如下：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  磁盘使用情况 — amd-cloud (MI300X)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

总计：124 GB 已用 / 697 GB (18%)

明细：
  /root/                         81 GB
    /root/zz/datasets/fineweb-edu    40 GB  ← 重复训练数据
    /root/nanoGPT/data/fineweb       28 GB  ← 训练数据
    /root/nanoGPT/out-fineweb-760m   8.5 GB ← 检查点 (ckpt.pt)
    /root/llama.cpp                  385 MB
    /root/zz/logs                    200 KB
  /usr/                          22 GB
  /opt/                          22 GB
  /var/                          694 MB
  /tmp/                          37 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

最大的空间占用：

1. **40 GB** — `/root/zz/datasets/fineweb-edu` — 训练数据副本
2. **28 GB** — `/root/nanoGPT/data/fineweb` — 训练数据（同一数据集）
3. **8.5 GB** — `/root/nanoGPT/out-fineweb-760m/ckpt.pt` — 检查点

你有 **68 GB 的重复训练数据**（同一FineWeb数据集存放在两处）。如需释放空间：

```bash
# 删除重复数据集（保留 nanoGPT 使用的路径）
rm -rf /root/zz/datasets/fineweb-edu    # 释放 40 GB

# 或训练完成后一并删除
rm -rf /root/nanoGPT/data/fineweb       # 释放 28 GB
```

这样可释放 40-68 GB。你在哪里看到240GB？