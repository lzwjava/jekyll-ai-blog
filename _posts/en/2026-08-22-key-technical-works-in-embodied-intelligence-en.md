---
audio: false
generated: true
image: false
lang: en
layout: post
title: Key Technical Works in Embodied Intelligence
translated: false
type: note
---

**Question:** What papers and technical methods in embodied intelligence does Fan Haoqiang mention in the article?

**Answer:** Here are all the technical works and concepts he references:

---

### Foundational Papers / Models

| Name | What he says about it |
| --- | --- |
| **Action Transformer** | One of the key works from 2024 that clarified how to combine AI with robotics |
| **Diffusion Policy** | Another 2024 work that helped map out the technical roadmap |
| **Pi (π0)** | Described as a "culminating work" that showed how Transformer applies to robot control — laid out the roadmap for the field |
| **Pi 0.6 / RECAP** | A core algorithm for human-correction feedback loops during deployment |

---

### Architectures & Technical Concepts

| Name | Context |
| --- | --- |
| **VLA** (Vision-Language-Action model) | The main model paradigm they're building around — valued for its **generalization ability** (e.g. switching from Coke to Pepsi without retraining) |
| **Transformer** | Discussed as the dominant architecture, though he notes it has evolved so much it now resembles convolution |
| **ConvNeXt** | Zhang Xiangyu's (张祥雨) paper from Megvii, arguing convolutions can match Transformers on vision tasks |
| **Dswin** (Sliding Window Attention) | Mentioned as an example of how Transformer and convolution have converged |

---

### Their Own Open-Source Work

| Name | Description |
| --- | --- |
| **Dexbotic (DB)** | Their open-source training codebase |
| **RoboChallenge (RC)** | Their open-source robot evaluation/benchmarking framework — already attracting 5-6 companies to apply for testing |
| **table30** | Their internal benchmark of 30 standardized tabletop manipulation tasks |
| **DOS-W1** | Their jointly developed data collection robot, now in mass production |

---

### Feedback / Deployment Algorithms

| Name | Origin | What it does |
| --- | --- | --- |
| **RECAP** | Pi 0.6 paper | Records human corrections to robot actions and feeds them back into training |
| **DAG** | General term | Same concept, different name |
| **SOP** | Shanghai Zhiyuan (智元) | Their version of the same closed-loop correction approach |

---

**Key Insight He Draws:** All these different routes — simulation, real data collection, world models — are like paths diverging at the base of a mountain but converging at the top. The underlying technical problems are the same regardless of approach.
