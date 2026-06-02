---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible 控制节点 Windows 限制说明
translated: true
type: note
---

问题：为什么Ansible控制节点不能在Windows上运行，os.set_blocking在此中扮演什么角色？

答案：

Ansible的控制节点（你运行`ansible`或`ansible-playbook`的机器）**不支持在Windows上运行**，这是因为Python的行为以及Ansible核心代码中对Unix/POSIX的假设存在根本性的技术原因。最常被引用的具体障碍是使用了低级别的文件描述符函数，例如`os.set_blocking()`。

### Windows不被支持的主要原因

1.  **os.set_blocking()仅限Unix**
    在多个地方（尤其是在Ansible的连接插件和进程处理中），Ansible会调用：
    ```python
    os.set_blocking(fd, False) # 使管道或套接字变为非阻塞
    ```
    这个函数**在Windows上不存在**——它是Python 3.5+中仅在类Unix系统上添加的POSIX特定方法。在Windows上尝试调用它会引发`AttributeError`。
    这在Ansible的`ansible-connection`进程和`persistent connection`逻辑中被大量使用。

2.  **严重依赖fork()**
    Ansible历史上广泛使用`os.fork()`（尤其是在“策略”插件完全守护化之前）。Windows没有原生的`fork()`，只有有限的`subprocess`替代方案，这些方案要慢得多并且行为不同。

3.  **POSIX路径、信号、伪终端（pty）和/dev/**
    - 许多模块期望`/bin/sh`、`/usr/bin/python`等。
    - 代码使用`os.kill()`、`signal.SIGTERM`、`pty.fork()`等。
    - Windows直到最近才缺乏真正的`pty`实现（Windows 10+有“ConPTY” API，但Ansible不使用它）。

4.  **Shebang和可执行文件假设**
    几乎所有的Ansible模块都使用`#!/usr/bin/python`或`#!/bin/bash`的shebang，而Windows无法原生解释这些。

5.  **Windows Subsystem for Linux (WSL) 也不受官方支持**
    尽管许多人成功地在WSL/WSL2中运行Ansible，但Red Hat/Ansible**并未官方支持或测试**它，原因在于进程处理、文件描述符行为和偶尔的死锁等方面的细微差异。

### 当前官方状态（截至2025年的Ansible 10.x / ansible-core 2.17+）

-   **控制节点**：仅限Linux、macOS和其他类Unix操作系统
-   **受管节点**：Windows完全支持（通过WinRM/PowerShell远程连接）
-   **没有计划**让Windows成为一流的控制节点平台，因为需要重写的代码量巨大。

### 人们使用的变通方法

-   在WSL2中运行Ansible（目前对大多数情况都有效）
-   使用Linux虚拟机或Docker容器
-   使用Ansible Tower/AWX或Automation Platform，它们无论如何都在Linux上运行

简而言之：导致Windows上立即出现导入/崩溃错误的直接技术障碍是`os.set_blocking()`，但真正的原因要深刻得多——Ansible从一开始就是基于POSIX环境构建的。

*   [Ansible 文档 – 平台支持](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements)
*   [GitHub Issue 讨论 os.set_blocking 在 Windows 上的问题](https://github.com/ansible/ansible/issues/29676)
*   [Ansible 连接框架 – set_blocking 用法](https://github.com/ansible/ansible/blob/devel/lib/ansible/executor/task_executor.py)
