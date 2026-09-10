---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达GPU内存测试指南
translated: true
type: note
---

问题：解释来自YouTube视频的Nvidia GPU内存测试指南。

答案：
这段来自**GPU Solutions**的Fraser的视频展示了一个自定义的、菜单驱动的USB可启动工具，旨在帮助技术人员使用**MODS**、**MATS**和**NVMT**诊断Nvidia GPU内存错误。

---

### 按VRAM类型划分的关键工作流指南

* **GDDR6 (RTX 20系列, RTX 3050–3070)**
* **设置：** 将显示器直接连接到独立GPU，并将BIOS Primary Display设置为`Auto`或`PEG`/`PCIe`。
* **主要诊断工具：** **MATS** [[12:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D736)]。
* **注意：** 对于标准GDDR6诊断，不需要MODS和NVMT。

* **GDDR6X & GDDR7 (RTX 3070 Ti–3090 Ti, RTX 40系列, RTX 50系列)**
* **设置：** 将显示器连接到CPU的集成显卡（**iGPU**），并将BIOS Primary Display设置为`IGFX` [[04:58](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D298)]。
* **主要诊断工具：** **MODS** [[07:23](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D443)]。
* **注意：** 如果具有GDDR6X或GDDR7的显卡输出了正常的显示图像，运行MODS将返回`100021`错误代码，表示没有内存错误 [[09:45](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D585)]。

---

### 解读诊断测试结果

1. **MODS Frame Buffer (FBPA) 报告：**
查看每个内存通道的十六进制值的最后一位：

* **以`0`结尾：** 无错误（健康） [[06:15](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D375)]
* **以`2`结尾：** Bank 0有故障 [[06:25](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D385)]
* **以`8`结尾：** Bank 1有故障 [[06:25](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D385)]
* **以`A`结尾：** Bank 0和Bank 1都有故障 [[06:35](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D395)]

2. **故障模式与维修路径：**

* **局部通道故障：** 指向物理GDDR芯片故障或焊点断裂 [[06:47](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D407)]。
* **多个通道的广泛错误：** 通常表明GPU核心内存控制器损坏，而不是多个独立的VRAM芯片同时损坏 [[13:02](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D782), [16:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D976)]。

3. **NVMT警告：**

* **NVMT**在功能正常的GPU上可能会报告误报错误，因此绝不应将其用作独立的诊断工具 [[10:43](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Djh5V2onzAV4%26t%3D643)]。

---

参考资料：

* [How to Test Nvidia GPU Memory Errors | MATS, MODS and GDDR6/GDDR6X Guide](http://www.youtube.com/watch?v=jh5V2onzAV4)
