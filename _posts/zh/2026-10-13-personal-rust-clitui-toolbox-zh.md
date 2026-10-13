---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 个人 Rust 命令行/终端界面工具箱
translated: true
type: note
---

**`/home/lzw/projects/ll`** 是一个个人 Rust CLI/TUI 工具箱 — 一个分派子命令的单一二进制文件（`ll`），以及一些附带实验。

## 主二进制文件（Rust、ratatui + crossterm + sysinfo）

`src/main.rs` 将第一个参数路由到子命令：

| 命令 | 功能 | 模块 |
| --- | --- | --- |
| `cargo run`（默认） | 在带边框的框中居中显示 "Hello" 的 TUI（`run_hello`，按 `q` 退出） | `main.rs` |
| `info` | 实时仪表盘：CPU 品牌/核心数/使用率、内存、磁盘表 | `main.rs` |
| `gcloud` | 显示 Google Cloud 账号和配置信息 | `src/gcloud.rs` |
| `uno` | Arduino UNO 串口监视器（使用 `serialport` crate） | `src/uno.rs` |
| `word2vec` | Word2Vec 训练 — Mikolov 实现的 Rust 移植版，多线程，带 epoch 循环 | `src/word2vec.rs`（约 39 KB，最大的文件） |

## 附带实验

- `quicksort.py`、`Quicksort.java` — 对 10,000 个数字进行排序的快速排序基准测试，用于与 Rust 版本进行语言比较。
- `sketch_jul9a/sketch_jul9a.ino` — Arduino sketch，每 3 秒闪烁一次 LED（与 `uno` 子命令配合使用）。

注：README 略有过时 — 它只提到了 `info` TUI 和快速排序基准测试，但代码后来增加了 `gcloud`、`uno` 和 `word2vec` 子命令。
