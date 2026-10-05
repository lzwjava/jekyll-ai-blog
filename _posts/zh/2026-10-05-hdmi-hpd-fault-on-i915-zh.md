---
audio: false
generated: true
image: false
lang: zh
layout: post
title: i915上的HDMI热插拔检测故障
translated: true
type: note
---

## 诊断：这是 Intel i915 显示器的 HDMI 热插拔（HPD）故障，与 `ww` 和 GNOME 屏幕熄灭无关

### 你机器上的证据

你的显示器使用的是 **Intel HD 530**（i915），连接器为 **HDMI‑A‑1**：

```
/sys/class/drm/card1-HDMI-A-1/status: connected   (1920x1080)
```

内核日志恰好记录了 HPD 信号抖动的特征：

```
Oct 05 19:20:36 kernel: i915 0000:00:02.0: [drm] HPD interrupt storm detected
                        on connector HDMI-A-1: switching from hotplug detection to polling
Oct 05 19:39:12 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 4 times
Oct 05 19:39:35 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 5 times
Oct 05 19:40:20 kernel: workqueue: i915_hpd_poll_init_work [i915] hogged CPU ... 7 times
```

### 为什么会出现“关闭 1 秒 / 开启 30 秒 / 关闭 1 秒”的现象

HDMI 连接器的 **热插拔检测（HPD，第 19 针）** 信号在抖动。每次 HPD 信号撤销时，i915 认为显示器被拔掉了，于是执行完整的模式切换 → 屏幕变黑。当 HPD 信号恢复时，它重新检测并点亮屏幕。风暴严重到驱动放弃中断，改为 **轮询**，而轮询工作（`i915_hpd_poll_init_work`）反复重新检测连接器 —— 因此大约每 30 秒出现一次约 1 秒的黑屏。

我排除了软件方面的嫌疑：

- `gsettings`: `idle-delay = 0` → GNOME **从不** 熄灭屏幕或执行 DPMS 关闭。`ww linux screen-lock` 未涉及。
- 没有影响显示的 cron 作业、用户定时器或自定义监控进程。
- 在刚才 60 秒的实时监控中，`status` 保持 `connected`，也没有出现新的 HPD 消息 —— 所以故障是 **间歇性的**，与你所说的“时不时”相符。

### 根本原因（按可能性排序）

1. **HDMI 线材损坏或接触不良** —— HPD 引脚或地线接触不牢，或信号完整性太差。这是最常见的原因。
2. **HDMI 接口松动/脏污**（显示器或主板）—— 重新插拔，尝试另一个接口。
3. **链路中的 HDMI 切换器 / KVM / 转接器** —— 去掉它们，直接连接。
4. **显示器固件** 在省电或自动信号源切换时脉冲 HPD —— 在显示器 OSD 中禁用“自动选择 / 自动信号源”、HDMI-CEC 以及节能/省电功能。

### 解决方法

1. **更换 HDMI 线材** 为一条短且已知完好的线（先做这一步）。
2. 在显示器和 PC 上尝试 **不同的 HDMI 接口**，如果可能的话换一台显示器测试。
3. 绕过任何切换器 / KVM。
4. 在显示器 OSD 中关闭 **自动信号源 / HDMI-CEC / 深度睡眠**。
5. 实时监控确认问题已修复：

   ```bash
   watch -n1 cat /sys/class/drm/card1-HDMI-A-1/status
   journalctl -k -f | grep -iE 'HDMI-A-1|HPD|storm'
   ```

   如果出现 `disconnected` 闪烁或新的 `HPD interrupt storm` 行，说明线材/接口仍有问题。

### 如果暂时无法更换硬件，可用的软件临时方案

你可以强制连接器忽略 HPD 信号保持开启状态，这样可以阻止黑屏（代价是模式被固定）：

- 在内核启动参数中添加（`/etc/default/grub`，然后执行 `sudo update-grub && reboot`）：

  ```
  video=HDMI-A-1:1920x1080@60e
  ```

  末尾的 `e` 表示即使 HPD 信号丢失也强制启用连接器。仅当需要进一步调试时才添加 `drm.debug=0`。

这只是掩盖了症状 —— 真正的修复是更换线材/接口。

**总结：** 你的显示器的 HDMI 热插拔检测线在抖动，导致 Intel 驱动每次重新模式切换显示器（大约 1 秒黑屏）。首先更换 HDMI 线材，然后是接口；绝大多数情况下这都能解决问题。
