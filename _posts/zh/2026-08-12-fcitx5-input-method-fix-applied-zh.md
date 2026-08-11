---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fcitx5 输入法修复已应用
translated: true
type: note
---

完成 ✅ fcitx 输入法已启用。

## Root Cause

你的系统（Wayland 上的 GNOME）的 im-config 的 Wayland 钩子被 Ubuntu 禁用了（`/etc/profile.d/im-config_wayland.sh` 被完全注释掉了），因此在登录时：

- 没有启动 fcitx5
- 环境变量保持为 ibus 默认值（`XMODIFIERS=@im=ibus`）

这就是重启后消失的原因。

## Fixes Applied

| 项目 | 文件 | 目的 |
| ------ | ------ | ------ |
| 自动启动 | `~/.config/autostart/org.fcitx.Fcitx5.desktop` | 登录时运行 `fcitx5 -d` |
| 环境变量 | `~/.config/environment.d/input-method.conf` | 设置 `GTK_IM_MODULE` / `QT_IM_MODULE` / `XMODIFIERS=@im=fcitx`（在登录时由 systemd 读取） |
| 输入法选择 | `~/.xinputrc` | `im-config -n fcitx5` 写入 `run_im fcitx5` |
| 当前运行 | PID 9854 | Shuangpin 配置已加载，拼音 + cloud-pinyin 插件已启用 |

## What You Need to Do

**注销并重新登录**（或重启），以便环境变量和自动启动生效。登录后：

- fcitx5 自动启动，托盘图标：🀄
- **Ctrl + Space** 切换中英文
- 输入法状态栏在右上角显示

## Verification

```bash
pgrep -a fcitx5          # 应显示 fcitx5 进程
echo $XMODIFIERS         # 应为 @im=fcitx（登录后）
```

如果重新登录后仍无法工作，请告知我，我们将检查 GNOME 输入源（`gsettings`）配置。
