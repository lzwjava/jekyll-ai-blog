---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WiFi扫描器无断连
translated: true
type: note
---

已完成。以下是摘要：

创建了 `ww network wifi-scan-best` — 一个无需断开连接即可工作的 WiFi 信号扫描器。

文件变更：

- 新增：`ww/network/wifi_scan_best.py` — 基于 CoreWLAN (macOS) + nmcli (Linux) 的扫描器
- 修改：`ww/main.py` — 添加了 `wifi-scan-best` 子命令及其帮助文本
- 修改：`pyproject.toml` — 增加了 pyobjc-framework-CoreWLAN 依赖
- 修改：`~/.zsh/completions/_ww` — 添加了 Tab 补全条目

用法：
  uv run ww network wifi-scan-best

功能特性：

- macOS：通过 PyObjC 使用 CoreWLAN（真实 RSSI、噪声、信噪比、信道、带宽）
- Linux：回退使用 nmcli
- 按 2.4GHz 和 5GHz 分组显示网络
- 按信号强度排序
- 标记当前连接的网络为 <-- YOU
- 推荐最佳网络并提供可执行的切换命令
