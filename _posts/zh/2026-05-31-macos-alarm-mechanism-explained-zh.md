---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacOS 警报机制详解
translated: true
type: note
---

说得好——你说得对，我之前的说法是错误的。

macOS 实际上正确处理了这个问题。当你在 Mac 上的时钟应用中设置闹钟时，它会注册到操作系统级别的通知系统，而不仅仅是应用进程。因此，当闹钟时间到达时，**即使时钟应用已经关闭，通知中心也会触发它**——这与日历提醒不需要打开日历应用就能触发的机制相同。

在底层，它使用的是 `UNUserNotificationCenter`（UserNotifications 框架），这是与进程无关的。操作系统守护进程 `UserNotificationCenter` 会保存计划并在任何应用状态下触发它。唯一需要注意的一点是：设备需要保持**唤醒状态**——如果合上盖子或 Mac 处于睡眠状态，闹钟将不会触发（这与 iPhone 不同，iPhone 有专门的闹钟协处理器路径，可以从深度睡眠中唤醒）。

因此，与 iOS 相比，实际的限制仅仅是：
- **Mac 处于睡眠状态** → 闹钟静默错过
- **Mac 唤醒但应用关闭** → 闹钟正常触发 ✓

感谢你直接测试——这才是正确的验证方式。我之前没经过核实就称它为玩具，是我错了。
