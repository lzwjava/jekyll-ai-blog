---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: MS-DOS 简介
translated: true
type: note
---

Question: Provide a comprehensive introduction to MS-DOS.

Answer:

**What is MS-DOS?**

MS-DOS (Microsoft Disk Operating System) 是由 Microsoft 为基于 x86 的个人电脑开发的 command-line 操作系统。它是一个单用户、单任务的 OS，依赖于通过键盘输入的文本命令，没有 graphical user interface (GUI)。它于 20 世纪 80 年代初发布，在那十年间成为 IBM PC 兼容机的主导操作系统，并在个人计算的兴起中发挥了关键作用。

**History and Origins**

MS-DOS 起源于 86-DOS（也称为 QDOS，即 Quick and Dirty Operating System），由 Seattle Computer Products 的 Tim Paterson 于 1980 年编写。它本质上是 CP/M (Control Program for Microcomputers) 的克隆版，专为 Intel 8086 处理器适配，并进行了诸如 FAT12 file system 等改进。

1981 年，Microsoft 以 75,000 美元购买了 86-DOS 的权利，将其更名为 MS-DOS，并作为 PC-DOS 授权给 IBM 用于原始的 IBM PC。Microsoft 保留了将其出售给其他制造商的权利，导致其在克隆机和兼容机上被广泛采用。

早期版本在 floppy disks 上运行，随后的更新增加了对 hard drives、更大存储空间和新硬件的支持。

**Key Versions Timeline**

- **MS-DOS 1.0 (1981)**：初始版本，与 IBM PC-DOS 1.0 同步；基本的文件管理，支持 160KB floppy disks。
- **MS-DOS 2.0 (1983)**：引入了 subdirectories、hard disk 支持和更好的 device drivers。
- **MS-DOS 3.0 (1984)**：支持 1.2MB floppies 和更大的 hard drives。
- **MS-DOS 3.3 (1987)**：增加了 1.44MB floppy 支持和更大的 partitions；应用广泛。
- **MS-DOS 4.0 (1988)**：引入了 DOS Shell（图形化菜单）并支持超过 32MB 的 partitions；存在一些稳定性问题。
- **MS-DOS 5.0 (1991)**：改进了 memory management、全屏 editor，以及首个零售升级路径。
- **MS-DOS 6.0–6.22 (1993–1994)**：增加了磁盘压缩 (DoubleSpace/DriveSpace)、antivirus 工具和更好的 utilities；6.22 是最后一个独立版本。
- **MS-DOS 7.0/7.1 (1995)**：集成到 Windows 95/98 中。
- **MS-DOS 8.0 (2000)**：Windows Me 的一部分；没有独立发布版。

开发工作于 2000 年左右停止。

**Features and Architecture**

- **Command-Line Interface**：用户通过 prompt（例如 `C:\>`）进行交互，输入命令来管理文件、运行程序和配置系统。
- **File System**：使用 FAT (File Allocation Table)，从 FAT12 开始，演进到 FAT16。
- **Memory Management**：最初限制为 640KB conventional memory；后期版本增加了对 extended/expanded memory 的支持。
- **Modular Design**：包括 IO.SYS (BIOS interface)、MSDOS.SYS (kernel) 和 COMMAND.COM (shell)。外部命令是独立的 .COM 或 .EXE 文件。
- **Batch Files**：.BAT 文件允许通过 scripting 实现自动化。
- **Limitations**：单任务（一次只能运行一个程序，通过 TSRs 实现有限的后台任务），没有内置的 multitasking 或多用户支持。

**Common Commands**

Internal 命令（内置于 COMMAND.COM）：
- `DIR`：列出目录内容。
- `CD`：切换目录。
- `MD`/`MKDIR`：创建目录。
- `RD`/`RMDIR`：删除目录。
- `COPY`：复制文件。
- `DEL`：删除文件。
- `REN`：重命名文件。
- `TYPE`：显示文件内容。

External 命令（独立的 executable 文件）：
- `FORMAT`：格式化磁盘。
- `CHKDSK`：检查磁盘完整性。
- `FDISK`：对 hard drives 进行分区。
- `EDIT`：文本编辑器（后期版本）。

**Legacy and Modern Relevance**

MS-DOS 推动了个人电脑革命，但随着 GUI 的兴起而衰落。Windows 3.0 (1990) 运行在其之上，Windows 95 (1995) 将其深度集成。后来的 Windows 版本为了兼容性而模拟 DOS。

今天，它在通用用途上已经过时，但仍用于历史或教学研究。Microsoft 在 GitHub 上发布了 1.25、2.0 和 4.0 版本的 source code。像 DOSBox 这样的 emulators 允许运行旧的软件和游戏。FreeDOS 等开源替代品延续了它的精神。

MS-DOS 的简单性、在低功耗硬件上的高效性以及庞大的软件生态系统，使其成为现代计算的奠基石。

References:

- [MS-DOS - Wikipedia](https://en.wikipedia.org/wiki/MS-DOS)
- [What is MS-DOS? - TechTarget](https://www.techtarget.com/searchenterprisedesktop/definition/MS-DOS)
- [MS-DOS | Britannica](https://www.britannica.com/technology/MS-DOS)
- [Microsoft DOS History - Computer Hope](https://www.computerhope.com/history/dos.htm)
