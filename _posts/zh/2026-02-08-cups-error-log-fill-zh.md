---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: CUPS 错误日志快速占满磁盘
translated: true
type: note
---

Question: 为什么 /var/log/cups 变得非常大（占用约 300 GB 的 log files）并导致系统空间耗尽？

Answer:

**/var/log/cups**（尤其是 **error_log**）增长到数百 GB 的最常见原因是 CUPS 进入了 **rapid error-loop**，并以每秒数千次的频率记录相同的错误消息。

典型原因包括：

- **配置错误或无法访问的 network printer**（最常见）
  CUPS 反复尝试连接、ping、探测状态或发送 keep-alive/notifications → 失败 → 记录错误 → 无限重复
  经典的重复消息：
  - `Notifier for subscription dbus:// went away, retrying...`（在 Ubuntu/Debian 上非常常见）
  - `Unable to connect to printer... retrying`
  - IPP backend 错误、LPD timeouts、身份验证失败等。

- **损坏的 printer subscription / notification system**（dbus notifier 挂掉或行为异常）
  CUPS 在紧密循环中不断重试 dbus subscriptions。

- **基于 Snap 或冲突的 CUPS 安装**（例如：snap firefox → 拉取 snapd → 有时与系统级 CUPS 安装或冲突）
  在一些报告的案例中，这导致了海量的重复 logging。

- **冗长的 logging level**（`LogLevel debug` 或 `debug2`）+ 高活跃度/失败率
  （对于 300 GB 级别的情况不太常见，但会使小问题迅速恶化）

- **非常陈旧的卡住的 print jobs 或糟糕的 filters/backends 不断刷新状态更新**

**为什么可能达到 300 GB**
单行日志约为 100–200 bytes。如果以每秒 10–1000 行的速度增长（在紧密循环中很容易达到），空间会迅速填满：

- ~100 lines/sec → 每小时 ~1 GB → 每天 ~24 GB
- 更快的循环（如 dbus retry storms）每小时可达数 GB。

**紧急处理措施**（当磁盘已满时）

1. 立即停止 CUPS 以终止 logging

   ```
   sudo systemctl stop cups
   # 如果系统因空间不足导致 systemd 异常：
   sudo service cups stop
   ```

2. 通过 truncate 或删除巨大的 log 文件来释放空间

   ```
   sudo truncate -s 0 /var/log/cups/error_log
   # 或者
   sudo rm -f /var/log/cups/error_log
   ```

3. 重启 CUPS（仅在修复根本原因后）

   ```
   sudo systemctl start cups
   ```

**长期预防**

- 在 CUPS 中查找并移除/修复有问题的 printer
  → <http://localhost:631> → Administration → Manage Printers → 删除可疑的打印机

- 降低 `/etc/cups/cupsd.conf` 中的 log level

  ```
  LogLevel warn        # 或 error / info (代替 debug)
  ```

  然后重启 CUPS：

  ```
  sudo systemctl restart cups
  ```

- 设置最大 log file 大小（如果你的 CUPS 版本通过 cupsd.conf 或 cupsctl 支持此功能）
  示例（某些发行版 / Web 界面）：限制为 10–50 MB

- 禁用不使用的 printers
  `sudo lpadmin -x printer-name`

- 如果使用 systemd-journald，请检查 journal（有时错误也会记录在那里）
  `journalctl -u cups`

**处于这种情况的大多数人**最终会发现，一个配置错误的 network printer（或者一个已被移除但在 CUPS 中仍有定义的旧打印机）是根本原因。

如果你能分享 `/var/log/cups/error_log` 的 **最后 20–50 行**（通过 `tail -n 50 /var/log/cups/error_log` 获取），通常能精确显示是哪个 printer 或 backend 在循环报错。

References:

- [Ask Ubuntu: Log files (CUPS) grow so fast!](https://askubuntu.com/questions/237019/log-files-cups-grow-so-fast)
- [Stack Overflow: Disk space rapidly decreased because /var/log/cups/error_log has become huge](https://stackoverflow.com/questions/15939532/disk-space-rapidly-decreased-because-var-log-cups-error-log-has-become-huge)
- [Unix & Linux Stack Exchange: CUPS Error log quickly filling up](https://unix.stackexchange.com/questions/709935/cups-error-log-quickly-filling-up)
- [Reddit: Cups Error = Big system log](https://www.reddit.com/r/linuxquestions/comments/1luefu1/cups_error_big_system_log)
