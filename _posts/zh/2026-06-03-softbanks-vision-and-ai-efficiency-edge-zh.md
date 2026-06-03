---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 软银的愿景与AI效率优势
translated: true
type: note
---

**问题：** 软银（孙正义）为何在2016年收购ARM，以及为何ARM在AI时代变得至关重要？

**答案：**

软银在2016年以320亿美元（243亿英镑）收购ARM，支付了约43%的公开市场溢价。孙正义预见到了ARM在万物互联未来中的潜力，并大力投资AI与自动驾驶。但2016年的赌注与2024-2025年的AI爆发是两个不同的故事。

## 2016年：移动互联网与物联网愿景

ARM不制造芯片，而是授权其设计与指令集，从每一颗使用其IP制造的芯片中抽取分成。收购时，ARM的处理器与图形技术已被三星、华为和苹果用于其自研微芯片。孙正义的愿景是：无处不在的计算——手机、物联网、自动驾驶。这是在底层架构中的战略布局。

## 2024-2025年：ARM为何在AI时代至关重要

**推理能效**：分析师预计，未来几年推理工作负载将占美国计算需求的75%以上。推理是AI“永远在线”的服务阶段，即使是微小的能效提升，也能在国家层面累积成巨大的能源节约。

ARM处理器及专用AI加速器进行推理时仅消耗100微瓦，而同等云端处理需要1瓦——这是10000倍的能效优势。这是RISC（精简指令集计算机）的物理原理：指令集最小化，单次操作功耗更低。

**边缘AI爆发**：AI正从云端走向现实环境。工业OEM厂商正寻求灵活、可扩展、内置AI加速的即用型算力，以支持对延迟敏感环境中的实时决策。边缘AI具有超低延迟（5-10毫秒，而云端为100-500毫秒），这对手机、可穿戴设备、工业自动化中的设备端推理至关重要。

## 软银的全栈布局

孙正义并未止步于ARM。软银先后收购了Ampere（服务器CPU）和Graphcore（用于AI训练的知识处理单元），打造了一个受软银控制的“闭环生态系统”：ARM提供核心架构，Ampere提供服务器CPU，Graphcore提供专用AI加速器。这是一套从边缘设备（通过ARM）到云端处理器（通过Ampere）的端到端解决方案。

## 数学逻辑

ARM在推理效率上的主导地位源于其ISA设计——更简单的指令（RISC）意味着更少的晶体管，单周期功耗更低。当推理占据AI工作负载的75%以上，且能源成本成为制约因素时，ARM的优势就变得生死攸关。2016年是远见，2024年则是验证。

**参考资料：**

- [软银股价24年后创历史新高，受ARM与AI提振](https://www.cnbc.com/2024/07/04/softbank-shares-hit-record-high-after-24-years-on-arm-and-ai-boost.html)
- [收购Ampere，软银加强对AI数据中心的掌控](https://www.datacenterfrontier.com/design/article/55277106/with-ampere-deal-softbank-tightens-its-grip-on-ai-data-centers)
- [高效AI与边缘计算如何助力美国竞争力](https://newsroom.arm.com/blog/how-efficient-ai-can-power-us-competitiveness)
- [AI暗战：SaaS与边缘计算架构之争](https://arxiv.org/pdf/2507.11545)
- [工业自动化中的边缘AI：OEM为何转向Arm](https://newsroom.arm.com/blog/the-architecture-shift-powering-next-gen-industrial-ai)
