---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: macOS与Linux的Unix传承
translated: true
type: note
---

### macOS 与 Linux 的共同起源

macOS（前身为 OS X）和 Linux 在概念上均源于 Unix——这款开创性多任务操作系统由贝尔实验室于 1970 年代开发。Linux 由 Linus Torvalds 于 1991 年创建，是一个仿照 Unix 但独立开发的开源内核，并非衍生自 Unix 源代码。而 macOS 则构建于 Darwin（苹果基于 FreeBSD 开发的类 Unix 操作系统）之上，其中包含 Unix 组件，并获得了 The Open Group 的 Unix 合规认证。这种同源传承解释了两者在工具与命令上的诸多相似性，因为它们都致力于提供类 Unix 功能。

佐证依据：Unix 标准（如 POSIX）影响了这两个系统以确保兼容性。像 Ubuntu 这类 Linux 发行版明确属于类 Unix 系统，而 macOS 则通过 BSD（伯克利软件发行版）继承了 Unix 工具。

### 为何两者都拥有 'ps' 命令

'ps'（进程状态）命令用于显示运行进程的信息，其起源可直接追溯至 1970 年代首次实现该命令的 Unix 系统。macOS 和 Linux 都包含 'ps' 的原因是：

- 这是它们 Unix 传承的一部分：macOS 通过 Darwin/FreeBSD 继承，Linux 则通过 PROC 文件系统及 GNU 或 POSIX 规范的标准工具集继承
- 该命令对系统诊断、脚本编写和管理至关重要，因此默认捆绑在它们的核心工具集中（如 macOS 的终端或 Linux 的 shell）

虽然选项可能存在细微差异（例如 macOS 使用 BSD 风格标志，Linux 常用 GNU 变体），但像 `ps -p pid -o pid,ppid,lstart,etime,command` 这类命令语法因遵循共同的 POSIX 标准而在两个系统上均受支持。这并非巧合——而是直接源自 Unix 的血脉传承。

### 能否称 macOS 和 Linux 都是 Unix？

严格来说不能："Unix" 既是操作系统家族，也是注册商标。macOS 符合 Unix 标准，因为 Darwin 通过了 The Open Group 认证并符合单一 Unix 规范。而 Linux 作为构成完整操作系统（如 Debian 等发行版）的基础内核，其内核本身及发行版并非官方认定的 "Unix"——由于它们遵循 POSIX 标准却未获得完整认证或共享代码库，因此被归类为类 Unix 或 Unix 兼容系统。

可以说它们是 "类 Unix 系统" 或 "Unix 传统的承载者"，但将 Linux 统称为 "Unix" 并不准确。不过对大多数用户而言，这种区别在实际使用中影响甚微，因为像 'ps' 这样的命令在两者中的行为表现相似。若需严格界定，请查阅认证资料或参考官方定义。
