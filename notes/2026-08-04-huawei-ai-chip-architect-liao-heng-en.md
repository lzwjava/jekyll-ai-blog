---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huawei AI Chip Architect Liao Heng
translated: false
type: note
---

Question: Who is Huawei scientist 廖恒 (Liao Heng)?

Answer:

廖恒 is a senior Huawei/HiSilicon (海思) scientist known mainly for **AI accelerator architecture, chip design, and computing systems**. He is not a public-facing celebrity like 任正非 or 何庭波, but he is considered one of Huawei's important technical leaders in semiconductor research. ([Tsinghua University][1])

Key career points:

* **Huawei Fellow**
* Former **Huawei 2012 Laboratories Chief Scientist**
* Former **HiSilicon Turing Architecture & Design Department head**
* Associated with Huawei's **Ascend AI chip architecture** work (昇腾 / Ascend). 

His background is unusually hardware-focused:

* Studied at **Tsinghua University Computer Science**, including the Tsinghua "少年班" route.
* Did postdoctoral research at **Princeton University EE department**.
* Worked at **PMC-Sierra** in the US semiconductor industry, with roles including architecture and R&D leadership before joining Huawei. 

His technical area:

```
AI workload
     |
     v
Algorithm / Model
     |
     v
Compiler + Runtime
     |
     v
AI Accelerator Architecture
     |
     v
NPU / ASIC / Memory / Interconnect
```

廖恒's area is mostly the bottom half:

* AI accelerator architecture
* NPU design
* chip/system architecture
* high-performance computing infrastructure

This is the layer where companies compete with NVIDIA. A model like DeepSeek or Qwen needs not only GPUs/NPUs but also:

* tensor compute units
* HBM/memory bandwidth
* inter-chip communication
* compiler stack
* distributed inference/training system

Recent Huawei AI infrastructure work also involves large-scale Ascend clusters and LLM serving architecture. A 2025 paper on Huawei CloudMatrix384 lists a Heng Liao among authors working on large-scale LLM inference architecture. ([arXiv][2])

A rough comparison:

| Person | Main domain                              |
| ------ | ---------------------------------------- |
| 任正非    | Company strategy                         |
| 何庭波    | Semiconductor leadership                 |
| 廖恒     | Chip architecture / AI computing systems |
| 徐直军    | Corporate and product strategy           |
| 王成录    | Software ecosystem                       |

From an AI engineer perspective, 廖恒 represents the **"hardware + systems" side of AI**. The future competition is not only about training bigger models; it is about the whole stack:

```
Model
 ↓
Framework (PyTorch / MindSpore)
 ↓
Compiler (CUDA / Ascend CANN)
 ↓
Runtime (vLLM / SGLang style serving)
 ↓
Accelerator (GPU / NPU / ASIC)
 ↓
Silicon
```

People like 廖恒 operate near the silicon boundary. For someone working on SGLang/vLLM, distributed inference, ROCm/CUDA, or custom accelerators, this is the same strategic layer: making AI cheaper and faster through systems engineering. ([career.huawei.com][3])

References:

* ([Tsinghua University][1])
*
* ([Fudan News][4])
* ([arXiv][2])

[1]: https://www.tsinghua.edu.cn/info/1181/35825.htm?utm_source=chatgpt.com "华为2012实验室总裁何庭波访问清华 探讨基础学科人才培养合作-清华大学"
[2]: https://arxiv.org/abs/2506.12708?utm_source=chatgpt.com "Serving Large Language Models on Huawei CloudMatrix384"
[3]: https://career.huawei.com/cn/young-genius?utm_source=chatgpt.com "挑战课题专项招聘"
[4]: https://news.fudan.edu.cn/2022/0924/c5a132488/page.htm?utm_source=chatgpt.com "复旦-华为微电子联合实验室2022年度研讨会圆满召开"