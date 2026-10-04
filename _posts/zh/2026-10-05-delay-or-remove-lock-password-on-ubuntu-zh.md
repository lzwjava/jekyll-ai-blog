---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu上延迟或移除锁屏密码
translated: true
type: note
---

**问题：** 在Ubuntu中，如何延迟屏幕因闲置锁定后出现的密码提示，或者完全关闭密码要求？

**答案：**

**方案一：设置应用（GNOME桌面）**
1. 打开 **设置 → 隐私与安全 → 屏幕锁定**。在旧版本中，它位于 **隐私 → 屏幕锁定** 下。
2. 要 **延迟** 密码提示：保持屏幕锁定开启，并将自动屏幕锁定延迟设置为你想要的时间。如果你更想推迟锁定而非完全移除，这个选项很有用。
3. 要 **禁用** 它：关闭自动屏幕锁定。
4. 同时检查 **空白屏幕延迟**（设置 → 电源）。屏幕变黑与锁定是分开的，如果你不希望显示器关闭，可将此设置为较长时间或“从不”。

**方案二：终端（gsettings）**

```bash
# 停止闲置后锁定
gsettings set org.gnome.desktop.screensaver lock-enabled false

# 或者保持锁定但延迟（屏幕变黑后的秒数）
gsettings set org.gnome.desktop.screensaver lock-delay 7200   # 2小时

# 屏幕变黑前的闲置时间（0 = 从不）
gsettings set org.gnome.desktop.session idle-delay 0
```

注意：lock-delay 是从屏幕变黑时开始计时的。如果想在闲置约 N 小时后才锁定，可将 idle-delay 设置为较长时间（例如 `10800` 表示3小时），并保持 lock-delay 为 `0`。

**从挂起唤醒后不要求输入密码**

```bash
gsettings set org.gnome.desktop.screensaver ubuntu-lock-on-suspend false
```

这是一个与闲置锁定分开的偏好设置，因此如果在睡眠后出现密码提示，你可能也需要修改它。

**其他须知**
- 重启或注销后询问密码来自登录屏幕，而非锁定屏幕。若要移除，请使用 **设置 → 系统 → 用户 → 自动登录**。
- 将 `org.gnome.desktop.lockdown disable-lock-screen` 设置为 true 会完全禁用锁定功能，包括 Super+L 快捷键。这比你通常需要的更激烈。
- 这些步骤适用于 GNOME（Ubuntu 的默认桌面环境）。KDE、Xfce 等其他桌面环境使用不同的设置。
- 如果没有锁屏，任何有物理访问权限的人都可以使用你的会话，因此建议使用较长的延迟而非完全关闭。

参考：
- [How to Turn Off the Lock Screen on Ubuntu](https://macmyths.com/how-to-turn-off-the-lock-screen-on-ubuntu/)
- [How to disable the screen lock in Ubuntu](https://linuxhint.com/disable-screen-lock-ubuntu/)
- [Disable Lock Screen on Ubuntu 22.04](https://linuxconfig.org/?p=14528)