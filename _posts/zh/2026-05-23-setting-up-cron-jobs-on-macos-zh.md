---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上设置Cron作业
translated: true
type: note
---

**问题：** 如何在 macOS 上设置 crontab 任务？

**回答：**

macOS 像 Linux 一样使用 `cron`。标准流程如下：

```bash
# 打开 crontab 进行编辑（使用 $EDITOR 环境变量指定的编辑器，默认是 vi）
crontab -e

# 列出当前 crontab 任务
crontab -l

# 删除所有 crontab 条目
crontab -r
```

**Crontab 语法：**

```
# ┌─ 分钟 (0-59)
# │ ┌─ 小时 (0-23)
# │ │ ┌─ 日期 (1-31)
# │ │ │ ┌─ 月份 (1-12)
# │ │ │ │ ┌─ 星期 (0-7，0 和 7 都代表星期日)
# │ │ │ │ │
# * * * * *  command
```

**常见示例：**

```bash
# 每分钟执行一次
* * * * * /usr/local/bin/python3 /Users/zhiwei/scripts/job.py

# 每 5 分钟执行一次
*/5 * * * * /path/to/script.sh

# 每天凌晨 2 点执行
0 2 * * * /path/to/backup.sh

# 每周一上午 9 点执行
0 9 * * 1 /path/to/weekly.sh

# 每小时执行一次，并记录输出
0 * * * * /path/to/script.sh >> /tmp/cron.log 2>&1
```

**macOS 特定注意事项：**

**1. 为 cron 授予完全磁盘访问权限** — macOS Catalina 及以上版本需要在「系统设置 → 隐私与安全性 → 完全磁盘访问权限」中为 `/usr/sbin/cron` 授权。否则 cron 在访问文件时会静默失败。

**2. cron 的 PATH 环境变量非常有限** — cron 运行时只有 `PATH=/usr/bin:/bin`。务必使用绝对路径：

```bash
# 错误写法
* * * * * python3 script.py

# 正确写法
* * * * * /usr/bin/env python3 /Users/zhiwei/scripts/script.py

# 或者在 crontab 顶部显式设置 PATH
PATH=/usr/local/bin:/usr/bin:/bin
* * * * * python3 /Users/zhiwei/scripts/script.py
```

**3. 不支持 shell 扩展** — `~` 不起作用。请使用完整路径，如 `/Users/zhiwei/`。

**4. 缺少环境变量** — 你的 `.zshrc`、conda、pyenv 等配置文件不会被加载。如果依赖虚拟环境：

```bash
* * * * * /Users/zhiwei/.venv/bin/python /Users/zhiwei/scripts/job.py
```

**5. cron 与 launchd 对比** — Apple 更推荐使用 `launchd`（基于 plist 文件），但对于简单任务，`cron` 也可以正常工作。仅在以下情况使用 launchd：
- 需要在登录/开机时运行
- 需要依赖管理
- 需要节流/保持运行

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
launchctl list | grep zhiwei  # 验证是否已加载
```

**调试 cron 未运行：**

```bash
# 检查系统日志中 cron 的错误信息
log show --predicate 'process == "cron"' --last 1h

# 或者
grep cron /var/log/system.log 2>/dev/null || log show --last 30m | grep cron
```

针对你的使用场景（AI 脚本、命令行工具、自动化工具），使用带绝对路径虚拟环境的 `cron` 是最快捷的方式。如果需要开机自启或登录时运行，则改用 `launchd`。
