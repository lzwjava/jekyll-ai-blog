---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 CUPS DBus 权限错误
translated: true
type: note
---

Question: 从 error_log 的末尾显示 "File /usr/lib/cups/notifier/ddbus has insecure permissions" 和 "notifier for subscription went away retrying"。为什么会出现这种情况以及如何修复？

Answer: 

你看到的这些信息非常常见，并且直接解释了日志体积剧增的原因（在你的案例中达到了 300 GB）：

- **"File \"/usr/lib/cups/notifier/dbus\" has insecure permissions"**（注意：通常拼写为 **dbus**，而不是 ddbus —— 你的消息中可能有一个小的拼写错误）  
  CUPS 拒绝使用 dbus notifier，因为该文件的权限设置过于宽松（通常为 0777 = -rwxrwxrwx 或类似权限，而不是安全的 0755 = -rwxr-xr-x）。

- **"Notifier for subscription dbus:// went away, retrying!"**  
  由于 notifier 二进制文件因权限不当被拒绝，dbus subscription 进程立即失败 → CUPS 立即在紧密循环中重试 → 这导致每秒记录数千次 warning/error 对 → 在几分钟到几小时内产生巨大的 error_log 文件。

这个循环之所以开始，是因为你之前在 /usr/ 上运行的 chown -R 命令（源于 npm prefix 错误）修改了许多文件的所有权/权限，包括 /usr/lib/cups/notifier/dbus（可能还有整个 /usr/lib/cups/notifier 目录）。

**修复步骤**（请按此顺序操作）

1. **立即停止 CUPS** 以停止日志洪水并释放 CPU/磁盘 I/O  
   ```
   sudo systemctl stop cups
   # 或者如果 systemctl 暂时无法工作：
   sudo service cups stop
   ```

2. **立即释放空间**（如果你想保留旧日志，truncate 比 rm 更安全）  
   ```
   sudo truncate -s 0 /var/log/cups/error_log
   # 或者删除它：
   sudo rm -f /var/log/cups/error_log*
   ```

3. **修复 notifier 文件的权限**  
   正确的权限通常是 **755**（所有者可执行，其他人可读/可执行），并且所有者为 **root:root**（在某些发行版上可能是 daemon:lp / lp:lp —— 但 root:root 是安全且通用的）。  
   运行：  
   ```
   sudo chown root:root /usr/lib/cups/notifier/dbus
   sudo chmod 755 /usr/lib/cups/notifier/dbus
   ```

   如果整个 notifier 目录都受到了影响，也请修复它（虽然是过度修复但很安全）：  
   ```
   sudo chown -R root:root /usr/lib/cups/notifier
   sudo chmod -R 755 /usr/lib/cups/notifier
   ```

4. **（可选但通常需要）清除滞留的 subscriptions**  
   破损的 subscriptions 即使在修复后也可能继续重试：  
   ```
   sudo rm -f /etc/cups/subscriptions.conf*
   sudo systemctl restart cups   # 或 sudo service cups restart
   ```

5. **重启 CUPS 并验证**  
   ```
   sudo systemctl start cups
   sudo systemctl status cups
   ```

   然后简要观察日志：  
   ```
   tail -f /var/log/cups/error_log
   ```
   重复的错误应该会停止。如果打印仍然无法工作，请访问 http://localhost:631 并检查/删除有问题的打印机。

**如果 sudo 仍无法工作**（由于你之前的 chown 破坏）：  
使用之前提到的 live USB / recovery mode 方法，以 root 身份运行这些 chown/chmod 命令。

**预防 / 更好的默认设置**  
恢复后，在 `/etc/cups/cupsd.conf`（或 `/etc/cups/cupsd.conf.d/` 文件）中设置较低的日志级别：  
```
LogLevel warn
```
然后重启 CUPS。

如果你根本不使用打印功能，可以永久禁用 CUPS：  
```
sudo systemctl disable --now cups
```

这个具体问题（dbus notifier 权限 + 重试循环）在多年来的无数 Ubuntu/Debian/Mint 报告中曾导致磁盘被 50–250+ GB 的日志填满 —— 几乎总是由于在 /usr 中误用了递归 chown/chmod 导致的。

References:

- [Ask Ubuntu: cupsd using 100% CPU, creating large (80GB+) error_log](https://askubuntu.com/questions/648807/cupsd-using-100-cpu-creating-large-80gb-error-log)
- [GitHub apple/cups issue: CUPS filled my drive with giant error_log file](https://github.com/apple/cups/issues/5804)
- [Stack Overflow: Disk space rapidly decreased because /var/log/cups/error_log has become huge](https://stackoverflow.com/questions/15939532/disk-space-rapidly-decreased-because-var-log-cups-error-log-has-become-huge)
- [Linux Mint Forums: Error log has filled my hard disk](https://forums.linuxmint.com/viewtopic.php?t=284580)