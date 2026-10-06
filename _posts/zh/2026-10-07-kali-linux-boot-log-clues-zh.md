---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kali Linux 引导日志线索
translated: true
type: note
---

**问题：** 这个系统实际上运行的是 Kali Linux 吗？你如何判断？

**答案：**

是的，这几乎可以肯定是 **Kali Linux**。以下是引导信息中可见的线索：

---

**线索 1：`file:/cdrom resolute`**

```
Ign:1 file:/cdrom resolute InRelease
Get:2 file:/cdrom resolute Release [664 B]
Get:4 file:/cdrom resolute/restricted amd64 Packages
Get:5 file:/cdrom resolute/main amd64 Packages
```

- **"resolute"** 是 **Kali Linux 2024.4** 的代号
- 这是 Kali 的 APT 包源从 ISO/光盘中读取

---

**线索 2：`/dev/disk/by-label/writable` → `/log-persistence`**

- 这完全是 **Kali Live USB 持久化** 设置
- Kali 默认将其持久化分区命名为 **"writable"**
- 没有其他发行版使用完全相同的标签/挂载组合

---

**线索 3：`passwd: password changed`**

- Kali Live 在启动时自动重置默认的 `kali/kali` 凭据

---

**总结：**

| 你所运行的系统 | 详细信息 |
| --- | --- |
| 操作系统 | Kali Linux |
| 版本 | 2024.4 ("resolute") |
| 模式 | 带有持久化的 Live USB |
| 持久化分区 | `/dev/sdb4` 标签为 `writable` |

这是一个运行 Kali Linux 的 **可引导 USB 驱动器**，并非传统安装在 SSD 上的操作系统。

---

**参考：**

- [Kali Linux 发布版本 — "resolute"](https://www.kali.org/blog/kali-linux-2024-4-release/)
- [Kali Live USB 持久化](https://www.kali.org/docs/usb/usb-persistence/)
