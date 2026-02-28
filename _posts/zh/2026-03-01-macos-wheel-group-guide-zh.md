---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS wheel 组简单解释
translated: true
type: note
---

**问题：** macOS 中的 wheel 组是什么？

**答案：**

macOS 中的 **wheel** 组是一个从其 BSD Unix 根源继承的特殊用户组。

### 历史背景
- 在传统的 BSD Unix 系统（macOS 基于此）中，**wheel** 组用于控制对 `su` 命令（成为 root/超级用户）的访问。
- 只有 **wheel** 组的成员才被允许使用 `su` 来获得 root 权限。
- “wheel” 这个名字是俚语，指有权势或重要的人（“big wheel”）。

### 在现代 macOS 中（包括 macOS Ventura、Sonoma、Sequoia 等最近版本）
- **wheel** 组的原始管理角色已被 **admin** 组大部分取代。
- macOS 上的常规管理员账户被添加到 **admin** 组（通常还有 **staff**）。
- **admin** 组控制大多数提升权限，包括不受限制地使用 `sudo`（通过 `/etc/sudoers` 文件）。
- **wheel** 仍然存在（它有 GID 0，与 root 的 UID 0 相同），但现在主要是遗留/兼容占位符。
- 通常，唯一成员是 **root** 用户本身。
- 普通管理员用户**不**在 wheel 组中。

### 今天你可能看到的实际用途
- 许多系统文件和目录（特别是在 `/System`、`/usr`、`/bin` 等）将 **wheel** 列为其组所有者。
- `/private/tmp`（因此 `/tmp`）目录由 **wheel** 组拥有 → 你在那里创建的文件通常显示组 **wheel**（这是正常的，从父目录继承；它不会提供额外访问，因为默认权限通常是 644/755）。
- 你可能在 Finder 的“Get Info”窗口或在 Terminal 中运行 `ls -l` 时看到文件权限中的 **wheel**。

简而言之：  
当前 macOS 上，**wheel** 主要是历史遗物，实际意义非常有限——真正的管理组是 **admin**。

你可以使用 Terminal 中的这些命令检查组成员资格：

```bash
groups          # shows groups for your current user
id -Gn          # same, more detailed
dscl . -read /Groups/wheel
```

**参考资料：**

- [What is the "wheel" user in macOS/OS X?](https://superuser.com/questions/191955/what-is-the-wheel-user-in-macos-os-x)
- [Wheel (computing) - Wikipedia](https://en.wikipedia.org/wiki/Wheel_(computing))
- [How does group 'wheel' get on my files? - Ask Different](https://apple.stackexchange.com/questions/275521/how-does-group-wheel-get-on-my-files)
- [What is the difference between the default groups on Mac OS X?](https://superuser.com/questions/20420/what-is-the-difference-between-the-default-groups-on-mac-os-x)