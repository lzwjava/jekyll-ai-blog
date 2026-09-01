---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 旧台式机风扇噪音诊断
translated: true
type: note
---

以下是完整的**风扇源诊断**：

---

## 硬件摘要

| 项目 | 详情 |
|------|------|
| **CPU** | Intel Celeron E3400 @ 2.60GHz（双核） |
| **GPU** | Intel G41 集成显卡（`i915` 驱动）—— **无独立显卡** |
| **主板** | 联想，搭载 Intel 4 系列 / ICH7 芯片组 |
| **风扇传感器** | **未检测到** |
| **当前温度** | CPU 核心 0：**43°C**，核心 1：**37°C**，ACPI：**30°C** |

---

## 风扇检查结果

### 1. 无硬件风扇转速传感器
`/sys/class/hwmon/` 仅显示：
- `hwmon0` = `acpitz`（主板温度）
- `hwmon1` = `coretemp`（CPU 核心温度）

**不存在 `fan1_input`、`fan2_input` 或 `pwm*` 文件。** 系统无法向软件报告风扇 RPM。

### 2. 无 ACPI 风扇设备
```
/proc/acpi/fan → 不存在
/sys/bus/acpi/devices/*FAN* → 未找到
```

### 3. 无 GPU 热区
```
/sys/class/drm/card0/device/hwmon/ → 不存在
```
Intel 集成 GPU 未暴露 hwmon 接口。

### 4. 热管理策略
- 临界跳闸点：**110°C**
- 当前温度低于临界点 **约 70°C** —— CPU 基本处于空闲/冷却状态。
- 冷却设备（`Processor`）显示 `cur_state=0`（未节流）。

---

## 你看到的是哪个插件？

你的 XFCE 面板配置（`xfce4-panel.xml`）显示 **没有 GPU/传感器插件** 处于活动状态。正在运行的插件如下：

| 插件 | 用途 |
|------|------|
| applicationsmenu | 开始菜单 |
| tasklist | 窗口列表 |
| pager | 工作区切换器 |
| systray | 系统托盘 |
| clock | 时间 |
| actions | 关机等 |
| showdesktop | 最小化所有窗口 |
| launcher x4 | 应用快捷方式 |
| directorymenu | 文件管理器菜单 |

如果你在某处看到“GPU”或“显卡”图标，可能是：
- 一个**通用监控小部件**（例如 Conky、自定义脚本或之前安装的 GPU 工具的系统托盘图标）
- 虚拟机/模拟器软件的**状态图标**

---

## 为什么风扇声音大？

尽管温度读数约为 37–43°C，但这款较旧的联想台式机风扇很可能是由 **BIOS 控制**（而非操作系统控制），并且可能以固定或激进的风扇曲线运行。常见原因：

1. **灰尘 / 散热片堵塞** —— 老旧的 Intel G41/Celeron 系统容易积尘，导致 CPU 风扇高速旋转。
2. **导热膏干涸** —— 使用超过 10 年的机器；Celeron E3400 上的导热膏可能已退化，导致风扇更努力地工作。
3. **机箱风扇** —— 噪音可能来自便宜的含油轴承机箱风扇，而非 CPU 风扇。

---

## 建议

如果噪音困扰你：

```bash
# 检查是否有任何隐藏的 GPU 监控进程在运行
ps aux | grep -iE "nvidia|amd|gpu|temp|sensor|fan"
```

由于系统**没有独立 GPU 且没有风扇传感器**，显示数据的“GPU 显卡插件”要么是：
- **读取 Intel iGPU 统计数据**（该 GPU 无风扇/温度传感器），要么是
- **来自预期检测到 NVIDIA/AMD 显卡软件的残留产物**

**针对物理噪音：** 打开机箱，用压缩空气清洁 CPU 散热片/风扇。如果是联想 G41 时代的台式机，CPU 风扇很可能是小型 65W Intel 原装散热器，随着使用年限增加会变得嘈杂。

是否需要一条命令来检查是否有隐藏的后台进程在假装监控 GPU？