---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 快速启动导致 EXT4 错误
translated: true
type: note
---

**问题：** 更换了不同的固态硬盘后，为什么仍然出现相同的 EXT4 日志 inode 错误？

**回答：**

这张新的截图在最顶部显示了一个**关键的新线索**：

```
磁盘包含未清理的文件系统（0， 0）。
该文件系统未在 Windows 中安全关闭。正在修复。
```

**这告诉了我们真正的根本原因——问题并非出在固态硬盘硬件上。**

---

**实际情况是：**

问题在于你的 **Kali Linux 持久化分区**（`sdb4`，标记为 `writable`）在 **Linux 启动前被 Windows 访问过**。Windows 接触了 EXT4 分区（它无法正确处理），使其处于“脏”状态，随后 Kali 无法干净地挂载该分区。

这种情况发生在：
- 你正在双系统启动 Windows + Kali
- **Windows 快速启动/休眠功能已启用** — Windows 并未完全关机，而是休眠了磁盘状态，从而导致“未清理”标志

---

**修复方法——禁用 Windows 快速启动：**

1. 打开 Windows → **控制面板 → 电源选项**
2. 点击 **“选择电源按钮的功能”**
3. 点击 **“更改当前不可用的设置”**
4. **取消勾选** “启用快速启动”
5. 点击保存 → **完全关机** Windows（不要重启）
6. 再次启动进入 Kali

**另外，从 Live 会话中运行 fsck：**
```bash
sudo fsck -y /dev/sdb4
```

---

**为什么新固态硬盘没有帮助：** 问题出在 **软件/操作系统交互** 上，而非磁盘硬件本身。

---

**参考信息：**
- [为双系统禁用 Windows 快速启动](https://help.ubuntu.com/community/WindowsDualBoot#Fast_Startup)
- [EXT4 未清理文件系统修复](https://wiki.archlinux.org/title/Fsck)
- [Kali 持久化设置指南](https://www.kali.org/docs/usb/usb-persistence/)