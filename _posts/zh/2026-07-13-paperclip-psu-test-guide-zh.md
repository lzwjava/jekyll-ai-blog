---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 回形针电源测试指南
translated: true
type: note
---

问题：如何使用回形针方法测试我的长城（Great Wall）85W电源是否正常工作，以及 pin-4/pin-5 步骤是如何操作的？

回答：

你粘贴的引脚定义说明描述的是标准的 **ATX PS_ON# 跳线测试**——其原理是，在任何符合 ATX 规范的 24 针接口上，将绿色线（**PS_ON#**，内部上拉到 5V）与黑色线（**COM/地**）短接，即可让电源的控制 IC 认为“主板要求启动”，从而绕过实际主板。

**为什么 pin 4/5 有效（电气原理）：**

24 针接口有两排，每排 12 针。如果将接口的塑料卡扣朝上，从左到右数 *上排* 的针脚，PS_ON# 和相邻的地线分别位于第 4 和第 5 位。这与一些指南中按全部 24 针顺序计数（pin 16 → pin 17）所指的物理线路是相同的——所有 24 针线缆的引脚定义一致，即使导线没有颜色编码，从左侧卡扣朝上开始向右数 4 针即可找到。不同厂商只是计数方式不同（顺序 1-24 与按行编号）。你粘贴的说明和英文指南描述的是同一个两个针脚。

**操作步骤（简洁版）：**

```
1. 关闭电源，拔掉交流电源线。
2. 断开所有其他线缆，仅保留 24 针主插头（交流线保持断开）。
3. 将 24 针插头方向调整为：卡扣/锁扣朝上，针脚朝向自己。
4. 从上排从左到右数第 4 针和第 5 针。
5. 将回形针弯成 U 形（剥掉表面涂层），两端分别插入 pin 4 和 pin 5 使其短接。
6. 插回交流电源线，将电源开关拨到“I”（开启）。
7. 风扇转动 → 电源能够供电，其自保护/控制 IC 工作正常。
   风扇不转 → 电源损坏，或者处于无负载的零转速待机模式。
```

**针对你情况的重要提醒：** 真正的 ATX 24 针接口通常用于额定功率约 300W 及以上的电源（这是标准 ATX 主板的需求）。一个 85W 的“长城”（Great Wall）电源极大概率 **不是** 带有 24 针接口的标准桌面 ATX 电源——85W 属于以下范围：

- 柔性 ATX / 迷你 ITX 嵌入式电源（部分确实使用 24 针或 4/6/8 针子集）
- 特定设备（NAS、瘦客户机、POS 终端、工业主板）的电源砖/适配器

在进行回形针测试之前，请检查：

```bash
# 快速确认——铭牌上写的是 "24-pin ATX"、"Flex-ATX" 还是专有规格？
# 查找：电源外壳上的型号，然后搜索数据手册
```

如果你的电源确实有 24 针主接口，上述步骤直接适用——ATX 规范是固定的，与功率无关。如果是专有直流电源砖，则回形针方法完全不适用；这种情况下，实际测试应使用万用表测量输出引脚：

```
预期电压轨（如果采用标准 ATX 引脚定义）：
+3.3V（橙色）、+5V（红色）、+12V（黄色）、-12V（蓝色，旧规范）、
+5VSB（紫色，即使电源“关闭”也始终带电）、
PS_ON#（绿色，浮空约 5V，触发时降为 0V）、
COM（黑色，所有测量的地参考）

万用表测试：
- 黑色表笔 → 任意黑色/COM 引脚
- 红色表笔 → 待测电压轨
- 短接前：PS_ON# 应读数约 +5V，所有主电压轨约 0V
- 短接后（电源“开启”）：PS_ON# 应降为接近 0V，
  +5V/+12V/+3.3V 应在标称值 ±5% 以内，+5VSB 始终约 5V
```

如果你能告诉我长城电源上印制的确切型号（或提供照片），我可以确认它是 ATX 引脚兼容还是专有砖，并给出准确的引脚分配，而非通用说明。

参考资料：

- [PSU Test, All cords are black — Tom's Hardware Forum](https://forums.tomshardware.com/threads/psu-test-all-cords-are-black.2583369/)
- [Testing your Power Supply Unit (Paperclip Test) — NZXT Support](https://support.nzxt.com/hc/en-us/articles/1260802863490-Testing-your-Power-Supply-Unit-Paperclip-Test)
- [Is my power supply dead?: The Paperclip Test — Antec Support](https://bobteam.freshdesk.com/support/solutions/articles/1000015319-is-my-power-supply-dead-the-paperclip-test)
