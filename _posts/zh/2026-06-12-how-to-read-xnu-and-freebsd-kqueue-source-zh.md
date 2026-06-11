---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何阅读XNU和FreeBSD的kqueue源码
translated: true
type: note
---

**问题：** 如何获取 macOS (XNU) 和 BSD 内核源码以阅读实际的 `kqueue`/`kevent` 实现？

**回答：**

macOS 的内核 (XNU) 是开源的。Apple 在 GitHub 的 `apple-oss-distributions` 下发布它，而 kqueue 起源于 FreeBSD，因此两者都获取：

```bash
# XNU — macOS 内核（Mach + BSD 层 + IOKit）
git clone https://github.com/apple-oss-distributions/xnu.git
cd xnu

# kqueue 位于 BSD 层：
ls bsd/kern/kern_event.c        # kqueue/kevent 核心（约 10000 行）
ls bsd/sys/event.h              # struct kevent, EVFILT_* 定义
ls bsd/kern/sys_generic.c       # select/poll 用于对比
```

```bash
# FreeBSD — kqueue 的诞生地（Jonathan Lemon, 2000 年）
git clone --depth 1 https://github.com/freebsd/freebsd-src.git
ls freebsd-src/sys/kern/kern_event.c   # 原始实现
```

在 XNU 的 `bsd/kern/kern_event.c` 中要阅读的关键入口点：

```bash
grep -n "^kevent\|^static.*kqueue_scan\|^kqueue_begin_processing" bsd/kern/kern_event.c
```

- `kevent_internal()` — 系统调用入口，相当于 `do_epoll_wait`
- `kqueue_scan()` — 等待循环；相当于你之前看到的 `ep_poll`。睡眠通过 `waitq_assert_wait64_leeway()` + `thread_block()` 实现，而不是 Linux 的 `__set_current_state` + `schedule_hrtimeout_range()`。XNU 使用 Mach waitqs/continuations，而非 Linux 的等待队列——这是相同“睡眠直到事件或超时”模式背后的结构性差异。
- `knote()` / `knote_post()` — 唤醒源：子系统（套接字、管道、vnode）向附着的 knotes 投递事件，类似于 `ep_poll_callback`。

标签很重要——要读取与*你正在运行的* macOS 匹配的源码：

```bash
git tag | grep xnu | tail -5      # 例如 macOS 15.x 对应的 xnu-11215.x
uname -v                          # 显示你的内核的 xnu 版本字符串
git checkout xnu-11215.81.4       # 匹配它
```

一些实用提示：XNU 也是可构建的——Apple 在 developer.apple.com/download 提供了 KDK（内核调试工具包），如果你需要符号/调试功能；仓库的 README 文档了如何使用 macOS SDK 进行构建。如果不想克隆而只是浏览，`opensource.apple.com/source/xnu/` 上有旧版本，GitHub 的代码搜索在仓库中也很好用。

与你的 epoll 对比的映射：Linux `eventpoll.c` 的 epitem ↔ XNU 的 `knote`；`ep_poll_callback` ↔ `knote_post`；文件描述符的红黑树 ↔ 挂在 fileproc 上的每个 fd 的 `klist`。FreeBSD 的 `kern_event.c` 比 XNU 的简短清晰（XNU 为 libdispatch 添加了 workloop、QoS 和 Mach 端口过滤器），因此如果你想要算法，先读 FreeBSD；如果你想要实际在你的 Mac 上运行的内容，再读 XNU。

**参考资料：**

- [apple-oss-distributions/xnu](https://github.com/apple-oss-distributions/xnu)
- [freebsd/freebsd-src](https://github.com/freebsd/freebsd-src)
- [Apple Open Source](https://opensource.apple.com)