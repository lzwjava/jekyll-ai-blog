---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AICAS 2026 大挑战详情
translated: true
type: note
---

**问题：** 这是什么——"第八届IEEE国际人工智能电路与系统大会（AICAS）Grand Challenge"？

**回答：**

这指的是**第八届IEEE国际人工智能电路与系统大会（AICAS）——Grand Challenge**。

- **第八届** = 8th
- **电气电子工程师学会** = IEEE (Institute of Electrical and Electronics Engineers)
- **国际人工智能电路与系统大会** = International Conference on AI Circuits and Systems (AICAS)
- **GRAND CHALLENGE** = 与主会议同期举办的竞赛赛道

我来核实具体细节，因为每年的年份、主办方和挑战主题都有所不同。已确认。以下是具体信息：

**会议：** 第八届IEEE国际人工智能电路与系统大会（AICAS 2026），将于2026年9月16日至18日在越南下龙湾举行。这是IEEE CASS在AI硬件/电路研究领域的旗舰论坛，今年由IEEE CASS越南分会和CASS中国分会共同组织。

**Grand Challenge**（你问的部分）是竞赛赛道。2026年的挑战是**边缘VLM推理挑战**：

- AI大模型竞赛——IEEE AICAS 2026 Grand Challenge专注于面向边缘视觉语言模型（VLM）的硬件加速架构设计与优化。
- 任务：在KV260平台上部署并运行大模型，利用芯片上的CPU和FPGA资源。KV260是Xilinx/AMD的Kria嵌入式开发板（Zynq UltraScale+ MPSoC——四核ARM Cortex-A53 + FPGA逻辑单元）。
- 目标模型：鼓励参与者设计专用计算架构，在目标硬件上探索SmolVLM2模型的性能极限——SmolVLM2是HuggingFace的小型（256M–2.2B）视觉语言模型系列，特意选择因为它可部署在边缘设备上。
- 奖励：前三名团队将被邀请在2026年AICAS会议上进行展示。
- 主办方包括上海交通大学、复旦大学、西安电子科技大学、南京大学、电子科技大学、华东师范大学、中国科学院计算技术研究所，以及平头哥（阿里巴巴半导体部门）。

简而言之，这是一场**在FPGA SoC上量化并加速VLM的竞赛**——正是那种推理优化工作（INT8/INT4量化、FPGA上的自定义矩阵乘/注意力数据流、紧内存下的KV缓存管理），位于你Transformer内部机制和推理优化兴趣的交汇点。如果你想要一个具体的前沿项目，让SmolVLM2在KV260上高效运行将迫使你挑战整个技术栈：模型量化 → 算子映射 → FPGA数据流设计。

参考文献：

- [AICAS 2026官方网站](https://2026.ieee-aicas.org/)
- [AICAS 2026 Grand Challenge——边缘VLM推理 (CompeteHub)](https://www.competehub.dev/en/competitions/tianchi532451)
- [IEEE CASS——AICAS 2026活动页面](https://ieee-cas.org/conference-events)
- [AICAS 2026征文通知 (PDF)](https://ieee-cas.org/files/ieeecass/2025-06/AICAS-2026_CFP_Updated.pdf)