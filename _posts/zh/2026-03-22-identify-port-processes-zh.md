---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 识别监听特定端口的进程
translated: true
type: note
---

**问题：** 如何找出哪个进程或应用程序正在监听端口 18789？

**答案：**

## 如何找出哪个进程正在监听端口 18789

将以下每个命令中的 `18789` 替换为您要检查的任何端口号。

---

## 🐧 Linux / macOS

### 方法 1：`ss`（推荐 — 现代）

`ss` 是查找特定端口上监听进程的推荐现代工具。

```bash
sudo ss --listening --numeric --processes sport :18789
```

简短形式：
```bash
sudo ss -lntp sport :18789
```

示例输出：
```
Netid  State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
tcp    LISTEN  0       128     0.0.0.0:18789        0.0.0.0:*          users:(("myapp",pid=12345,fd=7))
```

---

### 方法 2：`lsof`

`lsof` 列出 Linux 系统中的所有打开文件；由于网络端口被视为文件，您可以使用 `-i :port_number` 与其一起使用，以找出使用该端口的进程。

```bash
sudo lsof -i :18789
```

示例输出：
```
COMMAND   PID   USER   FD   TYPE  DEVICE  SIZE/OFF  NODE  NAME
myapp   12345   root    3u  IPv4   19373       0t0   TCP   *:18789 (LISTEN)
```

输出显示了 **进程名称**、**PID**、**所有者用户** 和 **文件描述符**。

---

### 方法 3：`netstat`

`netstat` 是显示网络连接的传统工具，仍然被广泛使用。

```bash
sudo netstat -tulpn | grep :18789
```

选项解释：

| 选项 | 含义 |
|---|---|
| `-t` | TCP 连接 |
| `-u` | UDP 连接 |
| `-l` | 仅监听套接字 |
| `-p` | 显示 PID/程序名称 |
| `-n` | 显示数字端口（无 DNS 解析） |

> **注意：** `netstat` 在较新的发行版上可能默认未安装。安装命令：`sudo apt install net-tools`

---

### 方法 4：`fuser`

```bash
sudo fuser -v 18789/tcp
```

示例输出：
```
                     USER        PID ACCESS COMMAND
18789/tcp:           root      12345 F....  myapp
```

---

## 🪟 Windows

### 方法 1：命令提示符中的 `netstat`（以管理员身份运行）

```cmd
netstat -ano | findstr :18789
```

示例输出：
```
TCP    0.0.0.0:18789    0.0.0.0:0    LISTENING    12345
```

最后一个数字是 **PID**。然后查找进程名称：

```cmd
tasklist /FI "PID eq 12345"
```

### 方法 2：PowerShell（一行命令）

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 18789).OwningProcess
```

这直接输出 **进程名称**，无需单独查找 PID。

---

## 快速参考摘要

| 操作系统 | 命令 |
|---|---|
| Linux (modern) | `sudo ss -lntp sport :18789` |
| Linux (lsof) | `sudo lsof -i :18789` |
| Linux (netstat) | `sudo netstat -tulpn \| grep :18789` |
| Windows CMD | `netstat -ano \| findstr :18789` |
| Windows PowerShell | `Get-NetTCPConnection -LocalPort 18789` |

> 💡 如果**没有返回任何内容**，则意味着**当前没有进程正在监听**端口 18789。

**参考资料：**

- [TecMint: Find Which Process is Listening on a Port](https://www.tecmint.com/find-out-which-process-listening-on-a-particular-port/)
- [Baeldung: Finding the PID of the Process Using a Specific Port](https://www.baeldung.com/linux/find-process-using-port)
- [Linux Audit: How to See Which Process is Using a Port](https://linux-audit.com/networking/faq/how-to-see-which-process-is-using-a-port/)
- [nixCraft: How to Check if Port Is in Use on Linux](https://www.cyberciti.biz/faq/unix-linux-check-if-port-is-in-use-command/)
