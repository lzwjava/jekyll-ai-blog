---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Rsync 双盘备份指南
translated: true
type: note
---

**Question:** 假设我有两个磁盘，需要备份总共 50 GB 的文件。我该如何使用 rsync 在我的电脑和两块便携式磁盘之间进行同步？

**Answer:**

对于使用 **两块便携式磁盘**（例如两个外部 USB 驱动器）的简单备份策略，最常用且可靠的方法是：

- 将你的 **computer**（源文件夹）视为唯一的 Single Source of Truth。
- 使用 rsync 分别将该源 **mirror** 到 **每一块** 便携式磁盘（每块磁盘运行一次 rsync）。
- 这样你将拥有两个独立且完全相同的备份。

rsync **不支持** 在一个命令中原生复制到多个目的地（除非使用高级 batch mode 或脚本），因此你需要运行两次——每个磁盘一次。

### 推荐的 rsync 命令 (macOS / Linux)

连接两个便携式磁盘。假设：

- 你要备份的文件位于：`~/ImportantData/`（或 `/path/to/your/50GB/folder/`）
- 磁盘 1 挂载为：`/Volumes/BackupDisk1`
- 磁盘 2 挂载为：`/Volumes/BackupDisk2`

使用这套 **安全且常用** 的选项：

```bash
# 第一次备份 — 到磁盘 1
rsync -avh --progress --delete \
  --exclude='.*' \
  --exclude='Desktop' --exclude='Downloads' --exclude='Library' \
  ~/ImportantData/  "/Volumes/BackupDisk1/ImportantData Backup/"

# 然后到磁盘 2（相同的命令，只需更改目的地）
rsync -avh --progress --delete \
  --exclude='.*' \
  --exclude='Desktop' --exclude='Downloads' --exclude='Library' \
  ~/ImportantData/  "/Volumes/BackupDisk2/ImportantData Backup/"
```

关键选项说明：

- `-a` = archive mode（递归 + 保留 permissions, times, symlinks 等）
- `-v` = verbose（显示正在发生的情况）
- `-h` = human-readable sizes（更易读的文件大小）
- `--progress` = 显示每个文件的传输进度（对于 50 GB 非常有用）
- `--delete` = 删除备份磁盘上在源中已不存在的文件（实现真正的 mirror/backup）
- `--exclude='.*'` = 跳过 macOS 隐藏文件（.DS_Store, ._* 文件等）——在 macOS 上非常常见，用于避免垃圾文件
- 可以为永远不想备份的文件夹添加更多 `--exclude`（例如 caches, temp files）

### 第一次 vs. 后续备份

- **首次运行**（目的地为空）：将复制所有约 50 GB 的数据 → 耗时最长（取决于 USB 速度，可能需要数小时）。
- **后续运行**（incremental）：仅处理更改、新增或删除的文件 → 通常非常快（几秒到几分钟）。

### 更好/更安全的变体

1. **先添加 --dry-run**（模拟运行 — 强烈推荐！）：

```bash
rsync -avh --dry-run --progress --delete ~/ImportantData/ "/Volumes/BackupDisk1/ImportantData Backup/"
```

运行此命令 → 检查输出 → 确保没有意外删除任何内容。

2. **保留修改时间 & extended attributes**（在 macOS 上表现良好）：

```bash
rsync -aEvh --progress --delete ...
# -E 保留 macOS 扩展属性 / resource forks
```

3. **记录备份日志**（对以后检查非常有用）：

```bash
rsync -avh --progress --delete --log-file=~/backup-log-$(date +%Y-%m-%d).txt \
  ~/ImportantData/ "/Volumes/BackupDisk1/ImportantData Backup/"
```

4. **使其完全自动化**（编写一个脚本）：

创建一个文件 `backup.sh`：

```bash
#!/bin/bash

SOURCE="$HOME/ImportantData/"
DEST1="/Volumes/BackupDisk1/ImportantData Backup/"
DEST2="/Volumes/BackupDisk2/ImportantData Backup/"

echo "Backing up to Disk 1..."
rsync -avh --progress --delete --exclude='.*' "$SOURCE" "$DEST1"

echo "Backing up to Disk 2..."
rsync -avh --progress --delete --exclude='.*' "$SOURCE" "$DEST2"

echo "Backup finished at $(date)"
```

然后运行：`bash backup.sh`

### 针对便携式磁盘 50 GB 备份的提示

- 使用 USB 3.0+ 接口和驱动器 → 比 USB 2.0 快得多。
- 首次备份：在夜间或不需要使用电脑时进行。
- 备份后正确弹出磁盘（`diskutil eject /Volumes/BackupDisk1`）。
- 如果磁盘仅用于备份 → 将它们格式化为 **APFS** (macOS) 或 **exFAT** (cross-platform)。
- 如果你需要轮换/历史记录（而不仅仅是镜像），可以考虑替代工具：rsync 配合 `--backup --backup-dir=../backups/$(date +%Y-%m-%d)` 或者 rsnapshot/Borg 等工具。

这能让你获得两个独立的、最新的备份——轮换使用它们（例如，将一个存放在异地）以获得更好的保护。

**References:**

- [https://apple.stackexchange.com/questions/224747/using-rsync-to-backup](https://apple.stackexchange.com/questions/224747/using-rsync-to-backup)
- [https://deepakness.com/blog/ext-hdd-backup](https://deepakness.com/blog/ext-hdd-backup)
- [https://serverfault.com/questions/137119/can-i-rsync-to-multiple-destinations-using-same-filelist](https://serverfault.com/questions/137119/can-i-rsync-to-multiple-destinations-using-same-filelist)
- [https://askubuntu.com/questions/556580/using-rsync-to-backup-to-two-locations](https://askubuntu.com/questions/556580/using-rsync-to-backup-to-two-locations)