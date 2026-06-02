---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Crontab 命令指南精要
translated: true
type: note
---

Question: Comprehensive introduction to crontab command options

Answer:

Linux/Unix 系统中的 `crontab` 命令用于管理用户的 cron tables —— 这些文件安排了由 cron daemon 自动执行的定期任务（cron jobs）。

### Main crontab command modes
主要有两种语法形式：

1. **从文件（或 stdin）安装/替换 crontab**：
   ```
   crontab [ -u username ] filename
   crontab [ -u username ] -
   ```
   - 从指定文件（或在使用 `-` 时从标准输入）读取 crontab 内容，并将其安装为该用户的 crontab。
   - 这是批量导入或恢复 cron jobs 最常用的方式。

2. **操作当前/现有的 crontab**：
   ```
   crontab [ -u username ] -l | -r | -e [options]
   ```

### Most common options (几乎在所有系统中都可用)

- `-e`
  使用 `$VISUAL` 或 `$EDITOR` 中定义的编辑器编辑当前用户的 crontab（如果未设置，则退回到 `vi`/`vim`）。
  这是交互式创建或修改计划任务最常用的选项。

- `-l`
  在标准输出上列出（显示）当前的 crontab。

- `-r`
  完全移除（删除）当前的 crontab。
  **警告**：除非你有备份，否则此操作不可逆。

- `-u username`
  操作指定用户的 crontab，而不是当前用户。
  在大多数实现中需要 root 权限（或相应的 sudo 权限）。
  示例：`sudo crontab -u www-data -e`

### Additional / less universal options (取决于 cron 的实现版本)

- `-i`
  交互/确认模式 —— 与 `-r` 配合使用。
  在移除 crontab 前要求确认。
  示例：`crontab -r -i`

- `-s`
  以 "system" 格式显示 crontab（如果适用，显示 SELinux 安全上下文）。
  主要适用于使用 SELinux 的系统。

- `-T` (语法测试 / 验证模式 —— 在 Vixie cron、systemd timers 相关实现等现代版本中可用)
  测试 crontab 文件的语法而不安装它。
  示例：`crontab -T myjobs.txt`
  如果有效则返回 exit code 0，否则返回非零值。在 scripts/CI 中非常有用。

- `-n hostname` / `-c`
  非常罕见 —— 主要见于专门的或分布式 cron 变体（不是标准的 Vixie cron）。

### Quick reference table of typical usages

| Command                        | What it does                              | Needs root? | Most common use case                  |
|-------------------------------|-------------------------------------------|-------------|---------------------------------------|
| `crontab -e`                  | 编辑你自己的 crontab                     | No          | 日常编辑                              |
| `crontab -l`                  | 显示你当前的 cron jobs                   | No          | 检查已安排的任务                      |
| `crontab -r`                  | 删除你的整个 crontab                     | No          | 清理 / 重置                           |
| `sudo crontab -u bob -e`      | 编辑 bob 的 crontab                       | Yes         | 系统管理                              |
| `crontab -u www-data -l`      | 显示 Web server 的计划任务               | Usually yes | 调试 Web app 自动化                   |
| `crontab newjobs.txt`         | 将 newjobs.txt 安装为你的 crontab         | No          | 部署 / 恢复任务                        |
| `crontab -T script.cron`      | 验证文件的语法（不安装）                  | No          | CI/CD 流水线，安全检查                |
| `crontab -r -i`               | 带确认地删除                             | No          | 更安全的删除方式                      |

### Important notes

- **不带选项** + filename → 用该文件的内容替换当前的 crontab。
- `crontab -` → 从 stdin 读取（在脚本中非常有用：`cat jobs | crontab -`）。
- 使用 `crontab -e` 所做的更改会在你保存并退出编辑器时自动安装。
- 大多数系统将用户 crontabs 存储在 `/var/spool/cron/crontabs/`（不可直接编辑）。
- 在进行风险操作前，始终使用 `crontab -l > backup.txt`。

关于 crontab 文件本身的语法（5个时间字段 + 命令），请参阅 `man 5 crontab`。

References:

- [https://man7.org/linux/man-pages/man1/crontab.1.html](https://man7.org/linux/man-pages/man1/crontab.1.html)
- [https://man7.org/linux/man-pages/man5/crontab.5.html](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [https://linux.die.net/man/1/crontab](https://linux.die.net/man/1/crontab)
