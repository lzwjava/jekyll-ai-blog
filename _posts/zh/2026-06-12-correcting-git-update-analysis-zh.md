---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修正Git更新分析
translated: true
type: note
---

以下是针对 `ww/git/git_update.py` 实际源代码的验证：

**代码实际执行的操作：**

```
第207行：default=32  ← 已确认，32 是 --jobs 的默认值
第278行：max_workers = min(args.jobs, len(valid_paths))  ← 上限为仓库数量
第281行：ThreadPoolExecutor(max_workers=max_workers)  ← 已确认，使用线程而非进程
```

两阶段设计（已确认）：

- 阶段 1（第274-293行）：并行 fetch 所有仓库 → 检查哪些需要 pull
- 阶段 2（第296-311行）：仅 pull 实际发生变更的仓库

Repos.json 包含 161 个仓库（不是 160，但很接近）。

**分析中错误或具有误导性的地方：**

1. **“线程 99% 的时间都在等待网络 RTT”** — 粒度错误。每次 `fetch_repo` 调用（第71-98行）会生成多个子进程调用：
   - `_get_current_branch()` → `git rev-parse --abbrev-ref HEAD`（子进程 #1）
   - `_has_upstream()` → `git rev-parse --abbrev-ref branch@{u}`（子进程 #2）
   - `git fetch`（子进程 #3，实际的网络 I/O）
   - `git rev-list --count HEAD..@{u}`（子进程 #4）

   即每个仓库生成 4 个子进程，而非一次网络往返。每个子进程都有 fork+exec 开销（macOS 上约 1-5ms）。161 个仓库 × 4 次调用 = 644 次子进程生成。

2. **“线程在内核的 epoll/kqueue 中挂起”** — 线程模型根本错误。Python 的 `subprocess.run()` 是阻塞 I/O。线程阻塞在 `waitpid()` 系统调用中等待子进程结束。它并没有使用 epoll/kqueue 异步 I/O。这是一个内核级线程阻塞，而非事件循环。区别很重要：32 个线程 = 32 个 OS 线程，每个消耗约 8KB 内核栈内存，而不是单个线程上的 32 个异步句柄。

3. **“等待时占 0% CPU”** — 具有误导性。Python 线程确实在休眠，但每个 `git` 子进程会占用 CPU 进行：
   - SSH 密钥交换 / TLS 协商（CPU 密集型加密）
   - Git 协议协商（包协议解析）
   - 接收对象的 SHA-1 哈希验证
   - 包文件解压缩和索引

   当同时运行 32 个 git 进程时，你*确实会*看到显著的 CPU 使用率。该说法混淆了“Python 线程休眠”与“系统空闲”。

4. **“每个 git 进程打开约 5-10 个 FD”** — 低估了。每次 `fetch_repo` 顺序生成 4 个子进程。峰值时，32 个并发线程 × 1 个活动子进程 × 约 5 个 FD = 约 160 个 FD。但父 Python 进程还有线程栈、管道缓冲区等的 FD。实际峰值约为 200-400 个 FD。仍在 `ulimit -n 2560` 范围内，但数字是错误的。

5. **“DMIT 代理瓶颈”** — 从代码中无法验证。代码仅调用 `git fetch`，此处未显示任何代理配置。hysteria2 是否在 OS/代理层面或 `~/.ssh/config` 中配置，属于此代码外部的事情。

**分析中正确的部分：**

- 默认值 32 已在代码中确认（第207行）
- `ThreadPoolExecutor` 适用于 I/O 密集型工作
- GitHub 确实会限制并发 SSH 连接（有文档记录的行为）
- 考虑到每个仓库有 4 个子进程的开销，每个“fetch”花费的时间超过一个 RTT，因此超过约 32 的收益递减是合理的
- `min(args.jobs, len(valid_paths))` 的上限意味着 32 大致相当于每批处理约 5 个仓库（161/32 ≈ 5），这能使线程池保持饱和而不产生过多排队

**32 工作良好的真正原因：**

这与网络 RTT 或 epoll 无关。关键在于每次 `fetch_repo` 会执行 4 次顺序子进程调用，每次都有 fork+exec+waitpid 开销。使用 32 个线程，你可以重叠约 32 个并发 `git fetch` 调用的网络等待时间，而其他调用的子进程生成开销则可以忽略不计。超过 32 时，你生成的 git 进程数量超过了 GitHub 愿意同时服务的数量，因此它们在服务端排队。瓶颈是 GitHub 的 SSH 连接接受速率，而不是你的本地线程。
