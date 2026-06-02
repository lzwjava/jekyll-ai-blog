---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Unix 起源与核心原则
translated: true
type: note
---

Unix 是一个 **multitasking**、**multi-user** 操作系统家族，最初于 1960 年代末和 1970 年代初开发。它深刻影响了现代计算，是 Linux、macOS、BSD 变体以及众多企业系统的基石。

### Unix 简史

- 1960 年代末：Bell Labs、MIT 和 General Electric 合作开发 **MULTICS**（Multiplexed Information and Computing Service），一个分时操作系统。
- 1969：**MULTICS** 项目缩减后，**Ken Thompson** 在 PDP-7 小型计算机上创建了第一个 **UNICS** 版本（后改名为 **Unix**），最初使用汇编语言。
- 1970–1973：**Dennis Ritchie** 和 Ken Thompson 用 **C** 重写——这一革命性决定使 Unix 可移植到不同硬件。
- 1974–1978：Unix 广泛分享给大学（版本 5–7）；1978 年的版本 7 成为未来派生的主要基础。
- 1970 年代末–1980 年代：分化为两大主要分支：
  - **System V**（AT&T 商业版）
  - **BSD**（Berkeley Software Distribution —— 加州大学伯克利分校）
- 1980 年代–1990 年代：商业 Unix 系统出现（Solaris、AIX、HP-UX），同时创建 **POSIX** 标准以提升兼容性。
- 1991：Linus Torvalds 发布 Linux 内核 → 开源类 Unix 系统迅速流行。
- 如今：真正的认证 Unix 系统相对稀少（macOS、某些 Solaris/IBM AIX 版本），但 **Unix-like** 系统（Linux 发行版、macOS）主导服务器、云、超级计算机、嵌入式设备和开发。

### 核心哲学 (Unix Philosophy)

Unix 系统遵循一套至今仍有影响的设计原则：

- **Everything is a file**（设备、套接字、进程——均通过文件接口访问）
- **Do one thing and do it well** —— 小型、专注的程序
- **Use composition** —— 使用管道（`|`）连接简单工具
- **Prefer text streams** —— 通用的、可读的数据格式
- **No policy in the kernel** —— 保持内核小巧并专注于机制

### Unix 系统的核心组件

1. **Kernel**
   操作系统的核心。管理：
   - 进程调度
   - 内存管理
   - 设备驱动
   - 文件系统
   - 系统调用

2. **Shell**
   命令行解释器，读取用户输入并执行命令。流行 shell：
   - **sh**（Bourne shell —— 原始版）
   - **bash**（Bourne-Again SHell —— 最常见）
   - **zsh**（功能丰富，现代 macOS 默认）
   - **fish**、**ksh**、**csh**、**tcsh**

3. **File System Hierarchy**（主要由 Filesystem Hierarchy Standard —— FHS 标准化）
   - `/`               — 根目录
   - `/bin`、`/usr/bin` — 基本及标准用户命令
   - `/sbin`、`/usr/sbin` — 系统管理命令
   - `/etc`            — 配置文件
   - `/home`           — 用户主目录
   - `/var`            — 可变数据（日志、邮件、假脱机）
   - `/tmp`            — 临时文件
   - `/dev`            — 设备文件
   - `/proc`           — 虚拟文件系统，包含进程及内核信息（Linux）

4. **Programs / Utilities**
   数千个小型工具：`ls`、`cat`、`grep`、`awk`、`sed`、`find`、`sort`、`wc` 等。

### Unix 的关键特性

- 从一开始就支持多用户和多任务
- 层次化文件系统（一切从 `/` 开始）
- 强大的安全模型（用户、组、权限 —— rwx）
- 可移植性（归功于 C）
- 强大的命令行界面 + shell 脚本
- 管道和重定向（`|、`、`>`、`＜`、`>>`、`2>`）
- 后台处理（`&`、`nohup`、`screen`、`tmux`）
- 早期内置网络（BSD 中的 TCP/IP）
- 服务器极度稳定

### Essential Unix Commands (Beginner Survival Kit)

| Category       | Commands                              | Purpose / Common Usage                              |
|----------------|---------------------------------------|-----------------------------------------------------|
| Navigation     | `pwd`、`cd`、`ls -la`、`tree`         | 打印当前工作目录、更改目录、列出文件                |
| File ops       | `cp`、`mv`、`rm`、`mkdir`、`rmdir`    | 复制、移动/重命名、删除、创建/删除目录              |
| Viewing/Editing| `cat`、`less`、`more`、`nano`、`vim`  | 显示、分页、简单/完整编辑器                         |
| Text processing| `grep`、`sed`、`awk`、`cut`、`sort`、`uniq`、`wc` | 搜索、替换、处理列、排序、计数                      |
| Permissions    | `chmod`、`chown`、`umask`             | 更改模式/所有者、设置默认权限                       |
| Processes      | `ps`、`top`/`htop`、`kill`、`jobs`、`fg`、`bg` | 列出进程、监控、终止、作业控制                      |
| System info    | `uname -a`、`df -h`、`du -sh`、`free -h`、`whoami`、`uptime` | 内核信息、磁盘使用、内存、身份、上线时间            |
| Finding        | `find`、`locate`、`which`、`whereis`  | 搜索文件、快速数据库搜索、定位可执行文件            |
| Archiving      | `tar`、`gzip`、`gunzip`、`zip`、`unzip` | 打包及压缩文件                                      |
| Networking     | `ping`、`ssh`、`scp`、`curl`、`wget`  | 测试连通性、远程登录/复制、下载                     |

### 快速实用示例

```bash
# List all files (including hidden) in long format
ls -la

# Create directory structure
mkdir -p project/src docs

# Find all .txt files and count lines in them
find . -name "*.txt" -exec wc -l {} \;

# Monitor processes and sort by CPU usage
top

# Copy directory recursively and preserve permissions
cp -a source/ destination/

# Search for "error" in last 100 lines of log (live follow)
tail -n 100 -f /var/log/syslog | grep error
```

### 现代背景 (2026)

如今大多数人使用 **Unix-like** 系统而非认证 Unix：

- **Linux**（Ubuntu、Fedora、Debian、Arch、CentOS Stream / Rocky / AlmaLinux 等）→ 主导服务器和云
- **macOS** → 认证 Unix（BSD 衍生）
- **FreeBSD**、**OpenBSD**、**NetBSD** → 仍在积极开发
- Android（Linux 内核）、iOS（Darwin / macOS 基础）、众多 IoT 和嵌入式系统

学习 Unix 基础意味着掌握直接适用于 Linux、macOS 终端、WSL、容器（Docker）、云服务器（AWS、GCP、Azure）和 DevOps 工作流的技能。

参考文献：

- [Introduction to UNIX System - GeeksforGeeks](https://www.geeksforgeeks.org/linux-unix/introduction-to-unix-system)
- [Unix - Wikipedia](https://en.wikipedia.org/wiki/Unix)
- [UNIX Introduction - Iowa State University HPC](https://www.hpc.iastate.edu/guides/unix-introduction)
- [Introduction to Unix - University of Virginia RC](https://learning.rc.virginia.edu/notes/unix-tutorial/introduction)
