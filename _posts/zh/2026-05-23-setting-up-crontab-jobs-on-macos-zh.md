---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上设置Crontab任务
translated: true
type: note
---

**问题：** 如何在 macOS 上设置 crontab 任务？

**回答：**

macOS 和 Linux 一样使用 `cron`。标准流程：

```bash
# 打开 crontab 进行编辑（使用 $EDITOR，默认为 vi）
crontab -e

# 列出当前 crontab
crontab -l

# 删除所有 crontab 条目
crontab -r
```

**Crontab 语法：**

```
# ┌─ 分钟 (0-59)
# │ ┌─ 小时 (0-23)
# │ │ ┌─ 日 (1-31)
# │ │ │ ┌─ 月 (1-12)
# │ │ │ │ ┌─ 星期 (0-7，0 和 7 表示周日)
# │ │ │ │ │
# * * * * *  命令
```

**常见示例：**

```bash
# 每分钟执行
* * * * * /usr/local/bin/python3 /Users/zhiwei/scripts/job.py

# 每 5 分钟执行
*/5 * * * * /path/to/script.sh

# 每天凌晨 2 点执行
0 2 * * * /path/to/backup.sh

# 每周一早上 9 点执行
0 9 * * 1 /path/to/weekly.sh

# 每小时执行，并记录输出
0 * * * * /path/to/script.sh >> /tmp/cron.log 2>&1
```

**macOS 注意事项：**

**1. 为 cron 授予“完全磁盘访问权限”** — macOS Catalina 及以上版本需要在系统设置 → 隐私与安全性 → 完全磁盘访问权限中，添加 `/usr/sbin/cron`。否则 cron 在访问文件时会静默失败。

**2. cron 环境中的 PATH 非常有限** — cron 运行时只有 `PATH=/usr/bin:/bin`。始终使用绝对路径：

```bash
# 错误
* * * * * python3 script.py

# 正确
* * * * * /usr/bin/env python3 /Users/zhiwei/scripts/script.py

# 或者在 crontab 顶部显式设置 PATH
PATH=/usr/local/bin:/usr/bin:/bin
* * * * * python3 /Users/zhiwei/scripts/script.py
```

**3. 没有 shell 扩展** — `~` 无效。请使用完整路径，如 `/Users/zhiwei/`。

**4. 缺少环境变量** — 你的 `.zshrc`、conda、pyenv 等不会被加载。如果依赖虚拟环境：

```bash
* * * * * /Users/zhiwei/.venv/bin/python /Users/zhiwei/scripts/job.py
```

**5. cron 与 launchd** — Apple 更推荐 `launchd`（基于 plist），但 `cron` 对简单任务来说也完全可用。仅在需要以下功能时才使用 launchd：
- 登录或开机时运行
- 依赖管理
- 节流 / 保活

**快速 launchd 等效示例**（每天凌晨 2 点执行）：

```xml
<!-- ~/Library/LaunchAgents/com.zhiwei.myjob.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.zhiwei.myjob</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>python3</string>
    <string>/Users/zhiwei/scripts/job.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>2</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/myjob.log</string>
  <key>StandardErrorPath</key><string>/tmp/myjob.err</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.zhiwei.myjob.plist
launchctl list | grep zhiwei  # 验证
```

**调试 cron 未运行：**

```bash
# 检查系统日志中的 cron 错误
log show --predicate 'process == "cron"' --last 1h

# 或者
grep cron /var/log/system.log 2>/dev/null || log show --last 30m | grep cron
```

针对你的使用场景（AI 脚本、命令行代理、自动化工具），使用 `cron` 配合虚拟环境的绝对路径是最快的方式。如果任务需要在重启后继续运行或在登录时执行，则使用 `launchd`。