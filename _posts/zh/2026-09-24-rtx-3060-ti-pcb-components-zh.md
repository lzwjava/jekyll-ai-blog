---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 3060 Ti PCB元件
translated: true
type: note
---

问题：**识别这块 RTX 3060 Ti PCB 上可见的电子元件，并解释每个元件的作用。**

回答：

这是 RTX 3060 Ti 的 **GPU 面 PCB**，散热器已拆除。这张照片足以识别主要的电源/数据元件，但**不足以读取大多数单个 IC 的型号**。RTX 3060 Ti 的 PCB 在不同厂商之间差异很大，所以我不会假装能仅凭这张照片给出精确 BOM。

![Image](https://images.openai.com/static-rsc-4/-KSIMYV-4SIKZBhrkBdL45IIQwyb8m69w9KgH9DFQ7s5WdgZhHMpGMcOd66e-jPApAkrdBob-L1y--KLTNbY3Q9GhoebvfclfStgJmZr0sB4_FQ0jKK7jgKVZO6qKqVZv9jV7k2hctXheCiMDvk-D8ovPwR0pjZfiRlMK124Mo3s4kH24LM_kBoNKeHSf_V8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/J51y_WXS7Z_OINabA3E99uuC_mmzQu88tlvOn0kuoGSB5LyOA7iVWPdbWkH6jSczyUXwACxyxuK_PuTHRpLeWqalsmGsGeUq9EUtRsI7zuwO2_ZUQ24SmUdwxIz-nz5ru-CTvm7P2XKKHBeHoTPhgc7pjz1LsceTkJYEO7jghIm6_3hEojjGXDd9x23HUmZj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PyRkAFvug7nhvNxeJGCH2PT5HEWLoC1iaOxua90k02IN3djQrlRARWeq_ZvZSF5DH4EycLLolPfibeZ2-tyV0gfuOcAoK7TzuytAICAVargbGg-LTMj0Imir07do9IGiR3nlSJdL0OiELcuokHJzqcMnhXnh0cSixmekMvYkuoqxlLVA4RytR6VD62M1Gm4F?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3UMdKuEOtW6m0HkF-tp1j13YNS80iZbUAQQ_fO1RoyBeGZ-aRupotZtTk2P-y98nw13VDd1UYGncUmKcL7rs9TTIGiVNckxS6d9jyCbcaQGGVaad2DmyijTzeu6lRhigkalxuV3Dd2WxYBlG8lK1OpPa4ogb2OUl9P-fyE-tohGYjOZ7RAkxuyHtLGGdIoWT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IHKvG7KxqTiM3OuReb1CFmx4tlIWyEluds_-j1hKS17MlxVV3_HpR1OM1opwnPWXanyNVGLdxeIiqKq4f3DCTp4GvjTCUHXBoshx9M_g3WAZCqz736KnepkNRDg55WyV9bLVA1CcHwuQ_x8UVEgoSbFGbg1HLZgj9OeHRqRcPVZwRkQZvn5rKB6DERTqiE2q?purpose=fullsize)

### 1. GPU — GA104

右侧，带裸露硅裸片的大型绿色封装。

这是实际的 GPU：

* NVIDIA **GA104**
* RTX 3060 Ti 使用 GA104 系列
* 约 392 mm² 裸片
* 4,864 个 CUDA 核心
* PCIe 接口
* 显存控制器
* RT/Tensor 核心
* 显示引擎等。

中间的大块灰色材料是旧的**导热硅脂**。

NVIDIA 将 RTX 3060 Ti 定义为基于 GA104 的 Ampere GPU。([NVIDIA][1])

---

### 2. GDDR6 VRAM

左侧——矩形黑色/棕色封装。

在这一侧我可以看到大约**四个显存封装**。另外四个可能位于 GPU 的另一面 / 或在这张照片之外，具体取决于 PCB 设计。

普通 8 GB RTX 3060 Ti 使用：

```text
8 × 1 GB GDDR6
        │
        ├── 256-bit total bus
        └── 8 GB
```

许多 3060 Ti 显卡使用三星 `K4Z80325BC-HC14`，但有些卡使用美光/海力士，因此**我无法凭这张照片确定你的具体显存品牌**。多个 3060 Ti 拆解确认使用 8 颗 1 GB GDDR6 颗粒。([Overclocking.com][2])

---

# 3. GPU VRM

这是你照片中最有趣的部分。

**紧邻 GPU 左侧：**

```text
        GPU
         │
         │ ~0.8–1.1 V
         ▼
     VRM output
         │
   ┌─────┴─────┐
   │           │
 MOSFET      MOSFET
   │           │
 Inductor    Inductor
   │           │
   └─────┬─────┘
         │
       GPU
```

GPU 不能直接由 PCIe 的 12 V 供电。VRM 将大约 12 V 转换为**电压极低、电流极大的 GPU 核心供电**。

### 3.1 黑色矩形电感

**中左部竖向排列的大型黑色矩形方块。**

这些是**电源电感/扼流圈**。

它们是这张照片中最容易识别的元件之一。

每一相大致如下：

```text
12 V
 │
 ▼
MOSFET/DrMOS
 │
 ▼
INDUCTOR  ← black block
 │
 ▼
GPU Vcore
```

电感储存/释放磁能，并平滑来自 MOSFET 级的开关电流。

你的 PCB 看起来大约有 **6 个 GPU 侧供电相**，但仅凭这张照片我不会把这一点视为确定。

一个有记录的、采用类似物理布局的 RTX 3060 Ti PCB 具有 **6 个 GPU 供电相 + 2 个显存供电相**。([XFastest][3])

---

# 4. MOSFET / DrMOS 功率级

这些位于**电感周围/旁边**，大多是小型黑色功率封装。

它们的工作本质上是高频开关：

```text
12 V
 │
 ├──── High-side MOSFET
 │
 └──── Low-side MOSFET
          │
          ▼
       INDUCTOR
          │
          ▼
         GPU
```

在现代 GPU 上，这些通常是 **DrMOS / 集成式功率级**，也就是说：

```text
High-side MOSFET
Low-side MOSFET
Gate driver
Current sensing
       ↓
  one package
```

这就是为什么你不一定会看到每相有三个独立元件。

例如，一个有记录的 RTX 3060 Ti 设计在 GPU 供电相中使用 **Alpha & Omega AOZ5311NQI DrMOS** 器件。其他 3060 Ti 型号使用完全不同的 MOSFET。([XFastest][3])

**重要提示：** 我无法可靠读取你板上元件的印字，所以不要假设你的就是 AOZ5311NQI。

---

# 5. 蓝色圆柱形电容

你这里有非常明显的一组垂直排列的电容：

```text
○
○
○
○
○
○
○
```

这些是**电源电容**，根据其物理结构，很可能是固态/聚合物电容。

它们的作用是：

* 滤除输出纹波
* 提供瞬态电流
* 稳定 GPU Vcore
* 降低 GPU 负载快速变化引起的电压波动

概念上：

```text
VRM ──── L ─────── GPU
         │
         C
         │
        GND
```

这些电容与电感一起构成 VRM 的输出滤波器。

GPU 和 VRM 周围还有许多小型 MLCC 陶瓷电容，负责更高频率的滤波。

---

# 6. 小型 MLCC 陶瓷电容

GPU/VRM 周围分布着**数百个微小元件**。

这些小的米色/灰色矩形主要是：

* MLCC 电容
* 电阻
* 偶尔有铁氧体磁珠 / 电感

GPU 需要大量的本地去耦，因为其内部电流变化极快。

你可以把它们想象成微观尺度的本地电池：

```text
VRM ─────────────── GPU
                    │
                 ┌──┴──┐
                 │ MLCC │
                 └──┬──┘
                    GND
```

典型的 RTX PCB 原理图包含许多容值，例如：

```text
0.1 µF
0.22 µF
1 µF
4.7 µF
10 µF
22 µF
...
```

实际容值无法通过外观判断。

例如，一份公开的 RTX 3060 Ti 原理图/BOM 在 PCIe/GPU 电源轨附近标有 0.1 µF、4.7 µF、10 µF 等。([Scribd][4])

---

# 7. 显存 VRM

GDDR6 也不能直接由 12 V 供电。

显存有一个**独立的、较小的 VRM**。

典型架构：

```text
12 V
 │
 ▼
Memory PWM
 │
 ▼
MOSFETs
 │
 ▼
Inductor
 │
 ▼
GDDR6 VDD / VDDQ
```

一个有记录的 RTX 3060 Ti 设计使用：

* `uP1666Q` 显存 PWM
* 2 个显存供电相
* 集成 MOSFET
* 电感
* 聚合物电容

但同样，你的具体 PCB 可能不同。([XFastest][3])

---

# 8. PWM VRM 控制器

应该有一个或多个小型控制器 IC 来控制功率级。

典型的 3060 Ti 示例包括：

```text
GPU VRM:
uP9512R
     │
     ├── phase 1
     ├── phase 2
     ├── ...
     └── phase N

Memory VRM:
uP1666Q
     │
     ├── phase 1
     └── phase 2
```

这些芯片本身并不承载 GPU 的数百安培电流。

它们生成控制信号：

```text
PWM controller
      │
      │ PWM
      ▼
Gate driver / DrMOS
      │
      ▼
MOSFET switching
```

具体到 NVIDIA RTX 3060 Ti Founders Edition，一次拆解识别出 **uP9512R** 为 GPU VRM 控制器，并采用 **7 相 GPU VRM + 2 相显存 VRM**。([Overclocking.com][2])

你的 PCB 看起来是一块不同/定制的 PCB，因此供电相数和控制器可能不同。

---

# 9. 小型电阻

VRM/GPU 周围的微型矩形元件包含大量电阻。

它们承担以下功能：

```text
voltage feedback
current sensing
gate control
pull-up / pull-down
signal termination
power sequencing
```

VRM 控制器需要反馈：

```text
             ┌──────────────┐
             │ PWM controller│
             └──────┬───────┘
                    │
                  PWM
                    ▼
                 VRM
                    │
                    ▼
                   GPU
                    │
                    │ VFB
                    └──────────► controller
```

该反馈网络部分由微型电阻/电容组成。

---

# 10. 铁氧体磁珠 / 小型电感

SMD 元件中还有一些微型电感类元件。

它们通常用于隔离/滤波电源域：

```text
12V ── ferrite bead ──► sensitive circuit
```

例如：

```text
digital power
      │
      ├── ferrite ──► analog power
      │
      └── ferrite ──► PLL / clock / memory
```

它们看起来与微型电阻相似，因此**我无法从这张照片中区分出每一个这样的元件**。

---

# 11. BIOS / SPI Flash

GPU PCB 上必须有一颗小型非易失性 Flash 芯片，其中包含固件/VBIOS。

通常：

```text
SPI NOR Flash
   │
   ├── GPU BIOS
   ├── board configuration
   ├── power/clock parameters
   └── fan/display configuration
```

常见芯片有 Winbond / GigaDevice / MXIC 的 8 引脚 SPI NOR 器件。

它很可能就在 PCB 上，但**这里的分辨率/角度让我无法自信地指出它的确切封装**。

---

# 12. 时钟振荡器

还应该有一个或多个晶体/振荡器元件提供参考时钟。

概念上：

```text
25/27 MHz reference
       │
       ▼
     GPU PLL
       │
       ├── core clock
       ├── memory clock
       └── PCIe clock domains
```

同样，这张照片中无法读取具体振荡器型号。

---

# 13. PCIe 边缘连接器

**图片底部。**

长的金色触点连接器是：

```text
PCI Express x16
```

它承载：

* PCIe 差分 TX/RX 通道
* 参考时钟
* 3.3 V
* 辅助电源/信号
* 边带信号
* 地

GPU 通过该接口与 CPU/芯片组通信。

---

# 14. 外部 12 V 供电

你这块 PCB 在显卡某处有外部 GPU 电源输入，只是在这张裁剪图中看不清楚。

电气上：

```text
PSU
 │
 │ 12 V
 ▼
GPU connector
 │
 ├──────── GPU VRM
 │
 ├──────── VRAM VRM
 │
 └──────── auxiliary regulators
```

RTX 3060 Ti 的参考规格约为 **200 W 整板功耗**，NVIDIA 为参考设计指定了一个 8 针 PCIe 辅助供电接口。定制显卡可能不同。([NVIDIA][1])

---

# 15. 显示输出电路

在挡板一侧，你可以看到 **DisplayPort/HDMI 连接器区域**。

这些连接器本身在电气上并不特别有趣；它们背后是：

* 高速差分走线
* ESD 保护
* 共模滤波
* 端接/无源元件
* GPU 显示 PHY 连接

RTX 3060 Ti 支持 HDMI 和 DisplayPort 输出。([NVIDIA][1])

---

# 16. ESD 保护

外部连接器附近通常会有微型 ESD 保护阵列。

例如：

```text
GPU ───────────── HDMI connector
                  │
                  ▼
              ESD TVS
                  │
                 GND
```

它们的作用是吸收从外部连接器进入的静电放电，而不是让它到达 GPU。

这些是微型 IC 封装，在你这张照片中无法可靠区分。

---

# 17. 电源管理辅助稳压器

除了大型 GPU/显存 VRM 之外，PCB 还需要较小的电源轨，例如：

```text
12 V
 │
 ├── ~1 V      GPU core
 ├── ~1.35 V   GDDR6
 ├── 1.8 V
 ├── 3.3 V
 ├── 5 V
 └── other auxiliary rails
```

这些由小型降压转换器/LDO 生成。

例如，一些 RTX 3060 Ti PCB 使用 `GS9216` 转换器为辅助电源轨供电。([Russerver][5])

---

## 你照片的重要物理布局

```text
                    TOP
 ┌──────────────────────────────────────────────┐
 │                                              │
 │   GDDR6       GPU VRM                       │
 │  ┌─────┐      ┌─────────┐                   │
 │  │ VRAM│      │ caps    │                   │
 │  ├─────┤      │  ○ ○ ○  │                   │
 │  │ VRAM│      │         │                   │
 │  ├─────┤      │ MOSFETs │                   │
 │  │ VRAM│      │ ███████ │                   │
 │  ├─────┤      │         │                   │
 │  │ VRAM│      │ inductors│                  │
 │  └─────┘      └────┬────┘                   │
 │                    │                         │
 │                    │ VCORE                   │
 │                    ▼                         │
 │              ┌─────────────┐                 │
 │              │             │                 │
 │              │   GA104     │                 │
 │              │    GPU      │                 │
 │              │             │                 │
 │              └─────────────┘                 │
 │                                              │
 └──────────────────────────────────────────────┘
                    BOTTOM
```

### 我能从你的实际照片中高置信度识别出的内容

| 可见项目 | 识别结果 | 置信度 |
| --- | --- | --- |
| 大型绿色封装 | GA104 GPU 封装/裸片 | **高** |
| 大型黑色矩形排列 | VRM 电感/扼流圈 | **高** |
| 蓝色圆柱形元件 | 聚合物/固态电源电容 | **高** |
| 左侧矩形芯片 | GDDR6 显存 | **高** |
| 电感周围的黑色功率封装 | MOSFET/DrMOS 功率级 | **高** |
| 小型米色/黑色 SMD | 电阻/MLCC 等 | **高** |
| 金色边缘连接器 | PCIe x16 | **高** |
| VRM 周围的小型 IC | PWM/驱动/稳压电路 | **中** |
| 确切的 MOSFET 型号 | 例如 AOZ5311NQI/等 | **低** |
| 确切的 PWM 控制器 | uP9512R/等 | **低** |
| 确切的电容值 | µF/耐压 | **低** |
| 确切的电阻值 | Ω | **低** |
| BIOS Flash | SPI NOR | **中** |
| 时钟振荡器 | 参考时钟 | **中** |

### 关键点

这颗巨型 GPU 实际上**并不是这张照片中在电气上最有趣的部分**。关键的电源路径是：

```text
PSU 12 V
   │
   ▼
┌─────────────┐
│ PWM control │
└──────┬──────┘
       │ PWM
       ▼
┌─────────────┐
│ MOSFET/DrMOS│  ← switches hundreds of watts
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  INDUCTOR   │  ← black blocks
└──────┬──────┘
       │
       ├────── capacitors
       │
       ▼
    ~1 V VCORE
       │
       ▼
     GA104
```

对于**元件级维修**，下一张有用的照片是**整块 PCB 两面的正对高分辨率照片**，最好能看清元件印字。然后我就可以逐个元件进行分析，并给出类似这样的结果：

```text
Uxxx = PWM controller
Qxxx = MOSFET/DrMOS
Lxxx = xx µH inductor
Cxxx = xx µF / xx V
Rxxx = xx Ω
Uxxx = SPI BIOS
Uxxx = VRAM
...
```

这会比仅仅识别元件类别更接近真正的 **RTX 3060 Ti PCB BOM/原理图级识别**。([Scribd][4])

参考资料：

* [NVIDIA GeForce RTX 3060 系列规格](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/?utm_source=chatgpt.com)
* [RTX 3060 Ti Founders Edition PCB/VRM 分析](https://overclocking.com/test-nvidia-rtx-3060-ti-founders-edition/3/?utm_source=chatgpt.com)
* [RTX 3060 Ti PCB 与 6+2 相 VRM 分析](https://www.xfastest.com/thread-247420-1-30.html?utm_source=chatgpt.com)
* [RTX 3060 Ti PCB 原理图/BOM 参考](https://www.scribd.com/document/765910143/Asus-Rtx-3060ti-Cg190pi-1-00?utm_source=chatgpt.com)

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/?utm_source=chatgpt.com "GeForce RTX 3060 Family | NVIDIA"
[2]: https://overclocking.com/test-nvidia-rtx-3060-ti-founders-edition/3/?utm_source=chatgpt.com "Test : NVIDIA RTX 3060 Ti Founders Edition - Spécifications et PCB : sur 13 - Overclocking.com"
[3]: https://www.xfastest.com/thread-247420-1-30.html?utm_source=chatgpt.com "INNO3D GeForce RTX 3060 Ti iCHILL X3 開箱測試 / 三風扇六熱導管，優質散熱的好選擇-iCHILL,INNO3D,RTX 3060 Ti,NVIDIA -"
[4]: https://www.scribd.com/document/765910143/Asus-Rtx-3060ti-Cg190pi-1-00?utm_source=chatgpt.com "Asus RTX 3060ti Cg190pi 1.00 | PDF"
[5]: https://www.russerver.com/blog/videokarta-s-aliexpress.-razborka-i-obsluzhivanie.?utm_source=chatgpt.com "Видеокарта с AliExpress. Разборка и обслуживание."