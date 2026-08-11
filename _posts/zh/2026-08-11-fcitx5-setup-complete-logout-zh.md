---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fcitx5 设置完成 – 请注销
translated: true
type: note
---

所有内容已安装并预配置完毕。以下是完整说明：

## ✅ 已完成的操作

| 步骤 | 状态 |
|------|--------|
| 已安装 `fcitx5`、`fcitx5-chinese-addons`、`fcitx5-config-qt` | ✅ 5.1.19 / 5.1.12 |
| 将 Fcitx5 设为默认输入法（`im-config -n fcitx5` → `~/.xinputrc`） | ✅ |
| 禁用 IBus GNOME 自启动（避免冲突） | ✅ |
| 预写入 `~/.config/fcitx5/profile` — 输入法列表：`keyboard-us`（默认）、**双拼**、拼音 | ✅ |
| 预写入 `~/.config/fcitx5/conf/pinyin.conf` — **小鹤双拼**（`ShuangpinProfile=4`），开启模式 | ✅ |

登录时自动启动由 `im-config` 的 phase-2 钩子处理（`/usr/share/im-config/data/23_fcitx5.rc` 运行 `fcitx5 -d` 并设置 `GTK_IM_MODULE`/`QT_IM_MODULE`/`XMODIFIERS=@im=fcitx`），因此无需额外步骤。

## 🚪 唯一剩下的步骤：登出并重新登录

Fcitx5 无法热加载到正在运行的 GNOME 会话中。重新登录后：

1. 在任何文本输入框中点击托盘图标（或按 `Ctrl+Space`）
2. 输入 `xm` + `空格` → 应显示 **小明** — 这表明小鹤双拼已生效

## 后续验证/调整

```bash
fcitx5-diagnose        # 健康检查
fcitx5-configtool      # 图形界面 — 调整方案、切换全拼回退
```

想要使用其他双拼方案而不是小鹤？编辑 `~/.config/fcitx5/conf/pinyin.conf`（或使用图形界面）：
`ShuangpinProfile=0` 自然码 · `1` 微软双拼 · `2` 紫光 · `3` 智能ABC · `4` 小鹤

⚠️ 提醒一下：我可以帮你触发登出（`gnome-session-quit --logout --no-prompt`）——但这会 **关闭所有打开的应用程序/窗口且不保存内容**。需要我这样做，还是你自行登出？