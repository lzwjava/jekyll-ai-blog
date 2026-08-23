---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 170HX VBIOS 恢复可能
translated: true
type: note
---

问题：**基于 `nvflash --list` 的结果，这张 CMP 170HX 8GB 的 VBIOS 状态真的没问题吗？**

回答：

这个结果**比一张死卡好得多**。这张卡很可能可以恢复。

从截图中可以看到：

```
lspci | grep -i nvidia

03:00.0 VGA controller: NVIDIA GA102 [GeForce RTX 3080]
03:00.1 Audio device: NVIDIA GA102 HDMI Audio

04:00.0 3D controller: NVIDIA GA100 [CMP 170HX]
```

以及：

```
nvflash --list

<0> GeForce RTX 3080
<1> Graphics Device
    (10DE,20C2,10DE,1585)
```

关键点：

### 好的迹象 ✅

1. **PCIe 枚举正常**

系统识别到了：

```
10DE:20C2
```

这正是 CMP 170HX 的设备 ID。

GPU 核心、PCIe 接口以及基础固件初始化都处于活动状态。

2. **nvflash 可以识别到它**

这是最积极的信号。

如果 VBIOS 完全损坏，通常会出现：

```
nvflash --list
No NVIDIA display adapters found
```

或者只有 PCIe 出现但无法访问固件。

这里 nvflash 检测到了：

```
Graphics Device
```

意味着 SPI ROM 很可能可读。

---

### 为什么显示 "Graphics Device" 而不是 "CMP 170HX"？

这表明 VBIOS 不正确。

正常情况下你期望看到类似：

```
CMP 170HX
GA100
```

但现在显示的是通用名称：

```
Graphics Device
```

常见于以下情况之后：

* 刷写了错误的 GA100 BIOS
* 修改过的 BIOS
* 缺少板卡字符串

因此当前状态很可能是：

```
GPU 硬件          正常
HBM 内存          未知但很可能正常
PCIe              正常
VBIOS             错误
驱动初始化        失败
```

---

## 在支付 2500 元之前，请让卖家再执行一条命令

运行：

```bash
sudo ./nvflash -i 1 --save cmp170hx_backup.rom
```

如果成功：

```
Firmware image saved
```

那么恢复风险较低。

然后刷写正确的 8GB BIOS：

```bash
sudo ./nvflash -i 1 -6 correct_170hx_8gb.rom
```

---

## 看到这个之后，我的价格判断发生了变化

截图之前：

> 2500 元 = 风险太高

截图之后：

> 2500 元 = 或许可以接受，但仍需砍价

我的估价：

* nvflash 可读且可备份：**2000-2500 元**
* VBIOS 成功恢复后：**3000 元以上**
* 如果卖家拒绝备份测试：**≤1500 元**

这不是一张"死掉的矿卡"。它更像一个"固件修复项目"。

鉴于你已经在使用 CUDA/Linux，这实际上是一个合理的冒险。

下一个关键测试是：

```bash
sudo ./nvflash -i 1 --save backup.rom
```

如果这条命令能成功，我会相当有信心。
