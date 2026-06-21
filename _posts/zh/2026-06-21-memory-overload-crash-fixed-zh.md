---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内存过载崩溃已修复
translated: true
type: note
---

已完成。以下是完整内容：

---

综合总结

问题
-------

分词脚本导致工作站（192.168.1.36）挂起/崩溃，使其过载到 sshd 甚至无法完成 SSH 横幅交换——TCP 端口 22 接受连接但从未响应。需要物理重启。

根本原因
----------

原始脚本使用了 `multiprocessing.Pool(16)` 配合 `pool.imap()`。16 个工作进程各自：

1. 通过 `pq.read_table()` 将整个 parquet 文件加载到内存中（磁盘上约 280 MB，解压缩后更大）
2. 遍历行并将 token 积累到一个 Python 列表（`all_tokens.extend()`）
3. 一个 parquet 文件产生约 3.69 亿个 token。包含 3.69 亿个 int 对象的 Python 列表约占用 10 GB RAM（每个 Python int 开销约 28 字节）
4. 16 个工作进程并行运行 = 在 62 GB 的机器上需要 160+ GB RAM

结果：内核 OOM killer 或灾难性的交换抖动。机器冻结到 sshd 因缺乏 CPU/内存而无法发送其横幅。

此外，当工作进程被 OOM 杀死时，`pool.imap()` 在主进程中静默挂起——没有错误，没有输出，只有“正在使用 16 个工作进程进行分词...”后永远沉默。

修复方案
-------

重写了脚本，包含三个关键更改：

1. 不使用多进程：单进程。每个 parquet 文件已经非常巨大（约 3.7 亿 token），当瓶颈是内存而非 CPU 时，并行化没有好处。

2. 流式读取 parquet：将 `pq.read_table()`（加载整个文件）替换为 `pq.ParquetFile.iter_batches(batch_size=8192)`——一次处理 8192 行，从不将整个文件保留在内存中。

3. 使用 NumPy 缓冲区累积：将 Python 列表（`all_tokens.extend()`）替换为预分配的 numpy uint16 数组，大小 1 亿 token（200 MB）。token 直接写入此缓冲区并跟踪索引。缓冲满时，作为 .npy 分片写入磁盘。完全没有中间 Python 列表。

结果
------

  输入：38 个 parquet 文件，10.2 GB
  输出：141 个分片（1 个验证 + 140 个训练），磁盘上 27 GB
  token 数量：约 140.7 亿
  耗时：41.1 分钟（约 570 万 token/秒）
  峰值内存：约 600 MB（旧脚本需要 160+ GB）

下一步：训练。输出位于 `/mnt/data/zz/datasets/github-code-tok/`，采用 nanoGPT 二进制格式，可直接使用。
