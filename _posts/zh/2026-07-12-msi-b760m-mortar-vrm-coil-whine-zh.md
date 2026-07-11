---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微星B760M迫击炮VRM电感啸叫
translated: true
type: note
---

问题：原来蜂鸣声实际上来自主板（MSI MAG B760M Mortar WiFi）——为什么会是来自这里？

答案：

## 这与你的排除顺序一致——也是最常见的结果

看看你实际测试的顺序：

1. **更换GPU（AMD ↔ Nvidia），完全移除GPU** → 无变化 → 排除GPU VRM
2. **检查风扇/机械接触** → （隐含已排除，因为你现在指向主板，而非风扇）
3. **剩余候选**：主板CPU VRM（或电源，但你已经将声音定位到板子上）

这正是我找到的论坛帖子中的排查过程——有人明确以与你相同的方式缩小范围：更换GPU，无变化，然后将声音强度定位到CPU插座区域正上方，得出结论是主板的VRM。

## 为什么B760M Mortar特别有可能是候选

MAG B760M Mortar WiFi是一款预算级mATX主板（1299 CNY），VRM设计较为普通——这类主板通常为CPU Vcore配备6-8相配置，使用比高端Z790主板更小/更便宜的电感。搭配**i9-13900KF**（24核8P+16E芯片，全核睿频时瞬态功耗可达250-300W+），等于是在让一款预算级VRM快速切换大电流——这正是会在电感绕组中引发可闻振动的条件（与我之前解释的电源线圈啸叫相同的磁致伸缩机制，只不过这次发生在CPU插座旁边的CPU功率级电感中）。

值得注意的是，MSI论坛上甚至有一个几乎相同的主板（B650M Mortar，AM5的对应型号）出现在与线圈啸叫相关的故障排查中——MSI这一"Mortar"级别的主板在AM5和LGA1700两个平台上似乎都容易收到这类报告，很可能是因为这是该系列中的同一VRM成本档次，而非你的主板特有的问题。

## 这是否是问题，以及如何处理

**是否危险？** 不——我找到的所有来源（Tom's Hardware、Overclock.net、MSI论坛）都一致认为：VRM线圈啸叫不会损坏主板或缩短寿命。这纯粹是声音问题。

**能否减少？按以下顺序尝试，从最便宜/最安全开始：**

```
1. BIOS：禁用CPU C状态（C1E、C3、C6、Package C-States）或设置为"Enabled"，
   具体取决于当前触发的状态——C状态切换会导致VRM占空比快速变化，
   这是非常常见的啸叫触发原因。两种设置都试一下。

2. BIOS：将Loadline Calibration（LLC）上调或下调一档——
   这会改变瞬态负载下的VRM开关行为，在默认设置下不会对稳定性产生实质性影响。

3. BIOS：如果有显示，查找"VRM Switching Frequency"（VRM开关频率）——
   MSI有时在超频设置下会暴露此选项。微调它会使基础啸叫频率偏移，
   有时会超出可听范围或你的耳朵敏感范围。

4. 物理测试（来自Tom's Hardware帖子）：开机后，用铅笔橡皮头轻轻按压
   CPU插座附近的大型黑色VRM电感（通过VRM散热器的气流间隙，如果有的话，
   或者拆下散热器后操作）。如果按压时啸叫的音调/音量发生变化，
   你就已确认是某个特定电感的机械振动——重新安装VRM散热器下的导热垫有时可以抑制它。

5. 降压/降频测试：如果你对64GB内存套件应用了任何XMP/EXPO或全核超频，
   暂时重置为完全默认的JEDEC + 无超频。如果啸叫消失，
   则说明它与负载相关，且与你的特定电压/频率工作点绑定——
   然后你可以寻找一个不会激发谐振的稳定点。
```

**如果以上方法都无效且声音确实很大**（不仅是在耳朵靠近机箱时能听到，而是在正常坐姿距离下也能听到），这就从"正常VRM啸叫"跨入了"可能为制造缺陷"的范围——值得在退换货窗口关闭前向MSI/京东提交RMA申请，尤其是你尚未完成最终装机，而在这个阶段更换主板既便宜又方便。

考虑到你即将用这台机器进行持续的AI训练工作负载（持续的CPU/GPU高占用率，而非突发性的游戏负载），现在追查在全核持续负载下出现的啸叫，比在未来2-3年内忍受它要值得。

参考资料：

- [主板线圈啸叫？有没有办法限制？- Tom's Hardware论坛](https://forums.tomshardware.com/threads/motherboard-coil-whine-is-there-any-way-to-limit-it.3685126/)
- [无法确定线圈啸叫的来源 - Tom's Hardware论坛](https://forums.tomshardware.com/threads/cannot-pinpoint-the-source-of-the-coil-whine.3784809/)
- [请帮我诊断我的AM5不稳定问题！- Overclock.net](https://www.overclock.net/threads/please-help-me-diagnose-my-am5-instability.1802538/)