---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内核分析修正I/O等待细节
translated: true
type: note
---

现在我从内核源码中获得了完整信息。以下是结论：

---

## 结论：分析在 I/O 密集型行为的方向上正确，但机制细节有误

### 1. "线程在内核的 epoll/kqueue 中挂起" — 错误

该分析声称 Python 线程通过 `epoll/kqueue` 等待。内核源码显示了两种完全不同的机制：

**对于 subprocess.wait()（即 `subprocess.run()` 实际执行的操作）：**
```
kernel/exit.c:1711-1734  (do_wait)
  1722:  set_current_state(TASK_INTERRUPTIBLE)
  1728:  schedule()    ← 线程让出 CPU，从运行队列中移除
  1731:  __set_current_state(TASK_RUNNING)  ← 子进程退出时唤醒
```
这是**子进程退出时的等待队列**，而非 epoll。线程在 `waitpid()` 中休眠，直到子进程退出。没有 epoll，没有 kqueue，没有事件循环。

**对于实际的 epoll（如果 Python 使用 asyncio）：**
```
fs/eventpoll.c:2013-2032  (ep_poll)
  2013:  __set_current_state(TASK_INTERRUPTIBLE)
  2029:  schedule_hrtimeout_range()  ← 带超时休眠
  2032:  __set_current_state(TASK_RUNNING)
```
相同的休眠机制，不同的唤醒源。

**此外：Linux 没有 kqueue。** kqueue 是 BSD/macOS 的概念。该分析混淆了 macOS 和 Linux 的内核概念。

### 2. "等待时 CPU 占用为 0%" — 部分正确但具有误导性

内核代码确认 Python 线程确实处于休眠状态：
```
kernel/sched/core.c:6625  (try_to_block_task)
  block_task(rq, p, flags)  ← 完全从运行队列中出队
```

TASK_INTERRUPTIBLE 状态的线程会被**从运行队列中移除**——调度器甚至不会查看它们。因此 Python 线程的 CPU 占用为 0%。但：

- 每个 `git` **子进程**都在运行并消耗 CPU（SSH 加密、协议协商、SHA-1）
- 在 32 个并发工作线程的情况下，有 32 个 git 子进程在活跃消耗 CPU
- "CPU 几乎什么都不做"的说法在系统级别上是错误的

### 3. "每个 git 进程打开约 5-10 个文件描述符……32 个工作线程时约 200-300 个文件描述符" — 错误

```
kernel/fork.c:1634-1637  (copy_files)
  if (clone_flags & CLONE_FILES) {
      atomic_inc(&oldf->count);  ← 仅递增引用计数
      return 0;
  }
```

Python 的 `pthread_create` 使用 `CLONE_FILES`，因此所有 32 个线程共享**一个文件描述符表**。不是 32 × 5-10 = 160-300 个文件描述符，而是总共约 5-10 个文件描述符（每个活跃的 git fetch 共享一个套接字和一个包文件，使用同一张表）。

### 4. "GitHub 连接限流——限制每个 IP 的并发 SSH 连接数" — 看似合理但机制有误

内核源码显示了服务器端连接丢弃机制：
```
net/ipv4/tcp_input.c:7612-7626  (tcp_conn_request)
  7615:  inet_csk_reqsk_queue_is_full(sk)  ← SYN 队列满？
  7623:  sk_acc...full(sk)            ← 接受队列满？
  7624:  NET_INC_STATS(...LINUX_MIB_LISTENOVERFLOWS)
  7625:  goto drop                         ← 内核丢弃连接
```

这是**服务器端内核在 accept 队列溢出时丢弃连接**。但这针对的是 TCP 连接，而非 SSH 连接。GitHub 的 SSH 限流很可能发生在应用层（sshd 的 MaxSessions、MaxStartups），而非内核 TCP 队列溢出。

### 5. "macOS 文件描述符开销" — 在 Linux 上不相关

该分析提到了 `kqueue` 和 macOS 的文件描述符开销，但：
- Linux 中不存在 kqueue（这是 Linux 内核源码）
- 代码运行 Python 的 `subprocess.run()`，该函数使用 `waitpid()`，而非 kqueue
- 如果在 macOS 上运行，`kqueue` 是正确的机制，但该分析将两者混为一谈

### 6. 真正的瓶颈——经内核代码验证

实际的瓶颈由 TCP 代码确认：

```
net/ipv4/tcp_input.c:7615
  if (syncookies == 2 || inet_csk_reqsk_queue_is_full(sk)) {
      want_cookie = tcp_syn_flood_action(sk, ...);
      if (!want_cookie)
          goto drop;  ← SYN 队列满 → 丢弃
  }

net/ipv4/tcp_input.c:7623
  if (sk_acc...full(sk)) {
      NET_INC_STATS(...LINUX_MIB_LISTENOVERFLOWS);
      goto drop;  ← accept 队列满 → 丢弃
  }
```

当 GitHub 的 sshd 存在过多待处理连接时，内核的 accept 队列会填满，新的 TCP 连接被丢弃。这是真正的"限流"机制——不是应用层的 SSH 限制，而是内核层的 TCP 队列溢出。

### 总结表

| 观点 | 结论 | 内核证据 |
|-------|---------|-----------------|
| 线程在 epoll/kqueue 中 | **错误** | 使用 waitpid() 等待队列 (kernel/exit.c:1722) |
| 等待时 CPU 占用 0% | **部分正确** | 线程休眠 (core.c:6625)，但 git 子进程消耗 CPU |
| 32 个工作线程时 200-300 个文件描述符 | **错误** | CLONE_FILES 共享文件描述符表 (fork.c:1634) |
| GitHub 限流 | **看似合理** | TCP accept 队列丢弃连接 (tcp_input.c:7623) |
| macOS 上的 kqueue | **上下文错误** | Linux 有 epoll，没有 kqueue |
| TASK_INTERRUPTIBLE = 无调度 | **正确** | block_task() 从运行队列中出队 (core.c:6625) |

结论：该分析在高层次行为上正确（I/O 密集型，超过 32 后收益递减），但内核机制有误。Python 线程不使用 epoll——它们使用 waitpid() 等待队列。它们不创建独立的文件描述符表。而且 kqueue 属于 macOS，而非 Linux。