---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机械风扇与电风扇的嗡嗡声
translated: true
type: note
---

Question: 一位朋友建议检查风扇区域是否有东西碰到它。这为什么重要？

Answer:

## 因为“嗡嗡声”有两种完全不同的根本原因，而您只排除了其中一种

您的 GPU 更换测试排除了 GPU 特定的**电气**源（VRM inductor whine）。但这并不能排除**机械**源——风扇物理接触某物会产生一种声音，很容易误认为是 coil whine，尤其是如果您仅凭耳朵而不是隔离组件来判断。

您朋友的假设实际上是一个值得优先检查的好方法，因为它是最快的零成本测试，并且是“coil whine”的一个非常常见的误报原因：

### 机械接触声听起来像什么，以及为什么它会迷惑人

| 来源 | 机制 | 声音特征 |
| --- | --- | --- |
| Fan blade 刮擦到 cable tie / sleeved cable | 每次旋转时 blade tip 拨动线缆 | 与 fan RPM 同步的节奏性嗡嗡声 — 音调随 fan speed 变化 |
| Fan blade 打到 dust bunny | 间歇性接触 | 不规则的嗡嗡声/嘎嘎声，可能时有时无 |
| PSU/case fan hub 在 bearing 上松动 | Fan motor 振动撞击 fan frame 或 grille | 持续的低沉嗡嗡声，随 fan curve 变化 |
| Cable 从 shroud 外侧靠在旋转的 fan 上 | 同上，但外部 | 如果拨动线缆，嗡嗡声会出现/消失 |
| CPU cooler fan wire 布线离 blade 太近 | 同上 | 与 RPM 相关的滴答声/嗡嗡声 |

与真实 coil whine 的关键诊断区别：**机械嗡嗡声随 fan RPM 变化**（当风扇在负载下加速时，声音变大/变高，例如 GPU/CPU 温度升高使 fan curve 上升），而 **coil whine 随电气负载（功耗）变化**，而不是 fan speed。由于在实际 workload 中 fan speed 和 power draw 是相关的，人们经常将它们混淆——这正是您朋友的建议值得在执行 PSU teardown tests 前花费 30 秒的原因。

### 快速检查（在之前我给您的 PSU isolation test 之前执行此操作）

```bash
# 无需命令——物理检查：
# 1. 打开机箱侧面板
# 2. 目视检查每个风扇（机箱风扇、CPU 散热器风扇、PSU 风扇如果可见）
#    - 查找是否有任何 cable、cable tie 或 zip-tie 尾部进入 blade sweep radius
#    - 检查 CPU 散热器（尤其 AIO 散热器风扇——常见罪魁祸首，线缆通常正好经过 fan hub 旁边）
# 3. 关闭电源，手动旋转每个风扇——感受：
#    - bearing 中的 grinding vibration（风扇损坏，需要更换）
#    - Blade 在通过固定点时刮擦到任何东西
# 4. 打开电源，使用手电筒 + strobe effect（或手机的 slow-mo 摄像头）
#    实时观察每个风扇的 blade tips——任何 wobble 或 contact 都会立即在视频中显现，即使现场看起来太快无法察觉
```

如果没有任何东西接触，并且手动旋转风扇时没有 bearing grind，且转动顺畅，那就确认了您可以回到之前的电气隔离测试（PSU paperclip test / VRM under load）——您已经首先排除了廉价的解释，这是调试的正确顺序（最便宜、最快的测试优先，用您 CS 的直觉来说，这就是按成本进行二分搜索而不是按证据质量）。