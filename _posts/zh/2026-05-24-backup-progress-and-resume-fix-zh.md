---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 备份进度与恢复修复
translated: true
type: note
---

数据良好。fix_backup2.sh 脚本已在 Mac 上。以下是当前情况：

========================================================================
  状态
========================================================================

项目：47/47 已完成 ✓

图片：部分完成 — 需要续传
  已备份：
    - 小项目（$RECYCLE.BIN、Camera Roll、扫描件等）
    - originals/0：311 个文件（1.3G）
    - originals/1：322 个文件（1.9G）
    - originals/2：291 个文件（1.6G）
    - originals/3：328 个文件（1.9G）
    - originals/4：140 个文件（557M）← 超时时正在传输中
    - originals/5-F：空（未开始）

  剩余：约 3,496 个文件，约 24GB
  （originals 4-9, A-F + private + resources + database）

========================================================================
  FIX_BACKUP2.SH — 在 MacBook 上的路径为 ~/fix_backup2.sh
========================================================================

与 fix_backup.sh 的不同之处：
  - 通过子目录传输 Photos 库（而非一个大型 rsync 命令）
  - 每个子目录大小为 1-3GB（不会超时）
  - 使用 --partial 和 --inplace 参数，使中断的传输可以续传
  - ServerAliveInterval=15 保持 SSH 连接活跃
  - 自动跳过已完成的子目录（通过 rsync 校验）

在 MacBook 上运行：
  bash ~/fix_backup2.sh

如果某个子目录超时，只需重新运行即可 — rsync 会借助 --partial 参数从断点处继续。

预计时间：剩余 24GB 约需 1-2 小时。
