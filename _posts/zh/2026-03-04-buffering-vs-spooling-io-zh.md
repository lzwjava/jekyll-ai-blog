---
audio: false
generated: true
image: false
lang: zh
layout: post
title: I/O系统中缓冲与假脱机
translated: true
type: note
---

**问题：比较 I/O 中的 buffering 和 spooling**

**答案：**

在输入/输出操作的上下文中，以下是 **buffering** 和 **spooling** 的清晰比较：


| 方面                    | Buffering                                      | Spooling (Simultaneous Peripheral Operations On-Line) |
|-------------------------|------------------------------------------------|---------------------------------------------------------|
| **主要目的**            | 通过在内存中收集数据来减少慢速 I/O 操作的数量  | 允许程序以 CPU 速度运行，同时 I/O 独立发生（将 CPU 与慢速设备解耦） |
| **主要目标**            | 提高 **performance**（throughput & latency）   | 启用 **multiprogramming** 并更好地利用设备               |
| **发生位置**            | 在 operating system kernel 或 application libraries（stdio 等）内部 | 通常在 operating system 中（特别是在 batch/multiprogramming 系统） |
| **典型设备**            | 所有慢速设备：disk、network、keyboard、terminal、printer 等 | 主要为非常慢的输出设备：printers、card readers/punches、plotters、tape drives |
| **数据流方向**          | 输入 **和** 输出                               | 主要是 **output**（print spooling 是经典示例），有时输入 |
| **数据存储**            | 小到中等的 **memory buffer**（几 KB – 几 MB）  | 大的 **disk area**（spool files / spool directory）– 可达数十 MB 到 GB |
| **数据生命周期**        | 非常短（直到 buffer 满/刷新）                  | 可持续几分钟到几小时（直到物理设备完成 printing/reading） |
| **控制者**              | OS kernel + runtime libraries（libc、Java 等） | 通常是 operating system spooler / print server subsystem |
| **允许程序在 I/O 完成前结束？** | 否 – 当 buffer 满/刷新时程序等待               | **是** – 程序认为一旦数据写入 disk spool，I/O 就完成了 |
| **经典示例**            | `printf()` / `fwrite()` 对 stdout/file 的 buffering | Print spooling – 将作业发送到 printer queue             |
| **开销**                | 非常低（仅 memory copy）                       | 更高（创建/删除 spool files 的 disk I/O）               |
| **在现代系统中使用？**  | 大量使用（几乎每个 I/O 操作）                  | 仍在使用（printing、batch job submission），但对用户不太可见 |
| **多用户支持**          | **不** 天然解决 contention                     | 设计用于解决 contention – 多个程序可以同时“print”       |
| **典型 buffer 大小**    | 4 KB – 64 KB（通常 8 KB 或 4 KB page size）    | Megabytes 到 gigabytes（取决于 spool space）             |

### 快速总结 – 一行区分

- **Buffering** = 使用 **memory buffer** 来减少 **physical I/O operations** 的数量
- **Spooling** = 使用 **disk space** 作为大 buffer 来 **完全解耦** 快速 CPU 与非常慢的 peripheral device

### 当今（2026）最常见的真实世界示例

- **Buffering**
  - 几乎每个 `write()`/`read()` 调用
  - `stdout` 的 line buffering / block buffering
  - TCP send/receive buffers
  - Filesystem page cache

- **Spooling**
  - 现代 network print spooling（CUPS、Windows Print Spooler、cloud printing）
  - HPC clusters 中的 batch job queues
  - 一些在写入 tape/library 前 queue 数据的 backup systems

**参考文献：**

- Operating Systems Concepts (Silberschatz, Galvin, Gagne) – I/O Systems 章节
- Modern Operating Systems (Tanenbaum) – I/O software layers 和 spooling 部分
