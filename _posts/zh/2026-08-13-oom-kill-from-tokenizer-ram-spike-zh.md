---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OOM从分词器内存峰值引发
translated: true
type: note
---

这就是答案。日志清晰地记录了实际情况。以下是诊断结果：

## 导致"卡死"的原因——是内存不足（OOM）触发进程终止，而非死循环

从 **8月13日 02:31:25** 的 `journalctl` 日志中可以看到：

```
kernel: postgres invoked oom-killer ... cpuset=...app-ghostty...task=python3.12,pid=441877
kernel: Out of memory: Killed process 441877 (python3.12)
        total-vm:43106372kB, anon-rss:38136604kB   <-- 约 43 GB 虚拟内存，38 GB 物理内存
```

被终止的进程是 `python3.12`，**消耗了约 38-43 GB 内存**——这正是你运行的 `train_tokenizer.py`。`mixed.txt` 在 02:19 构建完成，随后分词任务在 02:31 崩溃。

### 为何表现为"卡死"而非直接崩溃
你的机器有 **62 GB 内存，但仅分配了 2 GB 交换空间**。当训练进程膨胀至 40+ GB 并开始侵占页面缓存时，内核必须持续回收内存。由于几乎没有交换空间可用，整个桌面系统开始剧烈内存抖动——持续数分钟无响应——直到 OOM killer 最终介入终止 Python 进程（或你在此之前强制重启）。

### 分词器为何消耗约 40 GB 内存
`tokenizers.ByteLevelBPETokenizer.train()` 虽在 Rust 中执行，但在进行合并操作前会构建完整的**内存词频表**。`mixed.txt` 是包含中英文混合文本的 **11.5 GB / 6670 万行** 文件。对包含大量 CJK 字符的 6670 万行文本进行每个独立 token/词的计数，会生成极其庞大的内部哈希表——在合并步骤之前轻松占据数十 GB 内存。这不是死循环，而是确实需要消耗这么多内存。

## 如何修复以防再次发生

1. **不要用全部 11.5 GB 数据训练 BPE。** 学习 65K BPE 词表不需要完整数据集——从 `mixed.txt` 中**随机采样**几百 MB 到 1 GB 的数据，就能以极低内存获得基本相同的合并结果。先进行采样（例如使用 `shuf -n` 或 `random.sample`）。

2. **增加真实的交换空间**（对于 62 GB 内存来说，2 GB 远远不够）：
   ```bash
   sudo fallocate -l 32G /swapfile2 && sudo chmod 600 /swapfile2
   sudo mkswap /swapfile2 && sudo swapon /swapfile2
   ```
   即使未来内存溢出，数据也会写入磁盘而非导致笔记本卡死。

3. **降低单次运行内存消耗：** 减小 `--vocab-size` 或提高 `--min-frequency`；两者都能缩减工作集大小。

4. **若必须使用全部语料，** 改用内存效率更高的训练工具，如 **SentencePiece**（其 unigram/BPE 训练器采用流式处理，在处理 10GB+ 输入时比 `tokenizers` 的字节级训练器节省大量内存）。

5. **加入监控/进度日志**，以便下次能区分"正常处理"和"内存抖动"——例如在 `timeout` 下运行，或通过 `resource.getrusage` 定期打印 RSS。

结论：笔记本没有故障，脚本也并非无限卡死——**`train_tokenizer.py` 在 11.5 GB 语料上因仅有 2 GB 交换空间而耗尽内存，系统内存抖动导致看似卡死，最终内核 OOM 终止了进程。** 在缺少交换空间的情况下，重启是唯一的逃脱方式。对输入进行采样（或增加交换空间）即可让程序顺利运行完成。