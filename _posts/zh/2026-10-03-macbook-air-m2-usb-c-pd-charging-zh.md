---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook Air M2 USB-C PD 充电
translated: true
type: note
---

问题：**MacBook Air M2 能用任何 USB-C 充电器吗？需要哪种充电器？**

答案：

可以。**MacBook Air M2 使用 USB-C Power Delivery（USB-C PD）**，所以许多 Type-C 充电器都能为其充电，不限于苹果原装充电器。

关键点：

* 接口：**USB-C**
* 充电协议：**USB Power Delivery（USB-C PD）**
* 电压：通常为 **20V**
* 功率：

  * MacBook Air M2 最高支持约 **67W 快充**（取决于配置和充电器）
  * 默认配备的充电器：

    * 30W USB-C 电源适配器（基础型号）
    * 35W 双 USB-C 紧凑型电源适配器（部分配置）
    * 可选 67W 适配器以实现快充

兼容的充电器：

* ✅ 苹果 USB-C 充电器
* ✅ Anker USB-C PD 充电器
* ✅ UGREEN USB-C PD 充电器
* ✅ Baseus USB-C PD 充电器
* ✅ 笔记本 USB-C PD 充电器（戴尔/联想/惠普等）

示例：

```
USB-C PD 充电器
        |
        | USB-C 线缆
        |
MacBook Air M2
```

充电器会自动协商功率：

```
充电器：“我能提供 5V/3A、9V/3A、15V/3A、20V/3.25A”
MacBook：“给我 20V”
→ 开始充电
```

几点注意事项：

* 普通手机 USB-C 充电器（5W–20W）也能用，但充电速度会很慢。
* 不带 PD 协议的 USB-C 充电器可能无法正常工作。
* 线缆也很重要：

  * 进行超过 60W 的充电时，请使用额定功率为 60W/100W 的优质 USB-C 线缆（通常标有 E-marker）。
  * 廉价 USB-C 线缆可能会限制功率。

对于 M2 Air 来说，一款 65W–67W 的 GaN USB-C PD 充电器通常是理想选择：体积小、速度快，还能给手机/平板充电。