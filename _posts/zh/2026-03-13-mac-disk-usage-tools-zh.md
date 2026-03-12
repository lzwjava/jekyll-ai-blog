---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mac 磁盘使用工具指南
translated: true
type: note
---

你正在寻找的是 **`du`**（disk usage）——这是 macOS 上用于此的经典 CLI 工具。这里是最实用的方法：

## 使用 `du` 的快速命令

**在当前文件夹中查找最大目录：**
```bash
du -sh */ | sort -hr
```
- `-s` = 汇总（每个目录的总计）
- `-h` = 人类可读（GB、MB 等）
- `sort -hr` = 按大小降序排序

**递归查找最大项目：**
```bash
du -sh ./* | sort -hr | head -20
```

**针对特定路径（例如 Downloads）：**
```bash
du -sh ~/Downloads/* | sort -hr | head -10
```

---

## 更好的替代方案（更交互式）

**`ncdu`** —— 这可能就是你记得的那个。它是交互式的，便于探索大型文件夹：
```bash
brew install ncdu
ncdu ~/Downloads
```
然后使用箭头键导航，按 `d` 删除，按 `q` 退出。比原始的 `du` 更用户友好得多。

**`dust`** —— Rust 编写的替代品，输出更干净：
```bash
brew install dust
dust -r ~/Downloads  # -r = 反向排序（从最大开始）
```

---

## GUI 工具（如果你喜欢点选式操作）

- **Disk Diag** —— 以视觉方式显示占用空间的内容
- **Grand Perspective** —— 免费的，你的磁盘的可视化树状图
- **CleanMyMac** —— 付费，但会自动扫描并建议清理

---

## 一行命令彻底删除大型旧文件

删除超过 30 天且大于 100MB 的文件：
```bash
find ~/Downloads -type f -mtime +30 -size +100m -delete
```

**哪个工具让你觉得熟悉？** 如果不是 `ncdu`，请告诉我——还有 `lsof` 用于跟踪当前正在使用空间的文件，或 `fsearch` 用于快速文件搜索。