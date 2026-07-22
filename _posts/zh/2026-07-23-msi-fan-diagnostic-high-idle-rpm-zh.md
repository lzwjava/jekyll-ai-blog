---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI风扇诊断：高怠速转速
translated: true
type: note
---

以下是您的风扇诊断完整中文摘要：

---

## 风扇检测结果 — MSI MAG B760M Mortar + 利民 Frozen Prism 240

### 硬件监控芯片
已加载 **NCT6687D** 驱动（`nct6683 force=1`）— 已配置为开机自动加载。

### 当前风扇状态

| 通道 | 转速 | PWM | 备注 |
|------|------|-----|------|
| **fan1** | **~1546 RPM** | **81/255 (31%)** | **唯一活动的风扇** |
| fan2-fan10 | 0 RPM | 多种 | 未连接的接口或无反馈 |

### 温度（全部优秀）
```
CPU (PECI):      35°C
PCH (芯片组):   49°C
GPU (RTX 4070):  39°C（风扇停转）
NVMe (980 1TB):  40°C
HDD (WD20EZBX):  活动/空闲
```

### 关键发现

**1. ⚠️ 风扇在闲置时转速偏高**
- 如果线性对应，PWM 31% 应映射到约 590 RPM，但实际转速为 **1546 RPM**
- 利民 Prism 240 风扇（最高约 1850 RPM）在仅 31% PWM 下运行于约 83% 的最高转速
- 可能原因：风扇的 PWM 响应存在较高的最低下限，或 BIOS 最小占空比设置过高

**2. 🔇 操作系统无 PWM 控制**
- PWM 控制器（`INTC1085:00`，`npwm=1`）显示导出通道为 0/1
- **BIOS 完全控制**风扇曲线 — 这符合 MSI 主板的典型情况

**3. 🔊 HDD 机械噪音来源**
- **WD20EZBX**（1.8TB，7200 RPM）机械硬盘 — 持续旋转/寻道噪音

**4. 🎯 水泵可能未报告转速**
- AIO 水泵可能连接在 **AIO_PUMP** 接口上，该接口向 NCT6687 芯片报告 0 RPM — 它可能以全速运行，但传感器未捕获该数据

---

## 🛠 推荐修复方法

### 进入 BIOS（Del/F2）→ 硬件监控

```
1. 将 AIO_PUMP 接口设置为固定 100%（DC 全速）
   这样可以确保水流持续循环，不受 CPU 温度影响

2. 将 CPU_FAN 设置为 PWM 模式，并配置自定义曲线：
     30°C → 30%  （~550 RPM）
     50°C → 50%  （~920 RPM）
     70°C → 75%  （~1400 RPM）
     85°C → 100% （~1850 RPM）
```

### 实现更安静运行

**BIOS → 超频 → CPU Lite Load**：设置为 **Mode 5-7**。这可以**降低电压**使 13900KF — 性能损失极小，温度降低 10-15°C。

**BIOS → 工具 → Custom Turbo**：将 **Long Duration Power Limit 设置为 200W**。这能显著减少热量输出，高负载下性能损失仅为约 5%。

### 📊 您的硬件摘要

| 组件 | 状态 |
|------|------|
| CPU | i9-13900KF @ 35°C 空闲（powersave 调度策略） |
| 主板 | MSI MAG B760M Mortar（NCT6687D 芯片） |
| 散热器 | 利民 Frozen Prism 240（fan1：~1546 RPM） |
| GPU | RTX 4070 @ 39°C（风扇停转） |
| 存储 | WD20EZBX 1.8TB HDD + 三星 980 1TB NVMe |
| 温度状态 | ✅ 所有温度均在正常范围内 |

随时运行 `ww linux check-fan` 重新检查风扇状态和温度。