---
audio: false
generated: true
image: false
lang: en
layout: post
title: AICAS 2026 Grand Challenge Details
translated: false
type: note
---

**Question:** What is this — the "8th IEEE International Conference on Artificial Intelligence Circuits and Systems (AICAS) Grand Challenge"?

**Answer:**

This decodes to the **8th IEEE International Conference on Artificial Intelligence Circuits and Systems (AICAS) — Grand Challenge**.

- **第八届** = 8th
- **电气电子工程师学会** = IEEE (Institute of Electrical and Electronics Engineers)
- **国际人工智能电路与系统大会** = International Conference on AI Circuits and Systems (AICAS)
- **GRAND CHALLENGE** = a competition track run alongside the main conference

Let me verify the specifics, since the year/host/challenge theme changes each edition.Confirmed. Here's the concrete picture:

**The conference:** The 8th IEEE International Conference on Artificial Intelligence Circuits and Systems (AICAS 2026), taking place 16–18 September 2026 in Ha Long Bay, Vietnam. It's the IEEE CASS flagship forum for AI hardware/circuits research, co-organized this year by IEEE CASS Vietnam and CASS China.

**The Grand Challenge** (the part you asked about) is the competitive track. For 2026 it's an **edge VLM inference challenge**:

- The AI Large Model Competition — IEEE AICAS 2026 Grand Challenge focuses on the design and optimization of hardware acceleration architectures for Vision-Language Models (VLM) on the edge.
- The task: deploy and run large models on the KV260 platform, utilizing the CPU and FPGA resources available on the chip. The KV260 is a Xilinx/AMD Kria embedded board (Zynq UltraScale+ MPSoC — quad ARM Cortex-A53 + FPGA fabric).
- Target model: Participants are encouraged to design dedicated computing architectures to explore the performance limits of the SmolVLM2 model on the target hardware — SmolVLM2 being HuggingFace's small (256M–2.2B) vision-language model family, deliberately chosen because it's edge-deployable.
- Reward: The top three teams will be invited to present at the 2026 AICAS conference.
- Hosts include SJTU, Fudan, Xidian, Nanjing University, UESTC, ECNU, ICT/CAS, and Pingtouge (T-Head, Alibaba's semiconductor arm).

So in short: it's a **quantize-and-accelerate-a-VLM-on-an-FPGA-SoC competition** — exactly the kind of inference-optimization work (INT8/INT4 quantization, custom matmul/attention dataflow on FPGA, KV-cache management under tight memory) that sits at the intersection of your transformer-internals and inference-optimization interests. If you wanted a concrete frontier project, getting SmolVLM2 running efficiently on a KV260 would force you through the whole stack: model quantization → operator mapping → FPGA dataflow design.

References:

- [AICAS 2026 official site](https://2026.ieee-aicas.org/)
- [AICAS 2026 Grand Challenge — Edge VLM Inference (CompeteHub)](https://www.competehub.dev/en/competitions/tianchi532451)
- [IEEE CASS — AICAS 2026 event page](https://ieee-cas.org/conference-events)
- [AICAS 2026 Call for Papers (PDF)](https://ieee-cas.org/files/ieeecass/2025-06/AICAS-2026_CFP_Updated.pdf)
