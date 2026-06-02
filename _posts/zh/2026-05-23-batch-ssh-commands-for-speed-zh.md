---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批量SSH命令加速
translated: true
type: note
---

推送完成。总结如下：

**根因**：每台远程机器需要9次独立的SSH往返。每次SSH握手包括TCP握手、密钥交换和认证。仅DMIT一台就耗时约18秒。

**修复**：将所有命令打包成一个Shell脚本，通过标准输入管道传给 `ssh ... bash`。只需一次连接，一次往返。

**效果**：
  - 本地：0.1秒（无变化）
  - workstation：0.9秒（原约5秒）
  - dmit：2.5秒（原约18秒）
  - 三台合计：3.3秒（原超过30秒）

此外，修复了macOS的回退机制 —— `cmd | awk` 即使 `cmd` 失败，返回值仍为0，导致 `|| fallback` 从不触发。改用显式的 `if command -v` 检查。
