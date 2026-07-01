---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 精确测量SSH登录延迟
translated: true
type: note
---

**问题：** 如何测量 SSH 登录延迟——可以使用哪些命令行选项或工具来检测像 Andres Freund 注意到 的 500ms 异常延迟？

---

**答案：**

## 测量和检测 SSH 登录延迟的方法

有几种方法，从最简单的单行命令到详细的诊断深入分析。

---

### 方法 1 — `time` 命令（最简单的方法）

这很可能就是 Andres Freund 首先使用的方法。用 `time` 包装你的 `ssh` 命令：

```bash
time ssh user@hostname hostname
```

**正常输出示例：**

```
linux01.localdomain

real    0m0.120s     ← 这是你的总登录往返时间
user    0m0.021s
sys     0m0.008s
```

**异常输出（XZ 后门场景）：**

```
real    0m0.620s     ← 500ms 无法解释的额外延迟！
```

你也可以多次运行以确保一致性：

```bash
for i in {1..5}; do time ssh user@host hostname; done
```

---

### 方法 2 — `-v` / `-vv` / `-vvv` 详细模式（精确定位延迟发生的位置）

使用 `ssh -v user@server_ip` 连接到你的服务器。详细输出提供了连接过程的详细信息，包括认证步骤、密码协商和潜在超时，这可以揭示延迟的具体点。使用 `-vv` 或 `-vvv` 可以进一步增加详细程度。

```bash
ssh -v user@hostname hostname       # 基本详细模式
ssh -vv user@hostname hostname      # 更多细节
ssh -vvv user@hostname hostname     # 最大细节
```

使用 `-vvv` 可以显示每个握手阶段的计时，因此你可以精确识别哪个阶段——TCP 连接、密钥交换、认证或 shell 启动——很慢。

**示例输出，显示时间花费的位置：**

```
debug1: Connecting to hostname [1.2.3.4] port 22.
debug1: Connection established.
debug1: identity file /home/user/.ssh/id_rsa
debug2: kex: server->client ...
debug3: Waited 520ms here   ← 你会看到时间戳中的间隙
debug1: Authentication succeeded (publickey).
```

---

### 方法 3 — `ssh -E logfile` + 时间戳（带计时的日志）

将详细输出写入文件以进行分析，并添加时间戳：

```bash
ssh -vvv -E /tmp/ssh_debug.log user@hostname hostname
# 然后检查日志：
cat /tmp/ssh_debug.log
```

或者通过 `ts`（来自 `moreutils` 的时间戳工具）管道：

```bash
ssh -vvv user@hostname hostname 2>&1 | ts '%.s'
```

这会在每行调试信息前添加 Unix 时间戳，便于发现 500ms 丢失的位置。

---

### 方法 4 — `sshping` 工具（专用的 SSH 延迟基准测试工具）

`sshping` 是一个基于 SSH 的 ping 实用工具，用于测量交互式字符回显延迟和文件传输吞吐量。

```bash
# 安装
sudo apt-get install libssh-dev
# 然后从 https://github.com/spook/sshping 构建

# 运行
sshping -H user@hostname
```

它报告：`ssh-Login-Time`（建立 TCP、认证并形成 SSH 会话的时间）、`Minimum-Latency`、`Median-Latency`、`Average-Latency`、`Maximum-Latency` 和传输速率——全部以人类可读格式。

**示例输出：**

```
ssh-Login-Time:   1.84 s
Minimum-Latency:  633 us
Median-Latency:   751 us
Average-Latency:  764 us
Maximum-Latency:  1.15 ms
Upload-Rate:      9.33 MB/s
```

---

### 方法 5 — 在 sshd 上使用 `strace`（服务器端，深度诊断）

你可以在服务器端的 `sshd` 进程上运行 `strace`，以跟踪系统调用并精确找出守护进程在等待什么——文件读取、网络查找、库调用等。它不适合在关键的生产进程上 100% 安全使用，但对于调试非常强大。

```bash
# 在服务器上，在登录尝试期间找到 sshd 子进程 PID：
ps -ef | grep sshd

# 附加 strace 以带时间戳跟踪系统调用：
strace -tt -p <PID>
```

这本质上就是 Andres Freund 对进程运行 **Valgrind**（一个类似的深度内省工具）时所做的，他注意到了来自 `liblzma` 的异常行为。

---

### 方法 6 — Valgrind（Andres 实际使用的方法）

Andres 使用 Valgrind 进行内存分析基准测试：

```bash
valgrind --tool=callgrind ssh user@host hostname
```

Valgrind 错误指向了 `liblzma`，这拉开了揭露整个 XZ 后门的线程。

---

### 快速参考表

| 方法 | 命令 | 检测内容 |
| --- | --- | --- |
| 基本计时 | `time ssh user@host hostname` | 总登录往返时间 |
| 详细模式 | `ssh -vvv user@host hostname` | 哪个阶段很慢 |
| 带时间戳的日志 | `ssh -vvv ... 2>&1 \| ts '%.s'` | 毫秒级阶段间隙 |
| sshping | `sshping -H user@host` | 结构化的延迟报告 |
| strace（服务器端） | `strace -tt -p <sshd_pid>` | 导致延迟的系统调用 |
| Valgrind | `valgrind ssh user@host hostname` | 内存/库异常 |

---

### 关键要点

对于具体检测 XZ 风格的异常，最实用的日常命令是：

```bash
time ssh user@host hostname
```

如果 `real` 时间持续比预期高 400–600ms（且你的网络 ping 正常），那就是你的警告信号——这正是 Andres 注意到 的情况，这促使他使用 Valgrind 进一步调查，并最终揭露了后门。

---

**参考资料：**

- [Tanel Poder 博客 — 排查 Linux SSH 登录延迟](https://tanelpoder.com/posts/troubleshooting-linux-ssh-logon-delay-always-takes-10-seconds/)
- [PingTesti.com — SSH 延迟解释](https://www.pingtesti.com/en/blog/ssh-latency-explained/)
- [GitHub — spook/sshping](https://github.com/spook/sshping)
- [sshping 手册页 — openSUSE](https://manpages.opensuse.org/Tumbleweed/sshping/sshping.8.en.html)
