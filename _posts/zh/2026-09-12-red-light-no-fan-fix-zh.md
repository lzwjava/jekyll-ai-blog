---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 红灯，无风扇修复
translated: true
type: note
---

**问题：** RTX 3060 GPU（ORFULL 品牌）——通电后红色 LED 闪烁但风扇不转。如何修复？

**回答：**

这里有两个独立的现象，它们指向不同的原因：

---

### 🔴 红灯闪烁

RTX 3060 上的红色 LED 闪烁通常表示**电源供电问题**——要么是 PCIe 电源线松动/故障，要么是 PSU 电压不稳定/不足。

**修复红灯的步骤：**

1. **重新插拔 PCIe 电源线** — 拔下并重新牢固连接 GPU 上的 8-pin（或 6+2 pin）电源接口。确保完全卡入到位。
2. **检查你的 PSU 功率** — 确认你的 PSU 满足 GPU 的功率要求，并留有至少 100W 的余量。RTX 3060 建议使用 **550W 以上的 PSU**。
3. **尝试不同的电源线** — 如果你的 PSU 有多条 8-pin 线，换一条试试。
4. **完全断电重启** — 完全切断电源几分钟以重置指示灯，但注意观察开机后是否再次出现。
5. **尝试不同的 PCIe 插槽** — 将 GPU 插到主板上的另一个 PCIe 插槽中测试。

---

### 🌀 风扇不转

这很可能是**正常现象**，而不是故障。

RTX 3060 采用 **Zero RPM Mode（零转速模式）** — 风扇被设计为在空闲状态下（低于约 55–60°C）不转动。这可以降低噪音并延长风扇寿命。一旦你运行大型游戏且温度升高，风扇就会启动。

**然而**，如果红灯亮起*并且*风扇在负载下也不转动，这可能意味着 GPU 根本没有获得正常供电来运行。

---

### 故障排查清单

| 问题 | 可能原因 | 解决方法 |
|---|---|---|
| 红灯闪烁 | PCIe 电源线松动/损坏或 PSU 功率不足 | 重新插拔线缆，检查 PSU 功率 |
| 风扇不转（空闲时） | 正常的 Zero RPM 模式 | 运行游戏，风扇应在约 60°C 时转动 |
| 风扇不转（负载下） | 供电故障 / GPU 损坏 | 重新插拔 GPU，在另一台系统中测试或送修（RMA） |

---

**参考资料：**
- [GPU 风扇不转？原因、解决方法及何时需要担心](https://gpubottleneckcalculator.com/blog/gpu-fans-not-spinning-causes-fixes/)
- [ASUS Strix 3060 红灯闪烁 – ROG 论坛](https://rog-forum.asus.com/t5/nvidia-graphics-cards/asus-strix-3060-oc-12gb-blinking-red-lights-about-pcie-power/td-p/900631)
- [GPU 红灯闪烁 – Tom's Hardware](https://forums.tomshardware.com/threads/gpu-has-blinking-red-light.3754724/)