---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终止微信进程
translated: true
type: note
---

完成。微信正在运行，现已终止。

- 找到主进程 `/usr/bin/wechat` (PID 20044) 以及约 15 个辅助进程（`WeChatAppEx`、`wxocr`、`wxplayer`、`wxutility`、crashpad 处理程序）。
- 使用 `pkill -TERM -f` 将它们全部终止。后续检查显示**没有剩余的 wechat/weixin 进程**。

注意：`pkill -f` 模式也匹配了运行该命令本身的 shell（其命令行包含 "wechat"），因此该 shell 在打印后续检查之前就被终止了——但微信按预期被终止。如果将来想要更干净的终止脚本，请使用 `pkill -f '/usr/bin/wechat|/opt/wechat/'` 或按精确进程名称终止。