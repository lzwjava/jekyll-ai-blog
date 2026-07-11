---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 台式机嗡嗡声：电源线圈啸叫
translated: true
type: note
---

## 物理原理：所谓的“线圈啸叫”到底是什么

主板上每个开关元件——电源（PSU）、VRM电感、显卡电感——的工作原理，都是通过快速斩波直流电流通过电感（线圈），频率通常在20 kHz–1 MHz范围内，以调节电压（降压变换器拓扑）。线圈中的磁场会导致绕组以该开关频率物理振动（磁致伸缩 + 导线上的洛伦兹力）。如果该频率（或其谐波）落在可听范围（约20 Hz–20 kHz）内，且线圈上的灌封胶或清漆松动，你就会听到啸叫或嗡嗡声。这是机电现象，而非电气损坏——线圈啸叫本身不会损害系统。

你的测试——替换AMD↔Nvidia显卡无变化；完全移除显卡也无变化——实际上是一个干净的排除实验。它正确地排除了：

- 显卡VRM电感
- 显卡供电板

那么剩下三个开关稳压子系统，根据你的电源型号，可能性排序如下：

1. **电源（CX650F）**——内部变压器/电感（初级侧和次级侧）
2. **主板VRM**（CPU供电，CPU插座附近的电感）
3. **内存/扩展卡VRM**——可能性小得多，不太可能被听到

## 为什么我特别怀疑电源

我搜索了针对你确切型号CX650F的反馈报告，发现它有一个已知的类似投诉历史——用户报告CX650F发出“奇怪的噼啪声”，更广泛地说，CX系列因嗡嗡声/线圈啸叫问题而闻名，通常归因于较低成本的电容和电感元件。一个关于CX650F的帖子明确指出，啸叫通常来自电源、主板或显卡，并建议如为新设备则进行RMA。

这与CX650F的市场定位相符：它是80+ Bronze认证、非Seasonic平台的产品，处于Corsair产品线的低端。Corsair在CX系列上使用更便宜的OEM（通常是CWT），而非RM/RMx系列使用的Seasonic/Flextronics平台——更便宜的变压器和电感更不容易被正确浸渍/涂覆清漆，而这正是啸叫的根本原因（松散绕组 = 自由振动）。

## 如何完成隔离（在组装新机/决定RMA前执行）

```bash
# 你无法对电源运行命令，但这里是手动二分法步骤：

# 1. 将电源与主板完全隔离
#    - 单独用“回形针测试”启动电源（将24针上的绿色PS_ON线短接到黑色GND）
#    - 只连接一个旋转的机械硬盘或电阻性负载（旧显卡也可）作为负载
#    - 聆听：如果它在负载下继续啸叫，且没有连接任何主板，
#      则100%确认是电源问题。

# 2. 如果步骤1静音，重新连接主板但移除所有显卡
#    - 使用集显或无显卡启动到BIOS
#    - 给CPU施压：`stress-ng --cpu 24 --timeout 60s`（如果你有Live USB/Linux）
#      或只让它在BIOS空闲——VRM啸叫通常在CPU负载下出现，而非空闲
#    - 如果此时出现啸叫，则是主板VRM（B760M Mortar采用相对基础的
#      6+2+1相设计——在13900KF的高瞬态电流下有可能）

# 3. 使用纸箱隔离技巧交叉验证（论坛诊断中常用）：
#    - 将电源从机箱中物理取出，放在外面、架子上，无金属接触
#    - 这可以排除机箱共振/咔嗒声作为误判源
```

论坛报告汇聚到相同的方案上——逐个断开组件，并将电源从机箱中物理取出单独运行，这是人们确认电源发出嗡嗡声的标准方法，因为机箱面板和硬盘架可能共振，导致你误判声源。

## 对你的配件清单的评价

你的配置整体稳健——i9-13900KF + RTX 4070 + 64GB DDR5-6000 对于你的ML/开发工作负载来说非常均衡，水冷和机箱选择也都不错。根据你实际症状，我唯一要指出的组件是：

**Corsair CX650F（398元，80+ Bronze）**——鉴于它已经在你这个型号上被记录为啸叫问题源，而且你将要组装一台*新的* i9-13900KF 机器，我建议升级到 **Corsair RM650x / RM750e** 级别（Seasonic-adjacent平台，80+ Gold，贵约150-200元）或 **Super Flower Leadex / FSP Hydro Ti** 等效产品。在你当前预算下，差价相对13900KF的瞬态电流尖峰（全核睿频下P核瞬间可拉250W+）来说很小——一个廉价Bronze电源的开关电感正是这款CPU功耗曲线下受压最严重的部件，因此你很可能在旧机上复现出同样的啸叫声，只是更响亮。

考虑到你每月在GPU计算工作上超过12,000 token，且机器几乎连续运行进行训练，我会将“持续负载下静音”视为一个真正的规格要求，而非事后考虑——在8小时以上的训练运行中，嗡嗡作响的电源是一种低级别的摩擦，会逐渐侵蚀你数月间的专注力。

参考资料：

- [Corsair cx-650f psu coil whine and efficiency question - Tom's Hardware Forum](https://forums.tomshardware.com/threads/corsair-cx-650f-psu-coil-whine-and-efficiency-question.3794407/)
- [Corsair cx650m power supply making noise - Tom's Hardware Forum](https://forums.tomshardware.com/threads/corsair-cx650m-power-supply-making-noise.3339565/)
- [PSU making noise (CX650F) - Tom's Hardware Forum](https://forums.tomshardware.com/threads/psu-making-noise.3725276/)
- [Coil whine/buzzing from new Corsair PSU - Tom's Hardware Forum](https://forums.tomshardware.com/threads/coil-whine-buzzing-from-new-corsair-psu.3803602/)
