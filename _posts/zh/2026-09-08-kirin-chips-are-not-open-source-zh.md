---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 麒麟芯片不是开源的
translated: true
type: note
---

**问题：** 华为的麒麟芯片是开源的吗？

**答案：** 不，华为麒麟芯片**不是开源的**。它们是完全专有的。以下是详细说明：

**所有权与知识产权**
所有麒麟品牌、知识产权和设计权完全归属于华为，通过其全资无晶圆厂半导体子公司海思半导体持有。

**架构授权（非开源）**
海思从ARM公司购买CPU设计授权，包括各种ARM Cortex核心和Mali图形核心。这意味着麒麟是基于授权（但封闭）的ARM架构构建的——而非开源的RISC-V或类似架构。

**内部定制核心（同样封闭）**
虽然华为仍授权ARM的基础设计，但其海思芯片设计部门在新芯片（如麒麟9000S）中对其进行了改进，打造了自己的定制处理器核心。这些定制核心同样是专有的，未公开披露。

**独立知识产权声明**
麒麟710A具有首个拥有独立知识产权的纯中国芯片的殊荣——但这里的"独立知识产权"是指中国拥有所有权，而非开源。

**简而言之：** 麒麟芯片是海思（华为）设计的闭源专有硅芯片。芯片设计、RTL原理图及固件均未公开发布。华为唯一与开源相关的活动是在*软件*层面（例如鸿蒙OS/OpenHarmony的部分内容），而非芯片硬件本身。

---

**参考资料：**
- [什么是海思麒麟？– 阿里巴巴电子](https://electronics.alibaba.com/question/hisilicon-kirin-explained-performance,-ai,-us-restrictions)
- [海思 – EPFL图搜索](https://graphsearch.epfl.ch/en/concept/39222054)
- [华为新款SoC搭载内部设计处理器核心 – Slashdot](https://mobile.slashdot.org/story/23/09/24/1835200/huaweis-new-soc-features-processor-cores-designed-in-house)
- [麒麟710A：首款拥有独立IP的纯中国芯片 – XDA](https://www.xda-developers.com/huawei-hisilicon-14-nm-kirin-710a-chip-manufactured-shanghai-based-simc/)