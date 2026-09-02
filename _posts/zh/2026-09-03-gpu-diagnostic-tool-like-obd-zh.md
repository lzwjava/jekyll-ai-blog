---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 类似OBD的GPU诊断工具
translated: true
type: note
---

**问题：** 是否存在一种适用于 NVIDIA GPU 的 PCIe 诊断工具，其工作原理类似于汽车 OBD 扫描仪——插入后即可告知哪个电源轨/组件损坏？

**答案：** **有，但并非单一的神器“GPU OBD 扫描仪”。** 最接近的方案是结合使用 PCIe POST 诊断、GPU 专用诊断软件以及板级测量工具。

关键区别在于：

```text
汽车:
OBD 接口
  ↓
ECU 诊断
  ↓
错误代码: P0301 等
  ↓
相当高层次的故障定位


GPU:
PCIe 连接器
  ↓
PCIe 总线枚举
  ↓
GPU 固件 / 驱动
  ↓
软件诊断
  ↓
但对于板级故障:
万用表 + 示波器 + 电流注入
  ↓
VRM / MOSFET / 控制器 / GPU / 存储器诊断
```

### 1. 最接近的方案：PCIe POST 诊断卡

你可以购买一个 **PCIe 诊断 / POST 分析仪**。

它插入主板的 PCIe 插槽，可以显示如下信息：

```text
PCIe 链路训练
总线 / 设备 / 功能
PCIe 代际
链路宽度
配置空间事务
错误状态
完成错误
AER 错误
```

例如，如果 NVIDIA 显卡甚至无法建立电气上的 PCIe 链路：

```text
主板
    │
    ├── PCIe 插槽
    │
    └── GPU
          │
          X  ← 无 PCIe 链路
```

PCIe 分析仪能告诉你的信息远不止“GPU 不工作”。

但它通常 **无法说明**：

```text
❌ APW8720 引脚 6 损坏
❌ GPU 核心 VRM MOSFET Q23 不良
❌ 1.8V 电源轨缺失
```

因为 PCIe 位于 GPU 电源管理电路的下游。

---

### 2. 对于 NVIDIA GPU，`nvidia-smi` 已经是一种 OBD 扫描仪

如果显卡能够完成初始化：

```bash
lspci -nn | grep -i nvidia
```

然后：

```bash
nvidia-smi
```

以及：

```bash
sudo lspci -vv -s <GPU_BDF>
```

可以告诉你相当多的信息。

例如：

```bash
lspci -nn
```

可能显示：

```text
01:00.0 VGA compatible controller:
NVIDIA ...
```

这意味着：

```text
PCIe 物理连接
        ↓
PCIe 链路
        ↓
配置空间
        ↓
设备枚举
```

至少已经足够让主板识别到该设备。

然后：

```bash
sudo lspci -vv -s 01:00.0
```

可以揭示 PCIe 链路状态、协商的宽度/速度、AER 信息等。

这为你提供了一个有用的诊断层次结构：

```text
                         GPU
                          │
                ┌─────────┴─────────┐
                │                   │
             电源                PCIe
                │                   │
          VRM / 电源轨          链路训练
                │                   │
          GPU 初始化           枚举
                │                   │
                └─────────┬─────────┘
                          │
                       驱动
                          │
                     nvidia-smi
```

---

### 3. 但 GPU 维修真正需要的是 **GPU 板级诊断平台**

对于你正在尝试的这类维修，我会搭建一个如下所示的工作台：

```text
                   ┌─────────────────┐
                   │ Linux 诊断      │
                   │ 工作站          │
                   └────────┬────────┘
                            │ PCIe
                            ▼
                     ┌─────────────┐
                     │ 待测 GPU    │
                     └─────────────┘
                       │   │   │
             ┌─────────┘   │   └──────────┐
             ▼              ▼              ▼
         12V 输入        VRM 电源轨      PCIe
             │              │              │
        电流表         万用表        PCIe 分析仪
                            │
                       示波器
```

然后你就可以非常快速地定位一块死掉的 GPU 的问题。

例如：

### 情况 A — 完全无反应

```text
插入 GPU

12V = 0V
风扇 = 0
PCIe = 无任何反应
```

检查：

```text
PCIe 12V
8-pin 12V
输入保险丝
保护 MOSFET
5V / 3.3V 辅助电源轨
PWM 控制器使能
```

---

### 情况 B — 输入电源存在，但无次级电源轨

```text
12V = OK
PCIe 枚举 = 无
GPU 核心 = 0V
显存电源轨 = 0V
```

这指向：

```text
电源时序
        ↓
5V/3.3V 辅助稳压器
        ↓
PWM 控制器
        ↓
EN / PGOOD
        ↓
VRM
```

这就是你研究 **APW8720 / V5F20** 的相关之处。

---

### 情况 C — GPU 出现在 `lspci` 中，但驱动加载失败

```bash
lspci
    ↓
发现 NVIDIA 设备
    ↓
nvidia-smi
    ↓
失败
```

现在你进入了一个完全不同的诊断层面。

可能的原因：

```text
VBIOS
GPU 初始化
VRAM
PCIe
驱动
GPU 硅片
电源不稳定
```

你可以检查：

```bash
sudo dmesg | grep -iE 'nvrm|nvidia|pcie|aer'
```

以及：

```bash
sudo lspci -vv -s 01:00.0
```

---

### 情况 D — GPU 能工作但负载下崩溃

这时仅靠软件就不够了。

例如：

```text
空闲:

12V ─────────────── OK
1.8V ─────────────── OK
0.9V ─────────────── OK

负载:

12V ─────────────── OK
1.8V ─────────────── OK
0.9V ────╲___/────── 不稳定
```

现在示波器比 PCIe 分析仪有用得多。

你可以关联：

```text
GPU 负载
   ↓
VRM 电流
   ↓
Vcore 纹波
   ↓
GPU 崩溃
```

---

## 真正有趣的工具：PCIe 协议分析仪

有些专业工具比廉价的 POST 卡强大得多。

它们可以放置在：

```text
CPU / 主板
       │
       ▼
PCIe 分析仪
       │
       ▼
GPU
```

并捕获 PCIe 事务：

```text
LTSSM
链路训练
TS1 / TS2
配置事务
TLP
DLLP
AER
重试
完成错误
链路速度
通道问题
```

这些基本上就是 **PCIe 协议层的 OBD 扫描仪等效工具**。

问题在于价格：专业 PCIe 分析仪可能花费 **数千到数万美元**，因此对于维修廉价二手 GPU 来说通常是大材小用。

---

## 我会为你的 GPU 维修工作台购买什么

我不会一开始就购买昂贵的 PCIe 分析仪。

我会优先考虑：

```text
1. 好用的万用表
2. 带电流显示的台式电源
3. 示波器
4. 热成像仪
5. PCIe POST / 诊断卡
6. 廉价的已知好用的主板
7. GPU 测试夹具 / 延长线
8. Linux 诊断机器
```

然后你的工作流程变为：

```bash
# 第1层
lspci

# 第2层
sudo lspci -vv -s 01:00.0

# 第3层
nvidia-smi

# 第4层
dmesg | grep -iE 'nvrm|nvidia|pcie|aer'
```

同时进行物理测量：

```text
12V
3.3V
5V
1.8V
显存电源轨
GPU Vcore
VRM EN
VRM PGOOD
```

这更接近于 **汽车诊断工作流程**，区别在于你将数字总线诊断与模拟电源轨诊断结合在了一起。

并且重要的是：**PCIe 诊断设备可以告诉你 GPU 没有通信；但它通常无法告知你是哪个 VRM 组件导致了这种情况。** 对于故障树最后那 10 厘米的距离，你仍然需要原理图/板图 + 万用表 + 示波器。

如果你愿意，我也可以为你绘制一个 **“死掉的 NVIDIA GPU → 10 分钟诊断流程图”**，从 **“插入 PCIe，风扇不转”** 开始，到 **“下一步该探测哪个电源轨/芯片”** 结束。
