---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git源代码探索
translated: true
type: note
---

这是 **Git 源代码**——由 Linus Torvalds 编写的实际分布式版本控制系统。你当前位于 `/Users/lzwjava/projects/git` 目录，其中包含 git 本身的完整 C 源代码树。

你会找到的关键文件：
- **Core**：`builtin/`（命令）、`object-store/`、`refs/`、`diff.c`、`merge.c`
- **xdiff/**：diff/merge 算法（patience, histogram）
- **Transport**：`remote-curl.c`、`send-pack.c`、`fetch-pack.c`（协议处理）
- **Pack 文件**：`pack-objects.c`、`index-pack.c`
- **Refs**：用于 ref 存储后端的 `refs/` 目录

该项目约 60 万行 C 代码，使用 Makefile 构建，并通过 autoconf 进行配置。

你在这里探索什么——研究 git 内部原理、贡献补丁，还是其他目的？
