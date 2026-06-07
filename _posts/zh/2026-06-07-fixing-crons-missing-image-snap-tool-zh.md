---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复cron缺失的图像快照工具
translated: true
type: note
---

最新的 cron 任务运行**失败**。以下是摘要：

**错误：** `FileNotFoundError: [Errno 2] No such file or directory: 'imagesnap'`

**根本原因：** cron 环境的 PATH 变量非常有限（`/usr/bin:/bin`），但 `imagesnap` 是 Homebrew 工具，位于 `/opt/homebrew/bin/`。`ww` 二进制文件本身能被找到，是因为 cron 行使用了它的完整路径 `/opt/homebrew/bin/ww`，但当 `appearance smart-auto` 内部调用 `subprocess.run(["imagesnap", ...])` 时，系统无法找到它。

17:24:42 的 cron 邮件显示了完整的回溯信息。每 2 分钟运行一次的任务都会遇到此问题。

**快速修复方案 — 任选其一：**

1. 在 crontab 中添加 PATH：
```
PATH=/opt/homebrew/bin:/usr/bin:/bin
*/2 * * * * /opt/homebrew/bin/ww appearance smart-auto
```

2. 或者将 imagesnap 符号链接到 cron 可访问的路径：
```
sudo ln -sf /opt/homebrew/bin/imagesnap /usr/local/bin/imagesnap
```

方案 1 更简洁。需要我更新您的 crontab 吗？