---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多进程内存溢出流式修复
translated: true
type: note
---

运行良好。以下是概要：

```
进度：3/38 个文件 | 12 个分片 | 1.11B tokens | 5.7M tok/s
内存：6.5 GB / 62 GB（余量充足）
预计剩余时间：约 40 分钟
```

修复方案：

1. **根本原因**：原脚本使用了 `multiprocessing.Pool(16)`。每个工作进程将整个 parquet 文件加载为一个 Python 整数列表。一个文件 = 3.69 亿个 token × 每个 Python 整数约 28 字节 = 每个工作进程约 10 GB RAM。16 个工作进程 = 160+ GB。立即导致 OOM——要么被内核杀死，要么严重交换导致 sshd 甚至无法发送其 banner。

2. **修复**：完全移除了多进程。现在使用 `pq.ParquetFile.iter_batches()` 流式读取行组（每次 8192 行），并将 token 直接写入预分配的 numpy uint16 缓冲区（1 亿 token 占用 200 MB）。单进程，峰值内存约 600 MB。不再经过 Python 列表中间环节。

3. **额外修复**：EOT token 改用 `enc.eot_token`（50256），而非原来的 `enc._special_tokens["
