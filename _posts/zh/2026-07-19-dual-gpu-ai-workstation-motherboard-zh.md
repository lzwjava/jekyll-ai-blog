---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双GPU AI工作站主板
translated: true
type: note
---

问题：你有一台 i9-13900KF + RTX 4070 + DDR5 64GB 的配置，想再加一块 RTX 3060。该选哪款主板？

答案：

你的核心需求改变了主板的选购方向：

**你不再只是组装一台游戏电脑，而是在搭建一台小型 AI 工作站。**

关键因素是 **PCIe 插槽布局**，而非 CPU 兼容性。

你的 i9-13900KF 拥有：

* 来自 CPU 的 16 条 PCIe 5.0 通道
  * 通常用于第一块显卡：PCIe x16
* Z790 芯片组提供额外的 PCIe 通道
  * 第二块显卡通常连接芯片组：PCIe x4

对于 AI 工作负载（PyTorch、CUDA），第二块 RTX 3060 运行在 **PCIe 4.0 x4** 模式下通常是可以接受的。显卡的瓶颈主要在于显存和算力，而非 PCIe 带宽。

典型的布局：

```
CPU
 |
 +-- RTX 4070
 |      PCIe 5.0 x16
 |
Z790 芯片组
 |
 +-- RTX 3060
        PCIe 4.0 x4
```

第二块显卡并非用于 SLI/NVLink，其用途是：

* 增加显存
* 运行另一个模型
* 分离的 CUDA 进程
* 分布式训练实验

---

## 我的推荐：ATX 规格的 Z790 主板

不要购买 mATX 主板。

你的机箱虽然是“迷你”款，但若要安装双显卡，你需要足够的物理空间和良好风道。

优秀的选择：

### 1. MSI MAG Z790 Tomahawk WiFi DDR5（我的首选）

### [MSI MAG Z790 TOMAHAWK WIFI DDR5 ATX 主板](https://www.newegg.com/msi-mag-z790-tomahawk-wifi-atx-motherboard-intel-z790-lga-1700/p/N82E16813144567?item=N82E16813144567&negg_topt=22&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*209.99 美元*

原因：

* 轻松驾驭 i9-13900KF 的供电需求
* 4 个 DDR5 内存插槽
* 两个可用的 PCIe 显卡插槽
* 出色的 VRM 散热
* 多个 M.2 插槽
* 优秀的 BIOS

扩展接口：

```
PCIe 5.0 x16  -> RTX 4070

PCIe 4.0 x4   -> RTX 3060

PCIe 4.0 x4 M.2
PCIe 4.0 x4 M.2
...
```

MSI 将该主板列为 Z790/LGA1700，支持第 12/13/14 代英特尔 CPU，并采用强大的 VRM 设计。([MSI 美国官方商城][1])

---

### 2. ASUS TUF Gaming Z790-PLUS WIFI

### [ASUS TUF GAMING Z790-PLUS WIFI](https://www.bestbuy.com/product/asus-tuf-gaming-z790-plus-wifi-socket-lga-1700-intel-z790-atx-ddr5-wi-fi-6e-motherboard-black/JJGGL6ZF32/sku/11121666?fs=tic1l0&utm_medium=feed&utm_source=chatgpt.com)

*268.40 美元*

同样非常出色。

扩展接口：

```
PCIe 5.0 x16

PCIe 4.0 x16 插槽
   （电气规格为 x4）

PCIe 4.0 x4
```

华硕规格说明：

* 1× PCIe 5.0 x16
* 1× PCIe 4.0 x16（最大 x4）
* 1× PCIe 4.0 x4

这恰好是双显卡所需的配置。([华硕全球官网][2])

---

## 你的电源问题

你目前的电源：

```
海盗船 CX650F RGB 750W
```

功率处于临界状态。

功耗估算：

```
i9-13900KF
~250W 峰值

RTX 4070
~200W

RTX 3060
~170W

主板 + 硬盘 + 风扇
~80W
```

峰值功耗：

```
250 + 200 + 170 + 80
≈700W
```

750W 能用，但余量不多。

对于显卡持续满载运行数小时的 AI 工作负载：

我建议升级到：

```
850W 金牌电源
```

推荐型号：

* 海盗船 RM850x
* 海韵 Focus GX-850
* 微星 MPG A850G

---

## 机箱也是个问题

你的 RTX 4070 Gaming X Trio 体积巨大。

再加上 RTX 3060：

```
插槽 1：
RTX 4070
████████

插槽 2：
RTX 3060
████
```

可能出现的问题：

* 第二块显卡可能阻碍气流
* 温度升高
* 主板的间距设计很关键

更合适的机箱：

* ATX 中塔
* 7 个 PCIe 插槽
* 前面板网状通风

推荐型号：

* 联力 Lancool 系列
* 分形工艺 Define/Meshify
* 海盗船 4000D Airflow

---

## 再补充一点 AI 相关的要点

针对你的使用场景：

RTX 4070 + RTX 3060：

```
RTX 4070
12GB 显存

RTX 3060
12GB 显存

总计：
24GB 显存
```

但是：

**你不能简单地把它们自动组合成一块 24GB 的显卡来使用。**

举例：

Qwen 模型：

```
12GB 模型
```

可以运行。

但是：

```
20GB 模型
```

不能简单地通过：

```
4070 12GB + 3060 12GB
```

来运行，除非使用模型并行技术。

相关工具：

* PyTorch Distributed
* DeepSpeed ZeRO
* Accelerate

可以拆分模型，但显卡间的带宽相比 NVLink 慢很多。

---

我最终的装机建议：

```
CPU：
i9-13900KF

主板：
MSI MAG Z790 Tomahawk WiFi DDR5

显卡：
RTX 4070 12GB
+
RTX 3060 12GB

内存：
64GB DDR5 6000

电源：
850W 金牌

机箱：
ATX 风道机箱
```

这实际上是一台非常合理的“平民 AI 工作站”。它能提供：

* 20 个 CPU 核心 / 32 线程
* 64GB 内存
* 总计 24GB 的英伟达显存
* CUDA 兼容性
* 多显卡训练实验的能力

参考资料：

* ASUS TUF GAMING Z790-PLUS WIFI 规格 ([华硕全球官网][2])
* MSI MAG Z790 TOMAHAWK WIFI 规格 ([MSI 美国官方商城][1])

[1]: https://us-store.msi.com/Intel-Z790/MAG-Z790-TOMAHAWK-WIFI?limit=12&utm_source=chatgpt.com "MSI MAG Z790 TOMAHAWK WIFI DDR5 ATX 游戏主板 - MSI 美国官方商城"
[2]: https://www.asus.com/motherboards-components/motherboards/tuf-gaming/tuf-gaming-z790-plus-wifi/?utm_source=chatgpt.com "TUF GAMING Z790-PLUS WIFI｜主板｜华硕全球官网"