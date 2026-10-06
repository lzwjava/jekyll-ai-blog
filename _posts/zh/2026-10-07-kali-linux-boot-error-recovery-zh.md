---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kali Linux 启动错误恢复
translated: true
type: note
---

**问题：** 屏幕卡在这些错误上，无法继续——接下来该怎么办？

**答案：**

屏幕在最后一行 `Get:5` 之后看起来**冻结/卡住**了。系统正在启动，但桌面没有加载。请按以下步骤操作：

---

**步骤 1：先等待 2–3 分钟**
有时 Kali 会恢复并在这些错误后缓慢加载桌面。只需等待。

---

**步骤 2：如果仍然卡住，按下 `Ctrl + Alt + F2`**
这会切换到文本终端。然后运行：
```bash
# 使用你的凭据登录，然后：
sudo fsck -y /dev/sdb4
sudo reboot
```

---

**步骤 3：如果无法输入任何内容——强制重启**
长按电源键 5 秒 → 重新启动 → 在 **Kali GRUB 启动菜单** 处：
1. 高亮你的 Kali 条目
2. 按 **`e`** 编辑启动选项
3. 找到以 `linux` 开头的行
4. 在该行末尾添加：
```
systemd.unit=rescue.target
```
5. 按 `Ctrl + X` 进入救援模式
6. 运行：
```bash
fsck -y /dev/sdb4
reboot
```

---

**步骤 4：终极方案——重新创建持久化分区**

如果 `fsck` 持续失败，说明持久化分区损坏严重。重新创建它：
```bash
# 警告：这将清除你的持久化数据
sudo mkfs.ext4 -L writable /dev/sdb4
```

---

**你卡在哪一步？**——系统最终是否显示登录界面，还是完全冻结？

---

**参考：**
- [Kali Linux 持久化故障排除](https://www.kali.org/docs/usb/usb-persistence/)
- [通过 GRUB 进入 Linux 救援模式](https://wiki.archlinux.org/title/GRUB#Boot_into_rescue_mode)
- [e2fsck 手册页](https://man7.org/linux/man-pages/man8/e2fsck.8.html)