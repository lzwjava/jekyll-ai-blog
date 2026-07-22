---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信Ubuntu @所有人图标闪烁
translated: true
type: note
---

问题：当群聊中有“@所有人”通知时，Ubuntu 上的微信会闪烁图标吗？

答案：

会的，**正常情况下应该会**。

在 Linux（Ubuntu）版微信中，当收到重要的未读消息，例如：

* `@你`
* `@所有人`
* 私聊消息

桌面集成通常会将该应用标记为需要关注。根据你的桌面环境，你会看到以下一种或多种表现：

* 微信的 dock/任务栏图标 **flashing 或 pulsing**。
* 图标上出现 **红色未读 badge**。
* 图标在 Ubuntu Dock 中高亮显示。
* 桌面通知（如果通知已开启）。

图标是否真的**持续 flashing** 更多取决于**你的桌面环境**而非微信本身：

* **Ubuntu GNOME**：通常显示 badge/高亮；部分版本会短暂动画图标，而非持续 flashing。
* **KDE Plasma**：任务管理器通常会闪烁任务项，直到你聚焦该窗口。
* **Xfce/MATE/Cinnamon**：行为各异。

如果你**没有**看到任何提示，请检查：

```bash
# 通知守护进程是否正在运行？
ps aux | grep notification

# GNOME 通知设置
gsettings get org.gnome.desktop.notifications show-banners
```

同时确认：

* 微信的通知已开启。
* “请勿打扰”模式已关闭。
* 你使用的是原生 Linux 客户端，而非通过 Wine 或其他兼容层运行微信，因为通知行为会有所不同。

`@所有人` 通常与 `@你` 的提及同等对待，因此如果通知已开启，它应该会生成通知和未读指示器。但持续 flashing 由桌面 shell 控制，并非在每个 Ubuntu 系统上都一定会出现。
