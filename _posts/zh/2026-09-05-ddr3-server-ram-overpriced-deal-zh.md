---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DDR3服务器内存高价交易
translated: true
type: note
---

## 问题：三星 2×8GB 2Rx4 PC3L 内存条，160 元值得买吗？

**回答：不推荐——160 元的话建议跳过。**

关键在于 **2Rx4 + PC3L**。这很可能是 **DDR3L ECC 注册式（RDIMM）服务器内存**，并非普通台式机 DDR3。

例如三星 M393B1K70DH0-YH9 的参数：

* **8GB**
* **DDR3L-1333**
* **PC3L-10600R**
* **ECC**
* **注册式 / RDIMM**
* **2Rx4**
* **1.35V**
* 240 针 DIMM（[Compuram][1]）

卖家说 **“我的主板不支持”**，其实这强烈暗示它是服务器 RDIMM。

### 主要的兼容性问题

**普通台式机 DDR3 主板通常无法使用 RDIMM。**

示例：

```text
DDR3 UDIMM   ← 普通台式机内存
DDR3 ECC UDIMM
DDR3 ECC RDIMM ← 这一种
DDR3 LRDIMM
```

`RDIMM` 在内存控制器与 DRAM 芯片之间有一个寄存器/缓冲器。主板/CPU 必须明确支持它。

### 两根 160 元

换算下来：

```text
160 元 / 16GB = 10 元/GB
```

对于老旧的 DDR3 服务器内存来说，这个价格偏贵。

目前市面上的 8GB 三星 DDR3 ECC RDIMM 根据速度和型号不同，**每根约 17–30 美元**，而二手或服务器拆机件价格可能更低。（[Newegg.com][2]）

### [三星 8GB DDR3L 1066 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-00492?item=9SIAMBVK924851&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*17.56 美元*

### [三星 8GB DDR3 1333 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-004B2?item=9SIAMBVK924872&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*17.56 美元*

### [三星 8GB DDR3L 1600 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-004A0?item=9SIAMBVK924860&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*19.51 美元*

**针对你的使用场景，我建议目标价约为每根 8GB 内存 30–50 元人民币**，除非这些是速度特别快或特别受欢迎的服务器模块。

如果你正在为老款联想或其他测试机器专门购买 DDR3，**请把内存标签照片发给我**，我可以解读出具体三星型号，并告诉你 160 元是否值得。

[1]: https://www.compuram.biz/memory_module/samsung/m393b1k70dh0-yh9.htm?utm_source=chatgpt.com "三星 - M393B1K70DH0-YH9 8GB 240针 DIMM DDR3L - 内存模块"
[2]: https://www.newegg.com/p/1X5-000A-001Z7?utm_source=chatgpt.com "三星 M393B1K70DH0-YH9Q9 DDR3 1333 8GB ECC REG 2RX4 - Newegg.com"