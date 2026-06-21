---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内存压力下的SSH横幅停滞
translated: true
type: note
---

**问题：** 当机器处于严重内存/CPU压力下时，为什么 sshd 能接受 TCP 连接却从不发送其横幅消息？

**答案：**

## SSH 横幅问题的根本原因

SSH 握手有两个阶段：

```
客户端                服务端
  |                    |
  |--- TCP SYN ------->|   ← 22 端口开放，内核接受（环形缓冲区）
  |<-- TCP SYN-ACK ----|   ← 即使在冻结的机器上也能工作
  |--- TCP ACK ------->|
  |                    |
  |<-- SSH-2.0-OpenSSH-|   ← 这条消息永远不会到达
        (横幅)
```

TCP 握手（SYN/SYN-ACK/ACK）由**内核的网络栈**处理——它位于内核空间，即使 userspace 完全冻结也能运行。内核有一个套接字接受队列，它可以自动完成 TCP 连接。

但发送 SSH 横幅需要 **sshd 实际运行**——它是一个 userspace 进程。它需要：

1. 被 CPU 调度器调度
2. 从内核队列中 `accept()` 连接
3. 为会话分配内存
4. 向套接字写入 `SSH-2.0-OpenSSH-x.x\r\n`

如果机器正在交换或 CPU 资源匮乏，sshd 永远不会被调度，或者尝试分配内存并阻塞等待交换页面载入——因此横幅永远不会到达。你的 SSH 客户端只能……等待。

---

## 为什么 Tokenize 作业会导致这个问题

### 内存路径

```
16 个工作进程 × 270MB parquet 文件 = 仅原始读取就占用 4.3 GB
+ 每个工作进程中的 tokenized 输出列表
+ 主进程内存
+ 操作系统页面缓存
─────────────────────────────────────────────────────
在一台 16GB 或 32GB 的机器上很容易达到 10–15 GB 总量
```

当内存耗尽时，内核开始交换。机械硬盘上的交换速度约为 100 MB/s。机器需要交换数 GB 的数据——它基本上会被冻结。每个进程（包括 sshd）都在等待 I/O 将代码/堆栈页调入内存才能运行。

### CPU 路径

使用 `mp.Pool` 开启 16 个工作进程，而机器（例如）只有 8 个核心，这意味着调度器需要在 16 个 CPU 密集型的 Python 进程和主进程之间切换。sshd 优先级低，会被饿死。

### `pool.imap` 中的静默挂起

```python
for result in pool.imap(worker_fn, files):
    ...  # 主进程在此处永远阻塞
```

如果某个工作进程被内核的 OOM killer 杀死（`SIGKILL` 来自 OOM killer），`pool.imap` 不会抛出异常——它只是永远不会产生该结果。主进程则停留在 `for` 循环中等待。没有超时，没有错误。这是 Python `multiprocessing` 的一个众所周知的陷阱。

---

## 为什么 Ping 能工作而 SSH 不能

| 操作 | 由谁处理 | 能否在内存饥饿下存活 |
|---|---|---|
| `ping` 回复（ICMP echo） | 内核网络栈 | ✅ 可以 |
| TCP SYN-ACK（端口 22） | 内核 TCP 栈 | ✅ 可以 |
| SSH 横幅 | sshd userspace 进程 | ❌ 不能 |
| 任何 SSH 命令 | bash + userspace | ❌ 不能 |

即使在极端条件下，内核也能部分维持存活——它处理中断、网络数据包以及 OOM killer 本身。Userspace 首先消亡。

---

## 修复方法（流式处理方式）

不加载整个 parquet 文件，而是采用：

```python
import pyarrow.parquet as pq

def worker_streaming(path):
    pf = pq.ParquetFile(path)
    tokens = []
    for batch in pf.iter_batches(batch_size=1000, columns=["content"]):
        for text in batch.column("content").to_pylist():
            tokens.extend(tokenizer.encode(text))
    return tokens
```

这样每个工作进程的内存占用只包含大约 `batch_size` 行，而不是整个文件。同时将工作进程数量减少到 2–4 个，这样就不会成倍增加压力。
