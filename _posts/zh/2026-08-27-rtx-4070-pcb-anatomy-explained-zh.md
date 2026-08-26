---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 PCB结构解析
translated: true
type: note
---

**问题：** RTX 4070 显卡有何特别之处？其电路板/显卡上物理集成了哪些元件？

**回答：**

---

## 🧠 RTX 4070 的特别之处

RTX 4070 基于 NVIDIA 的 **Ada Lovelace** 架构（AD104 核心），采用 **台积电 4N 制程工艺**（实际相当于 ~5nm 级别）。主要亮点包括：

- **5888 个 CUDA 核心** — 执行绝大多数 GPU 运算的并行处理器
- **36 个 RT 核心**（光线追踪，每个 SM 单元对应一个）— 用于光照/阴影模拟的专用硬件
- **184 个 Tensor 核心** — 处理 AI/矩阵运算，驱动 DLSS 3 超分辨率技术
- **12GB GDDR6X 显存**，搭载 **192-bit 显存位宽**
- **200W TDP** — 在同性能级别中能效相对较高
- **PCIe 4.0 x16** 接口

---

## 🔩 显卡上实际集成的物理元件（PCB 组件）

### 🟢 主芯片 — GPU 核心
- 位于中央的大型方形芯片，表面覆盖金属散热顶盖
- 包含数十亿个晶体管（AD104 核心约为 358 亿个）
- 通过 **焊锡凸点（倒装芯片工艺）** 与 PCB 基板连接

### 🔵 显存 — 视频内存芯片
- 多个 **GDDR6X 显存芯片** 环绕在 GPU 核心周围（通常为 6 颗芯片组成 12GB）
- 由美光制造，速度极快 — 每引脚最高可达 21 Gbps
- 以环形/光环图案排列在 GPU 周围

### ⚡ VRM — 电压调节模块
- 一组元件，负责 **将 PCIe 接口/电源接口的 12V 电压转换为 GPU 所需的精确较低电压**（通常约为 0.8–1.1V）
- 由以下部分组成：
  - **MOSFET / DrMOS 芯片** — 开关晶体管（外观为成排的小型黑色芯片）
  - **电感（扼流圈）** — 用于平滑电流的粗线圈，外观为小型金属方块/圆柱
  - **电容（大容量电容）** — 圆柱形或扁平贴片电容，用于缓冲电力和滤波噪声
  - **PWM 控制器 IC** — 小型芯片，负责指示 VRM 以多快速度切换

### 🟡 电容（多种类型）

| 类型 | 位置 | 作用 |
|---|---|---|
| **大容量电解电容** | 靠近电源输入 | 储存大量电荷储备 |
| **MLCC（陶瓷贴片电容）** | PCB 上各处 | 高频噪声滤波 |
| **POSCAP / SP-CAP 电容** | 靠近 GPU/显存 | 去耦，降低电压纹波 |

### 🔌 电源接口
- RTX 4070 使用 **16-pin PCIe 5.0 接口**（或通过 2× 8-pin 转接）
- 直接向 VRM 区域供电

### 🖥️ 显示输出电路
- 输出端口附近设有 **DisplayPort 1.4a** 和 **HDMI 2.1** 控制器芯片
- 端口周围配有 ESD 保护二极管及信号滤波电容

### 🧩 PCIe 金手指接口
- 插入主板的金色边缘接口
- 同时承载数据（x16 PCIe 通道）与部分电力

### 🌡️ 温度传感器
- 分布于电路板各处的贴片元件；向 GPU 核心及风扇控制器报告温度

### 🎮 BIOS 芯片
- 存储显卡固件/BIOS 的小型闪存芯片（通常为 8 引脚 SOP 封装）

### 🔒 其他 IC 芯片
- **时钟发生器 / PLL** — 确保精确的时序信号
- **电源时序控制 IC** — 控制启动时各电压开启的顺序

---

## 整体工作流程

```
市电 → 电源 → 12V 供电轨
                      ↓
              PCIe 接口 + 插槽
                      ↓
              VRM（MOSFETs + 电感 + 电容）
                      ↓
         GPU 核心 ←→ GDDR6X 显存
                      ↓
           显示 IC 芯片 → 你的显示器
```

---

**参考来源：**
- [NVIDIA RTX 4070 规格 — NVIDIA 官方](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070/)
- [GPU PCB 结构解析 — 基于 NVIDIA A100 案例研究（AnandTech 风格）](https://images.nvidia.com/aem-dam/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf)
- [什么是 VRM？ — 硬件详解](https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html)
- [GDDR6X 显存 — 美光](https://www.micron.com/products/graphics-memory/gddr6x)