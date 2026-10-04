---
audio: false
generated: true
image: false
lang: zh
layout: post
title: dd前USB被弹出：修复
translated: true
type: note
---

找到根本原因了。日志揭示了发生了什么：

```
20:51:30  storagekitd: ejected disk, id = /dev/disk12, success.      ← disk EJECTED
20:51:46  kernel: dd(84861) deny(1) file-write-create /dev/rdisk12   ← your dd ran AFTER the eject
```

**你的U盘在20:51:30被弹出——早于你的`dd`运行**（通过Finder的弹出按钮/Disk Utility，或者线缆松脱）。`dd`随后尝试写入一个已不存在的设备 → `Operation not permitted`。

### 修复：重新插入并一次性刷写

**1. 物理拔出U盘并重新插入**（等待约3秒）。

**2. 确认它已重新连接** — 运行以下命令并告诉我它获得的编号：

```bash
diskutil list
```

**3. 一旦它出现，立即连续运行以下命令**（中间不要弹出任何设备，不要点击Finder中的弹出图标，不要让任何东西自动挂载）：

```bash
diskutil unmountDisk /dev/diskNN     # NN = number from step 2
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdiskNN bs=4m status=progress conv=fsync
```

这将需要大约2–5分钟。等待`xxxx+0 records out`和提示符返回后再拔出。

---

⚠️ 两个避免再次发生的提示：
- 在`dd`之前不要使用Disk Utility / Finder弹出 — 只能使用`diskutil unmountDisk`（卸载 ≠ 弹出）。
- 如果macOS在重新插入后自动挂载，那没关系 — 在`dd`之前立即卸载。

插入U盘并粘贴`diskutil list`的输出 — 在你运行`dd`之前，我会和你确认设备编号。