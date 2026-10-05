---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决HDMI显示器唤醒问题
translated: true
type: note
---

问题：在 MSI Z170A GAMING M5 主板（Ubuntu）上，显示器通过主板 HDMI 接口连接，AOC 显示器在闲置约 30 分钟后保持黑屏，即使移动鼠标或按下按键也无法唤醒。如何修复？

回答：

主板和二手部件清单可能不是原因。这看起来像是软件或信号握手问题。屏幕变黑后，显示器丢失了 HDMI 信号并进入休眠状态。当 PC 尝试唤醒时，显示器和显卡驱动未能正确重新协商连接。某些 HDMI 显示器特别容易出现此问题（特定于某些显示器，且尤其影响通过 HDMI 连接的显示器）。

首先，确认 PC 是处于唤醒还是挂起状态。屏幕变暗后按 Num Lock 或 Caps Lock 键。如果键盘灯能切换，说明 PC 已唤醒，只是显示卡住了。如果灯无反应，则系统已挂起，唤醒问题是另一种情况。

按顺序尝试以下方法：

1. **重新插拔 HDMI 线缆一次。** 如果这样能恢复画面，则确认是握手问题（拔掉并重新插入 HDMI 显示器曾让一位出现相同症状的 Arch 用户恢复显示）。
2. **切换到文本控制台再切回。** 按 Ctrl+Alt+F3，再按 Ctrl+Alt+F2（旧版本按 F1）。这通常能强制显示器重新初始化。
3. **禁用自动挂起和屏幕空白以进行测试。** 在“设置” → “电源”中，关闭“自动挂起”并将“屏幕空白”设为“从不”。禁用完整挂起并仅测试屏幕空白是标准诊断步骤（如某一故障排除指南所建议）。如果问题消失，则说明已找到触发因素。
4. **关闭 X11 DPMS（仅限使用 Xorg 会话时）。** 运行 `xset -dpms s off`。若要持久生效，将其添加到启动应用程序中。
5. **检查当前使用的是 Wayland 还是 Xorg。** 运行 `echo $XDG_SESSION_TYPE`。如果输出为 `wayland`，请注销并在登录屏幕的齿轮图标中选择“Ubuntu on Xorg”后重新测试；如果你已在 Xorg 下，则反向操作。
6. **设置固定的 Xorg 配置。** 有用户通过手动创建 xorg.conf（使用当前配置）解决了 HDMI 显示器无法休眠或唤醒的问题，这阻止了 X11 在 DPMS 激活时自动重新配置显示器。
7. **检查显示器自身设置。** 在 AOC OSD 菜单中查找自动输入源设置、“DDC/CI”或“HDMI 模式 / 全范围”选项。尝试将输入源手动设置为 HDMI 而非自动。如果显示器有 DisplayPort 或 DVI 输入，换用其他线缆或接口是快速排除 HDMI 握手问题的方法。Z170A GAMING M5 主板具有 DVI 和 HDMI 输出，因此你可以测试 DVI 对 DVI（或 DVI 转 HDMI 适配器），无需额外硬件。
8. **换用不同的 HDMI 线缆。** 劣质线缆或二手主板上的不良接口可能导致间歇性握手问题。
9. **更新系统。** 运行 `sudo apt update && sudo apt full-upgrade`。Intel 显卡修复通常通过内核和 Mesa 更新推送。

由于主板是二手的，还需确认安装的 CPU 具有集成显卡（主板上的 HDMI 接口仅在使用带 Intel HD 显卡的 CPU 时才能工作，F 系列 CPU 不行），并且 BIOS 已更新到较新版本。

如果以上方法均无效，请提供你的 Ubuntu 版本、`echo $XDG_SESSION_TYPE` 的输出、CPU 型号以及 Num Lock 测试结果，我可以进一步缩小范围。

参考链接：
- [为什么我的显示器在 Ubuntu 上进入休眠后无法唤醒？](https://us.ktcplay.com/blogs/support-tips/ubuntu-monitor-wont-wake-up)
- [登录后显示器无法进入休眠（Ubuntu Budgie 24.04）](https://discourse.ubuntubudgie.org/t/monitor-wont-enter-sleep-when-logged-in-ubuntu-budgie-24-04/7257)
- [升级后显示器不亮，dpms 问题（Arch Linux 论坛）](https://bbs.archlinux.org/viewtopic.php?id=259462)