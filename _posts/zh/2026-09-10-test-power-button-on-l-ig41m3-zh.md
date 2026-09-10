---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试 L-IG41M3 上的电源按钮
translated: true
type: note
---

问题：您短接 **引脚 9 ↔ 引脚 11** 在您的 L-IG41M3 主板上，但机器没有断电。是主板故障吗？

回答：**不一定——但如果它能正常开机且同样的短接操作能可靠启动，那么 F_PANEL 输入多半是正常的。** 关键在于区分 **正常关机** 和 **强制断电**。

L-IG41M3 的电路图确认：

```text
pin 9  = PS / PWRBTN
pin 11 = GND
```

且电源按钮信号进入主板的 `PWRBTN_L` 逻辑。（[ManualMachine][1]）

### 按此方法测试

如果您当前在 Windows/Linux 下：

```text
短接引脚 9 ↔ 引脚 11
       ↓
操作系统收到电源按钮事件
       ↓
操作系统决定“电源按钮”的含义
```

它 **可能不会立即切断电源**。操作系统可配置为忽略该按钮、进入睡眠或执行正常关机。

相反，测试硬件的强制断电行为：

```text
开机
   ↓
短接 9 ↔ 11
   ↓
持续短接约 4–5 秒
   ↓
风扇应停止
```

实际上，有一个针对 **L-IG41M3** 的维修案例报告了完全相同的症状：

> 开机正常，但关机后风扇继续转动，且 4 秒短接无法关闭。

维修人员通过 `SLP3_L` → `IT8755E` → `ATX_PSON_L` 追踪了关机序列；最终发现一个 USB 电源控制器故障导致关机信号保持在错误状态。（[China2Japan][2]）

因此，如果 **短接 9↔11 持续 4–5 秒完全没有任何反应**，那么从主板维修角度看就值得关注了。

### 首先，排除各种可能性

进行这个简单实验：

```text
1. 启动主板。
2. 短暂短接 9 ↔ 11。
   → Windows/Linux 是否有反应？

3. 然后连续短接 9 ↔ 11 持续 5–10 秒。
   → 风扇/电源是否真的停止？
```

结果解读：

| 结果                                     | 可能情况                                      |
| ---------------------------------------- | --------------------------------------------- |
| 短按使操作系统关机                       | F_PANEL + PWRBTN 逻辑正常                     |
| 短按无反应，长按有效                     | 操作系统/按钮行为/配置问题                     |
| 短按有效，长按无效                       | **可能存在主板电源时序问题**                    |
| 甚至用 9↔11 启动都不稳定                 | 检查 F_PANEL / PWRBTN 输入                     |

**还有一个重要点：** 不要反复长时间短接这些引脚。正常测试是短暂接触；约 4 秒的测试仅用于复现主板的紧急电源按钮行为。

如果您能上传一张 **实际 L-IG41M3 的 F_PANEL 区域在主板通电时的照片**，我可以检查物理方向，确保您确实短接了 **9 和 11**，而不是依赖引脚编号。

参考资料：

* [ECS L-IG41M3 Rev. 1.1 电路图](https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com)
* [L-IG41M3 维修案例：关机后无法断电](https://www.china2japan.com/bbs_forum/weixiujingyan/2021/0828/1178171.html?utm_source=chatgpt.com)

[1]: https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com "ECS L-IG41M3 Schematics REV 1.1 - ManualMachine.com"
[2]: https://www.china2japan.com/bbs_forum/weixiujingyan/2021/0828/1178171.html?utm_source=chatgpt.com "日本维修经验酷派_ 按时序修好联想L-IG41M3谁有影驰660黑将的BIOS 麻烦"