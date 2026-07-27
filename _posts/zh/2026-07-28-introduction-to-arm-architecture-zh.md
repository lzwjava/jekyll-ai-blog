---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ARM架构简介
translated: true
type: note
---

问题：**ARM芯片介绍**

答案：

![Image](https://images.openai.com/static-rsc-4/SsDBzUcrpB-r-tFFDXAjSofX7BYcHIqwMHb496t9G4bQxx00UhYsrCpAdAnoHV40DBChb7VeCvMiFQ49d2BGSTvHJkJgyGCQBbvGu66S3MAxrAgGVyDg5c7S0J0oUuE15HNpxQIAaTD25iIf5jpIhAzCD2moVsRtgwJ6zYECqaed8Zi3ThNpdDL5NpsK6k66?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eUKAa7NyIAPibP0WotiKojWabawtrEhaZ6KF_xVsBAkgImw42CiZ9MjgQcwRPgXfxCmoyGXovCR3KU7XVmkWiJQHCzrxmVlKPcS2ms3p9IT7hb6VeDyJ1WEfyCKLC146FcM6EV3A7sGK8BbRSasjwCP0ryqAzFhVPiHotglhtb71uhfEVNZ4TsYmKhxeYOYY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ofWM5OaOxUvn1tfzR3Ht3UtH46-m4Y3H9jCmS94KA6an-e2Cx9F5wnKu4Hi0SWrcP5C-txaH0D8_nEUiHsWPKVKU49-d3osN2DhtLGZ_XkZT1PpJbAGeHQUb0LsZICNtM8wTDv9F6MhEoYjJSL4ZRd253aOrbF_giQ6xOfz-gu6Zkr03aV77vSdMtWxqZhR6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3oUSUdPt-YRF9p8jEfgS6xHv342SJQUVrZnhyANH8FNKaYccicNzWJ7Wn7Ca6cThwIqnovJnVNP5Ha-A7QsY6P6ZtjnmNcSgPN025rBrcomi32yEv3s5yVvFh9j0x4lqtq_5aH_E7Yx15wmK0OP9sp9s5bulqHQ4cZGeSLDFN5QSBAqdIs23S4TnQ56r20A0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2fVoP5kepDzEnzWW0oR5xRbZbjERDXtYAzbhBK9O3IWsTgVGVTSLGpzmRYQUGF-LH5OIlKUBvy-jKB_LGPxuUZ0Pe7NuXX06RH-HpmQnHHxao-zguhUMokNfccQnVqI16L5Z5sxenRtMEsjV6c-1JAMC2fgKwGh9EhHVk-A6ZWvlepsgPC4JwXMYkYtrF1BP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qSbq-ki83Uhh5l3KA2ZuWRws-51n3GY4D4bz8pd_DKFTbQgNzKCnwgr281rz3GjUQL3QHCrFVMFln25QQn18pZd8MGkOovQht17rIBIYRS0t7Y-CVTVBnU-um7BRKWkl6KnLFU7CDrFXkohHgdFVSfWOcD1SebmsXJrxYFBJg9kDHDcW5m5zSfa5JVc2M6M2?purpose=fullsize)

ARM 是一种 **CPU 指令集架构 (ISA)**，最初由 Arm Holdings 创建。与 Intel x86 CPU（用于大多数 PC）不同，ARM CPU 围绕**低功耗和高效率**设计。

核心思想：

> ARM 授权 CPU 设计/架构。公司围绕它构建自己的芯片。

示例：

* Apple 基于 ARM 架构设计 M 系列芯片 (M1/M2/M3/M4)。
* Qualcomm 设计骁龙芯片。
* MediaTek 设计智能手机 SoC。
* Huawei 在麒麟芯片中使用基于 ARM 的设计。

---

## 1. ARM vs x86

传统 PC：

```
Intel Core / AMD Ryzen
        |
        v
      x86 ISA
        |
        v
    CPU 核心
```

ARM：

```
ARM ISA 授权
        |
        +----------------+
        |                |
      Apple           Qualcomm
        |                |
     M4 芯片      骁龙 X
```

ARM 本身不是芯片。它类似于 CPU 理解的“语言”。

示例：

x86 指令：

```
ADD RAX, RBX
```

ARM 指令：

```
ADD X0, X1, X2
```

不同的机器语言。

---

## 2. ARM 为何流行

### 能效

ARM 采用更简单的指令设计：

**RISC**
（精简指令集计算机）

特点：

* 更少的指令类型
* 更简单的 CPU 解码
* 更低的晶体管成本
* 更好的能效

典型对比：

| CPU           | 设备        | 功耗    |
| ------------- | ----------- | ------- |
| Intel Core i9 | 台式电脑    | 100-250W |
| Apple M4      | 笔记本/平板 | ~10-30W  |
| 骁龙          | 手机        | ~3-8W    |

---

## 3. ARM SoC 设计

现代 ARM 芯片通常是 **SoC（片上系统）**：

```
+--------------------------------+
| ARM SoC                        |
|                                |
|  CPU 核心                      |
|   - Cortex-X 大核              |
|   - Cortex-A 能效核心          |
|                                |
|  GPU                           |
|                                |
|  NPU / AI 加速器               |
|                                |
|  ISP 摄像头处理器              |
|                                |
|  内存控制器                    |
|                                |
|  调制解调器（有时）            |
+--------------------------------+
```

手机芯片本质上就是一台完整的计算机。

---

## 4. Apple Silicon 示例

Apple M4：

```
             M4 SoC

+--------------------------+
| CPU                      |
|  4 个能效核心            |
|  6 个性能核心            |
+--------------------------+
| GPU                      |
+--------------------------+
| 神经网络引擎             |
| （AI 加速）              |
+--------------------------+
| 统一内存                 |
+--------------------------+
```

重要的创新：

### 统一内存

传统 PC：

```
CPU 内存 <----> PCIe ----> GPU 显存
```

Apple：

```
        统一内存
             |
     +-------+-------+
     |               |
    CPU             GPU
```

更少的数据复制，更高的效率。

---

## 5. ARM 在 AI 计算中的应用

ARM 变得重要，因为 AI 工作负载需要高效。

示例：

### 边缘 AI

```
摄像头
 |
ARM 芯片
 |
神经网络引擎
 |
AI 推理
```

无需云端。

应用场景：

* 自动驾驶汽车
* 机器人
* 无人机
* 智能摄像头
* 手机

---

## 6. ARM 服务器市场

ARM 也在进入服务器领域。

示例：

* Amazon Web Services Graviton 处理器
* Ampere Altra CPU

服务器优势：

```
相同电力预算：

x86：
100 核心

ARM：
150+ 核心
```

云服务提供商喜欢 ARM，因为电力是主要成本。

---

## 7. ARM vs RISC-V

另一个重要架构：

```
ARM
 |
 |-- 专有 ISA
 |-- 需要授权

RISC-V
 |
 |-- 开放 ISA
 |-- 任何人都可实现
```

RISC-V 在中国和研究领域越来越流行，因为公司可以避免 ARM 授权。

---

## 8. 对于开发者

ARM 影响软件，因为二进制文件不同。

示例：

x86：

```
app-x86_64
```

ARM：

```
app-aarch64
```

Linux：

```bash
uname -m

# Intel PC
x86_64

# ARM 机器
aarch64
```

Docker：

```bash
docker build \
  --platform linux/arm64 .
```

现代工具支持多架构镜像：

```
myapp:latest

        |
        +-- linux/amd64
        |
        +-- linux/arm64
```

---

## 9. 未来趋势

计算格局正在转变：

```
2000-2020

Intel x86
   |
   +-- PC
   +-- 服务器


2020-2030

ARM
   |
   +-- 移动设备
   +-- 笔记本
   +-- 服务器
   +-- AI 边缘


2030+

ARM + RISC-V + 定制 AI 加速器
```

对于 AI 工程师来说，ARM 很重要，因为未来不仅仅是 GPU 集群。大量推理将在**高效的 ARM + NPU 设备**上运行。

参考资料：

* [Arm Architecture](https://www.arm.com/architecture?utm_source=chatgpt.com)
* [Apple M4 chip overview](https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/?utm_source=chatgpt.com)
* [AWS Graviton Processors](https://aws.amazon.com/ec2/graviton/?utm_source=chatgpt.com)
* [RISC-V International](https://riscv.org/?utm_source=chatgpt.com)