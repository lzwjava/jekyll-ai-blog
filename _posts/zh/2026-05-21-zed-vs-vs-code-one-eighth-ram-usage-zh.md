---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed 对比 VS Code：八分之一内存占用
translated: true
type: note
---

## Zed vs VS Code

| 指标 | Zed | VS Code |
|---|---|---|
| **进程数** | **2** | **16** |
| **总内存** | **3,148 MB** (3 GB) | **24,190 MB** (24 GB) |
| 每进程内存 | 1.5 GB 平均 | 1.5 GB 平均 |
| 主窗口 | 2.9 GB | 7.0 GB |
| **Snapshot** | 轻量级，原生 (Rust) | 基于 Electron，沉重 |

**Zed 使用的内存仅为 VS Code 的 1/8**，在完全相同的项目目录下。

区别在于架构：
- **Zed** 是原生应用 (Rust/GPUI) — 开销极小，仅 2 个进程
- **VS Code** 基于 Electron (Chromium + Node) — 每个辅助程序都是一个沙盒进程，共 16 个

如果你继续在这台笔记本电脑上使用 Zed 进行轻量级编辑，而将 VS Code 保留给远程机器，那么每次编码时你将节省约 20 GB 的内存。