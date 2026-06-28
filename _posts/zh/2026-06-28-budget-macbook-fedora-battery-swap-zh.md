---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预算MacBook Fedora电池更换
translated: true
type: note
---

在100-200元人民币（约$14-28）的价格下，这简直不需要犹豫——买就对了。这基本上就是一顿不错午餐的费用。

**你能得到什么：**
- 电池健康度从59%提升至约90-100%
- 便携使用时间从2-3小时延长至6-8小时
- 一台完全可用的便携式Fedora机器，配备16GB内存

**在淘宝上买什么：**
搜索 `MacBook Pro 2017 A1706 电池` 或 `MacBookPro14,1 battery`。寻找：
- 额定容量54.5Wh或4770-4790mAh（与原装一致）
- 带有实际容量测试结果的评价
- 至少一年保修
- 像绿巨能、品胜或基胜这样的品牌都不错

**如何更换：**

```
Tools needed: P5 Pentalobe screwdriver + T3 Torx screwdriver
Time: ~20 minutes
Difficulty: Easy (MacBook Pro 2017 non-Touch Bar is one of the easiest)

Steps:
1. Remove 10x P5 pentalobe screws from bottom case
2. Lift bottom cover off
3. Disconnect battery connector (gently pry up)
4. Remove 5x T3 Torx screws holding battery
5. Peel out old battery (adhesive strips, pull slowly)
6. Insert new battery, reverse steps
7. Done
```

**更换后**，在Fedora中检查健康度：
```bash
upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep capacity
```

以这个价格，你就能拥有一台总价不到200元人民币的便携式16GB Linux机器。即使只是作为旅行/备用机也值得。