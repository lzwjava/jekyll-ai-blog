---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 令牌化任务过载修复
translated: true
type: note
---

好的，现在情况是这样的：

1. 机器是活着的（能 ping 通，22 端口是开放的）
2. sshd 接受 TCP 连接，但从不发送 SSH 横幅——这是严重内存/CPU 匮乏的典型迹象
3. 几乎可以肯定是由 tokenize 任务本身引起的

查看脚本，我找到了可能的元凶：

**问题 1 —— 内存爆炸**  
脚本通过 `mp.Pool` 启动了 16 个工作进程。每个工作进程调用 `pq.read_table()`，将整个 parquet 文件加载到内存中（对于 10GB/38 个文件，每个约 270MB），然后通过 `all_tokens.extend(tokens)` 构建一个巨大的 Python 列表。16 个工作进程并行运行，仅工作进程就很容易占用 5-10+ GB 的内存，再加上主进程。如果机器内存有限，要么静默地 OOM 杀死工作进程（导致 `pool.imap` 永远挂起），要么引发严重的交换抖动，导致系统冻结。

**问题 2 —— 列名不匹配（潜在）**  
文档字符串的第 2 行说“Tokenizes 'code' column”，但第 37 行读取的是 `columns=["content"]`。如果 parquet 文件实际使用的是 `code` 列，每个工作进程会因 `KeyError` 崩溃，进程池挂起，主进程则永远停留在 `pool.imap` 上等待。

**问题 3 —— mp.Pool 挂起**  
如果任何工作进程崩溃（OOM、KeyError 等），`pool.imap` 可能会在 Python 中静默挂起——没有错误，没有输出，只是……什么都不做。这与症状“打印 'Tokenizing with 16 workers...' 然后没反应”相符。

**该怎么办：**

你需要亲自到机器前（或者等它交换足够多以响应）。到达后：

1. 检查进程是否仍在运行或已崩溃：

    ```bash
    ps aux | grep tokenize
    ```

2. 检查 dmesg 中的 OOM 杀死记录：

    ```bash
    dmesg | tail -20
    ```

3. 检查 parquet 文件中的实际列名：

    ```bash
    python3.11 -c "import pyarrow.parquet as pq; t = pq.read_table('/mnt/data/zz/datasets/github-code/0000.parquet'); print(t.schema.names)"
    ```

4. 然后要么：
    - 减少工作进程数：`--workers 2`
    - 或者我可以修复脚本，使用流式读取（`pq.ParquetFile` + `iter_batches`）而不是将整个文件加载到内存中

是的——你必须站起来去看看。机器负载过重，无法 SSH 进入。一旦你能看到屏幕，先检查 `dmesg | tail` 和 `free -h`。如果是 OOM，直接杀死 python 进程，我会在重新运行前修复脚本使其内存高效。
