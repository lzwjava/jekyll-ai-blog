---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Skylake屏幕黑屏修复
translated: true
type: note
---

我深入研究了实际机器，而不是相信泛泛的问答，并发现了一些改变答案的内容。以下是实际情况以及我所做的操作。

## 系统实际配置

| 项目 | 值 |
|---|---|
| 主板 | MSI **Z170A GAMING M5 (MS-7977)** — 与你之前的MSI主板一致 |
| 操作系统/桌面环境 | Ubuntu 26.04, **GNOME Shell 50.1** |
| 会话类型 | **Wayland** (`XDG_SESSION_TYPE=wayland`) |
| CPU/GPU | i5-6600 → Intel **HD Graphics 530** (i915)，所以集显*确实*存在 |
| 第二GPU | NVIDIA **Tesla M40** (`prime-select on-demand`, `nvidia_drm.modeset=1`) — 仅作计算用，无显示输出 |
| 显示器 | AOC **2369**，连接在 `card1-HDMI-A-1`，分辨率 1920x1080@60 |
| 空闲设置 | `sleep-inactive-ac-timeout=0`（交流电下不休眠），`idle-delay=300`（**5分钟**后息屏），`idle-dim=true` |

你粘贴的那个答案中有两处重要的修正：

1. **你用的是Wayland，不是Xorg。** 所以步骤4 (`xset -dpms s off`) 和步骤6（手动创建的 `xorg.conf`）在这里**完全无效**——GNOME/mutter 在Wayland上管理DPMS，而不是X服务器。那些仅适用于Xorg。
2. **休眠不是你的问题。** 在交流电下，`sleep-inactive-ac-timeout` 原本就是 `0`。实际触发的是GNOME的**息屏**（`idle-delay=300`，即约5分钟，不是30分钟——你可能记错了，或者因为4.5分钟变暗让你感觉时间更长）。息屏后，mutter关闭了i915管道；你的HDMI显示器随之休眠，唤醒时i915↔AOC链路没有重新协商。内核甚至在你日志中提示了Skylake的基础弱点：
   ```
   i915 ... 减少压缩帧缓冲区大小。... 如果可能，请在BIOS中增加stolen memory大小。
   ```

## 我已经更改的内容（无需root，立即生效）

```bash
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.settings-daemon.plugins.power idle-dim false
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 0
```
已验证：`idle-delay=0`，`idle-dim=false`，两个休眠超时均为 `0`。这将阻止显示器进入会导致卡死的状态。这是一个临时解决方案，而非根本修复。

## 真正的修复（需要sudo——你当前没有免密码sudo权限）

**1. 禁用Skylake显示电源（DC）状态——真正的根本原因。** 这是已知的“Intel Skylake屏幕在DPMS关闭后无法唤醒”的bug：
```bash
sudo cp /etc/default/grub /etc/default/grub.bak
# 在GRUB_CMDLINE_LINUX_DEFAULT中追加（在引号内）：
#   i915.enable_dc=0 i915.enable_fbc=0
sudo sed -i 's/\\(GRUB_CMDLINE_LINUX_DEFAULT="[^"]*\\)"/\1 i915.enable_dc=0 i915.enable_fbc=0"/' /etc/default/grub
sudo update-grub
sudo reboot
```

**2. 修复BIOS DVMT/stolen memory（内核明确要求了这一点）。** 重启进入MSI BIOS → *Settings → Advanced → Integrated Graphics Configuration*：
- **DVMT Pre-Allocated: 64M**（或更高；默认32M太小）
- **DVMT Total Gfx Mem: MAX**
- **IGD Multi-Monitor: Enabled**
- 同时将BIOS更新到最新的 7977v1x 版本。

**3. AOC 2369 显示器OSD菜单**（物理显示器）：将 *Input Select → HDMI* 手动设置为HDMI，而不是自动；关闭任何 **Off Timer / Auto Power Off / Eco** 模式。自动信号源扫描是导致此HDMI握手丢失的常见触发因素。

**4. 排除HDMI本身的问题。** 主板也有DVI-D接口。尝试其他HDMI端口或DVI转HDMI适配器以及不同的线缆，以隔离二手端口可能存在的问题。

**5. 可选：测试NVIDIA共存问题。** Tesla M40没有显示输出，但 `prime-select on-demand` 仍处于激活状态，且 `nvidia_drm.modeset=1`。如果仅靠i915修复无法解决，可测试 `sudo prime-select intel`（然后重启），以确认NVIDIA DRM堆栈是否干扰了Wayland唤醒。

## 下次发生问题时如何确认诊断

- 在操作前，先查看 `cat /sys/class/drm/card1-HDMI-A-1/status` 和 `.../dpms`。如果 `status` 变为 `disconnected` 而线缆仍连接，则是链路丢失/握手问题（确认需要DC-state修复）。如果仍显示 `connected` 但 `dpms=Off`，则是mutter未能重新启用。
- Num Lock测试：如果Num Lock灯可以切换，说明PC已唤醒，仅显示器卡住；如果无法切换，说明系统已休眠。
- 在Wayland下有效的恢复方法：按 `Ctrl+Alt+F3` 再按 `Ctrl+Alt+F2`（VT切换强制进行modeset），或者拔插一次HDMI线。

总结：你粘贴的答案中关于X11的 `xset`/`xorg.conf` 建议不适用于你的Wayland会话，且休眠原本就是关闭的。触发原因是GNOME的5分钟息屏在Skylake iGPU上遇到了HDMI握手bug——我现在已经禁用了息屏，而 `i915.enable_dc=0` 加上BIOS DVMT修复是持久的解决方案。