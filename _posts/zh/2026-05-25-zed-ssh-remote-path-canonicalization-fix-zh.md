---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed SSH 远程路径规范化修复
translated: true
type: note
---

## 问题

Zed SSH 远程打开 `ssh://lzw@192.168.1.36/mnt/data/deepseek-v4-inference/` 后显示空项目——目录实际存在且包含 8 个文件（model.py、kernel.py、generate.py 等），但编辑器中什么也没有显示。

## 根本原因

在 `~/Library/Logs/Zed/Zed.log` 中发现两个问题：

1. **路径规范化失败**（主要原因）：
   ```
   ERROR [worktree] failed to canonicalize root path "/mnt/data/deepseek-v4-inference":
   canonicalizing "/mnt/data/deepseek-v4-inference": No such file or directory (os error 2)
   ```
   Zed 远程服务器进程可以看到该路径（它尝试了文件监视），但在执行 `std::fs::canonicalize()` 时失败。可能是远程服务器二进制文件过时，缓存了错误的状态。

2. **inotify 监视限制耗尽**（次要原因）：
   ```
   ERROR [crates/worktree/src/worktree.rs:5018] (remote server) OS file watch limit reached.
   ```
   远程主机的 `max_user_watches=65536`（默认值）——对 Zed 的文件监视器来说太低。

## 已应用修复

| 修复项 | 命令 | 效果 |
|-----|---------|--------|
| 提升 inotify 限制 | `echo 'fs.inotify.max_user_watches=524288' \| sudo tee -a /etc/sysctl.conf && sudo sysctl -p` | 65536 → 524288 |
| 删除过期服务器 | `rm -rf ~/.zed_server/` | 强制 Zed 重新上传新二进制文件（约 100MB） |

## 关键要点

- Zed SSH 远程会自动下载服务器二进制文件到远程主机的 `~/.zed_server/`。如果它变得过时或损坏，删除该目录并让 Zed 重新下载。
- 始终检查客户端的 `~/Library/Logs/Zed/Zed.log`——它也会记录远程服务器的错误（以 `(remote server)` 前缀标识）。
- Zed SSH URL 中的绝对路径需要使用双斜杠：`ssh://host//absolute/path` 而非 `ssh://host/absolute/path`。
- 默认的 inotify 限制（65536）对 Zed 来说太低。在用作 Zed 远程的任何机器上将其提升至 524288。
- 远程机器（Ubuntu 24.04，x86_64）无需安装 Zed——服务器二进制文件是自包含的。

## 备注

已保存至 `notes/2026-05-25-zed-remote-ssh-canonicalization-bug-fixes-en.md`（之前的诊断中已存在）。
