---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复systemsetup完全磁盘访问权限错误
translated: true
type: note
---

**问题：** 在 macOS Ventura 上运行 `sudo systemsetup -setremotelogin on` 时出现完全磁盘访问权限错误 — 如何修复？

**回答：**

这是 macOS Ventura 的一项变更。`systemsetup` 需要在隐私设置中授予终端（或 iTerm2）**完全磁盘访问权限**。

**修复方法 — GUI 方式（30 秒）：**

1. `系统设置` → `隐私与安全性` → `完全磁盘访问权限`
2. 点击 `+` → 添加你的终端应用（`Terminal.app` 或 `iTerm`）
3. 将其开关切换为 **开启**
4. 重新运行 `sudo systemsetup -setremotelogin on`

---

**替代方案 — 完全跳过 `systemsetup`，直接使用 launchctl：**

```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

这会绕过 `systemsetup` 直接启用 sshd，无需完全磁盘访问权限。

验证：

```bash
sudo launchctl list | grep ssh
# 应该显示 com.openssh.sshd
```

---

**在 Ventura 及以上版本中，launchctl 方法是更干净的做法**，因为苹果正逐步弃用 `systemsetup`。今后建议使用该方法。