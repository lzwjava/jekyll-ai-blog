---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决长时间Rsync备份中的SSH超时问题
translated: true
type: note
---

好问题。让我解释一下实际情况。

========================================================================
  为什么备份总是失败
========================================================================

根本原因：长时间传输过程中 SSH 连接断开。

当你通过 SSH 运行 rsync 时，数据流的路径如下：

  MacBook  ---[SSH 隧道]--->  Ubuntu 机器 (192.168.1.36)

只要 rsync 在运行，隧道就保持开启。如果隧道中断（网络波动、WiFi 干扰、空闲超时），rsync 就会崩溃。

每次的实际状况：

  backup.sh：
    尝试在单个 rsync 调用中发送整个 ~/Projects（27GB）。
    还尝试在单个 rsync 调用中发送整个 ~/Pictures。
    传输中途 SSH 断开 → rsync 崩溃 → 返回码 255。

  fix_backup.sh：
    通过一次发送一个项目来修复 Projects ✓
    但 Pictures 仍然是一个巨大的 rsync 调用。
    在 18 分钟内传输了 1,392 个文件（约 7GB），然后：
    "io timeout after 1083 seconds" → SSH 再次断开。

为什么 SSH 会断开：
  - 照片库有 4,888 个文件，其中许多是 10-80MB 的视频
  - 总计：约 30GB
  - 局域网速度约 3MB/s，需要连续 SSH 约 3 小时
  - 任何因素都可能破坏连接：WiFi 休眠、路由器超时、macOS 电源管理、TCP 空闲超时

========================================================================
  为什么 "COPY"（如 scp）也会遇到同样的问题
========================================================================

scp 和 rsync 底层都使用 SSH。它们都会在单个 30GB 传输时超时。问题不在于 rsync —— 而在于长时间传输过程中 SSH 隧道断开。

========================================================================
  FIX_BACKUP2.SH 如何解决这个问题
========================================================================

不再对整个照片库进行一次大的 rsync：

  之前（fix_backup.sh）：
    一次性 rsync 整个 Pictures/ → 30GB，4888 个文件
    18 分钟后断开

  之后（fix_backup2.sh）：
    rsync Pictures/照片图库.photoslibrary/database/    (133MB) ✓
    rsync Pictures/照片图库.photoslibrary/external/     (0B)    ✓
    rsync Pictures/照片图库.photoslibrary/private/      (3.3GB) ✓
    rsync Pictures/照片图库.photoslibrary/resources/    (1.9GB) ✓
    rsync Pictures/照片图库.photoslibrary/scopes/       (20KB)  ✓
    rsync Pictures/照片图库.photoslibrary/originals/0/  (1.3GB) ✓
    rsync Pictures/照片图库.photoslibrary/originals/1/  (1.9GB) ✓
    ...
    rsync Pictures/照片图库.photoslibrary/originals/F/  (1.2GB) ✓

  每次调用 1-3GB，5-15 分钟完成。
  如果某次失败，只需重做那一个子目录。

--partial 标志：
  通常 rsync 崩溃时会删除不完整的文件。
  使用 --partial，它会保留部分文件。
  下次运行 rsync 时会从中断处继续，而不是重新开始。

--inplace 标志：
  通常 rsync 写入临时文件，然后重命名。
  使用 --inplace，它直接写入目标文件。
  结合 --partial，实现真正的断点续传能力。

ServerAliveInterval=15：
  每 15 秒，SSH 发送一个微小的 "你还在吗？" 心跳包。
  如果没有这个设置，当一段时间没有数据流动（例如 rsync 正在处理文件列表）时，路由器或操作系统可能会关闭连接。

========================================================================
  总结
========================================================================

Mac 上的 rsync（v2.6.9，古老的版本）+ 通过 WiFi 的 SSH + 30GB 照片库 = 必然超时。解决方案是将其拆分为 16 个小块（每个 originals 子目录一个），这样每个块在连接断开之前就能完成。运行一次，如果某一块失败再运行一次，就完成了。