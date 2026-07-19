---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI双GPU安装指南
translated: true
type: note
---

**问题：如何在一块微星主板上安装两块 RTX 4070 或 RTX 3090 显卡？mATX 是否太小？哪些微星主板适合？**

回答：

是的，**大多数 mATX 主板都不适合安装两块大型显卡**，尤其是 RTX 3090。问题不仅在于 PCIe 插槽，还涉及**物理间距、风道、供电和 PCIe 通道布局**。

对于 AI 工作负载（PyTorch、vLLM、训练），你需要：

* 两个全长 PCIe x16 物理插槽
* 至少 **3 插槽的显卡间距**
* 良好的 VRM/供电能力
* ATX/E-ATX 机箱
* 足够的电源容量

---

## 1. 为什么 mATX 有问题

典型的微星 mATX 主板：

```
CPU
 |
PCIe x16  ---- RTX 3090（占用3个插槽）
 |
PCIe x1
 |
PCIe x16 ---- 第二块显卡
```

一块 RTX 3090 通常占用：

```
插槽1：GPU
插槽2：散热器
插槽3：散热器厚度
```

安装第一块显卡后：

```
[ RTX 3090 ]
[ RTX 3090 散热器 ]
[ 被遮挡的 PCIe 插槽 ]
```

第二块显卡会面临：

* 几乎没有风道
* 温度升高 15~30°C
* 可能触发温度降频

对于 RTX 4070 来说会好一些，因为大多数是双插槽卡，但仍然很紧凑。

---

## 2. 我考虑推荐的微星主板

### 选项 A：MSI MAG B760 Tomahawk WiFi（ATX）

MSI MAG B760 Tomahawk WiFi

不错的平衡选择：

* ATX 尺寸
* 2 个 PCIe x16 物理插槽
* DDR5
* 支持第13/14代 Intel CPU
* 良好的 VRM

布局：

```
CPU

PCIe x16
   |
   |  RTX 3090

3 插槽间距

PCIe x16
   |
   |  RTX 3090
```

这大概是我会考虑的最低配置。

---

### 选项 B：MSI PRO Z790-A MAX WiFi

更适合 AI 构建：

* 更多的 PCIe 灵活性
* 更强的 VRM
* 更好的内存支持

搭配推荐：

* i7-13700K
* i7-14700K
* i9-13900K

---

### 选项 C：MSI MAG Z790 Tomahawk MAX WiFi

更高端的选择。

优势：

* 更强的供电设计
* 更多扩展能力
* 长时间运行双显卡时更稳定

---

## 3. 真正的限制：PCIe 通道

重要说明：

大多数消费级 Intel CPU：

```
CPU PCIe 通道：

16 通道给显卡
4 通道给 NVMe
```

两块显卡时变为：

```
显卡1：x8
显卡2：x8
```

示例：

```
RTX 3090 #1
PCIe 4.0 x8

RTX 3090 #2
PCIe 4.0 x8
```

对于 LLM 推理/训练：

通常可以接受。

会损失一些带宽，但显存大小重要得多。

---

## 4. 电源

两块 RTX 3090：

显卡：

```
3090 约 350W 每块
```

两块：

```
700W
```

CPU：

```
150-250W
```

系统：

```
100W
```

实际需求：

```
最低 1000W
推荐 1200W
```

不错的选择：

* Corsair HX1200
* Seasonic PRIME 1300W
* MSI MPG A1000G/A1250G

---

## 5. 机箱比主板更重要

对于双 3090：

避免普通游戏机箱。

你需要：

* 8 插槽显卡支持
* 420mm 显卡长度空间
* 前面板网状进风

示例：

Fractal Design Define 7 XL

Lian Li O11D XL

服务器机箱更好。

---

## 6. 针对你的 AI 使用场景

考虑到你在考虑：

* 本地 LLM
* Qwen/DeepSeek 风格的模型
* 微调
* vLLM

我的排序如下：

### 最佳性价比

```
2 × RTX 3090 24GB
+
MSI B760 Tomahawk
+
128GB DDR5 内存
+
1200W 电源
```

总显存：

```
48GB
```

这是一个非常强大的本地 AI 设备。

---

### 更便宜的方案

```
2 × RTX 4070 12GB
```

显存：

```
总共 24GB
```

但针对 LLM：

```
48GB 的 3090 > 24GB 的 4070
```

因为显存容量占主导。

---

对于你现有的 **i9-13900KF + MSI B760M Mortar + RTX 4070**，第一步升级实际上是主板 + 机箱 + 电源。B760M Mortar 是一块不错的游戏主板，但并非为双显卡 AI 工作站设计。
