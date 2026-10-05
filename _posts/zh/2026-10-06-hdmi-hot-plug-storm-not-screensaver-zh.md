---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HDMI热插拔风暴不是屏幕保护程序
translated: true
type: note
---

## 诊断：这是 HDMI 热插拔（HPD）中断风暴，而非屏幕保护程序

你的显示器并非进入休眠——而是被反复检测为“断开/重新连接”，导致桌面环境每次重新配置显示输出，并黑屏约 1 秒。

内核日志中的关键证据（大约在我查看前 1 分钟）：

```
01:58:49 kernel: workqueue: i915_hotplug_work_func [i915] hogged CPU ... 4 times
01:59:10 kernel: workqueue: i915_hotplug_work_func [i915] hogged CPU ... 5 times
01:59:11 kernel: i915 0000:00:02.0: [drm] HPD interrupt storm detected
                  on connector HDMI-A-1: switching from hotplug detection to polling
01:58:43 gnome-shell: Failed to post KMS update: drmModeAtomicCommit: Invalid argument
```

- `i915_hotplug_work_func` 持续占用 CPU = GPU 被热插拔中断淹没。
- GNOME 报告的 `drmModeAtomicCommit: Invalid argument` 正是表现为 1 秒黑屏的失败模式设置。
- 随后内核放弃中断，回退到**轮询**——因此当前状态稳定（`connected` 持续 12 秒）。重启后问题会再次出现，直到根因被修复。

### 这不是电源/屏幕保护程序引起的黑屏

你的 GNOME 设置已经是“从不黑屏”：

```
org.gnome.desktop.session idle-delay = 0
org.gnome.settings-daemon.plugins.power idle-dim = false
sleep-inactive-ac-timeout = 0
/sys/class/drm/card1-HDMI-A-1/dpms = On
```

因此更改屏幕锁定/黑屏超时无济于事。

### 硬件

- GPU：Intel Skylake GT2 HD 530（`i915`），显示器：**Lenovo LI2364**，连接在 **HDMI-A-1** 上。

### 原因

HDMI **热插拔检测（HPD）** 线路存在电气抖动。GPU 将该噪声解读为快速拔插事件，重新枚举连接器，合成器重新进行模式设置 → 黑屏闪烁。HPD 抖动几乎总是**物理层面**的问题：劣质/廉价/过长的 HDMI 线缆、松动的连接器、转接器，或端口/显示器故障。

### 修复方法，按可能性优先排列

1. **重新插拔 / 更换 HDMI 线缆。** 尝试使用一根不同的、质量好的、较短的线缆。这能解决大多数 HPD 风暴。
2. **尝试 GPU 上的其他 HDMI 端口**（你有 `HDMI-A-2`、`HDMI-A-3`）以及显示器的另一个 HDMI 输入接口。避免使用 HDMI 转接器/切换器。
3. **如果显示器/GPU 支持，尝试 DisplayPort**——DisplayPort 的热插拔通常更稳定。
4. 在黑屏发生时实时确认：

   ```
   sudo dmesg -w | grep -iE "hpd|hotplug|i915"
   ```

   如果每次黑屏时看到大量输出，即可确认是 HPD 问题。

### 软件缓解措施（如果暂时无法更换线缆）

- 内核已切换到轮询模式，因此重启前可能保持平静。要阻止中断路径重新启用，可以禁用内核 DRM 轮询（完全关闭重新检测——对于固定桌面没问题，但之后热插拔显示器不会被识别）：

  ```
  echo 0 | sudo tee /sys/module/drm_kms_helper/parameters/poll
  ```

- 锁定显示模式，使失败的模式设置不那么具有破坏性——在 `/etc/default/grub` 的 `GRUB_CMDLINE_LINUX_DEFAULT` 中添加：

  ```
  video=HDMI-A-1:1920x1080@60e
  ```

  然后执行 `sudo update-grub` 并重启。
- 尝试从 GRUB 菜单启动另一个已安装的内核（`7.0.0-31-generic`）——i915 的 HPD 处理在不同内核版本间有变化，而 26.04 使用的是非常新的 `7.0.0-34`。

### 次要清理（非根因）

`~/.config/monitors.xml` 仍然描述了一个不存在的 `DVI-I-1` 1024x768 显示器——过时信息。无害，但如果你需要，我可以清除它。

需要我现在应用软件缓解措施（禁用 DRM 轮询 + 锁定 HDMI 模式）吗？这样在你更换线缆之前问题可以停止。
