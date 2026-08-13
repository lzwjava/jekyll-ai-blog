---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内核OOM终止了分词器训练
translated: true
type: note
---

找到了。你的进程**并没有卡住——而是被内核的 OOM killer 终止了**。以下是来自日志（`journalctl`/dmesg）的证据：

```
Aug 13 19:57:28 to kernel: Out of memory: Killed process 32871 (python3.12)
total-vm:88230300kB, anon-rss:60743884kB  (≈ 60 GB RSS)
oom_score_adj:100
```

## 死亡原因

`ByteLevelBPETokenizer`（Rust 的 `tokenizers` 库）会将**整个语料库加载到内存中**，并构建一个庞大的内存合并结构。你的机器有 **62 GiB 内存**，而该进程在 OOM killer 介入前已膨胀到 **~60 GB**。

当前正在运行的命令是 `--input mixed.txt`，这是一个 **11.4 GB** 的文本文件。对于这台机器上的训练器内存模型来说，这太大了。

空白的 `/dev/null` 风格日志（`tok_train_sample.log`，仅 1 字节 = `\n`）是第二个症状，而非独立 bug：当标准输出重定向到文件时，Python 会进行块缓冲输出，而 `print("training on N file(s)")` 这条消息一直停留在缓冲区中，在进程被杀死前从未被刷新。

## 解决方案

让语料库适配内存。你之前创建的 2 GB 样本文件（`mixed_sample_2gb.txt`）大小正好合适——11.4 GB → 60 GB，所以 2 GB 大约会占用 ~10 GB，运行起来会非常轻松。

```bash
python3.12 -m scripts.train_tokenizer \
    --input mixed_sample_2gb.txt \
    --out-prefix tok_mixed \
    --vocab-size 65536
```

如果你必须在完整的 11.4 GB 文件上训练，可以考虑以下选项：

- **分片处理**——在少量 `.jsonl` 分片（脚本已支持输入分片目录）上训练，而不是用一个巨大的文件。
- **提高 `--min-frequency`**（例如 `--min-frequency 5`）以缩小合并表。
- **降低 `--vocab-size`**——内存占用与合并候选项数量成正比。
- 切换到流式训练器（文档字符串中提到了 `nanochat` 的 rustbpe / `prepare.py`），它以流式方式处理数据，无需将整个语料库保存在内存中。

需要我用 2 GB 样本文件启动一次运行并监控它吗？
