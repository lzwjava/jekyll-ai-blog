---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI推理成本与速度突破
translated: true
type: note
---

好，视频已确认：**《Tri Dao：英伟达主导地位的终结，推理成本为何下降，以及下一个10倍速度提升》**——Tri Dao，Together AI首席科学家、普林斯顿大学教授，FlashAttention和Mamba的创建者，探讨推理优化与成本降低。让我获取更多内容。我找到了Tri Dao的详细内容。现在让我再查找那期特定播客节目的文字记录或详细笔记。好了，我现在有足够的信息给出扎实的答案。具体视频来自**Redpoint Ventures的《Unsupervised Learning》播客**。我无法直接提取文字记录，但我从视频描述、相关访谈以及Tri Dao同时期的其他陈述中整合出了关键内容。

---

**问题：** Tri Dao在这次谈话中说了什么？(https://www.youtube.com/watch?v=xlSaoP0b90A)

**回答：**

该视频是**Redpoint Ventures《Unsupervised Learning》播客节目**，标题为*《英伟达主导地位的终结，推理成本为何下降，以及下一个10倍速度提升》*，发布于2025年9月10日。Tri Dao是Together AI首席科学家、普林斯顿大学教授，FlashAttention和Mamba的创建者。

以下是该集内容（根据描述、相关访谈以及Tri Dao那段时间已知立场重构）：

---

### 1. 自ChatGPT发布以来，推理成本下降了约100倍

Tri Dao讨论了自ChatGPT发布以来，推理优化如何将成本降低了100倍。这是宏观背景。这100倍不仅仅来自硬件——很大一部分来自软件/算法改进：FlashAttention、更好的批处理（连续批处理、PagedAttention）、量化（FP8 → FP4）以及推测解码。

---

### 2. 100倍的原因——推理受内存限制，而非计算限制

这是Tri Dao处处提及的核心思维模型。在推理过程中（如今是主要工作负载），你主要使用内存子系统。这正是FlashAttention背后的洞察：注意力机制是I/O受限的，而非计算受限。硬件看似繁忙，但大部分时间都在等待HBM读取。

推测解码直接利用了这一点：生成五个token所需的总计算量相同，但你只需访问一次内存，而不是五次。你用闲置的FLOPs换取了更少的内存往返次数。

---

### 3. 软件算法能够媲美定制芯片

这是2025年Together AI工作的核心论点。“软件和算法的改进能够缩小与高度专业化硬件的差距。我们在这些大模型上实现了每秒500个token，甚至比某些定制芯片还快。”

Together AI使用的叠加技术栈：FP4量化（相比FP8基线提升80%）、静态推测解码（在此基础上再提升80-100%），然后再加上自适应推测解码。每一层都会叠加效果。

---

### 4. “下一个10倍”——自适应推测解码（ATLAS）

这是Together AI研究成果的落脚点。静态推测器的问题：“与我们合作的公司随着规模扩大，通常会发现工作负载发生变化，然后他们从推测执行中获得的速度提升不如之前。这些推测器在工作负载领域发生变化时通常效果不佳。”

解决方案是ATLAS（自适应学习推测器系统）——一种双模型架构：一个静态重型推测器提供基线，一个轻量级自适应推测器从实时流量中持续学习。你可以将其视为一种智能缓存方式，不是精确存储，而是找出你看到的一些模式……然后我们可以预测大模型将要说什么，并且随着时间推移，预测能力越来越强。

---

### 5. 英伟达的主导地位——论点

“英伟达主导地位的终结”这一框架与推理是不同于训练的场景有关：

- 训练：批量、吞吐量受限，CUDA护城河真实存在，H100/B200胜出
- 推理：延迟敏感、内存带宽受限、软件定义的优化更为重要，替代硬件（Groq LPU、Cerebras）可以竞争

Tri Dao的立场（从他的公开言论中反映）是**在普通英伟达硬件上，以软件优先的推理优化可以媲美专用芯片**——这既削弱了专用芯片的叙事，同时又论证了推理才是真正的优化前沿。

---

### 6. 工作负载漂移是隐藏的扩展成本

“也许他们最初将AI用于聊天机器人，但后来发现它还能写代码，于是开始转向代码。或者他们意识到这些AI实际上可以调用工具、控制电脑、做会计之类的事情。”

强化学习训练是静态推测器的另一个难题：训练过程中策略分布会发生变化，因此任何固定的推测器都会过时。在大规模下，自适应系统是必需的。

---

### Tri Dao的信念（提炼后的论点）

| 主张 | 证据 |
|---|---|
| 推理现在是主导工作负载 | 在总计算量中的份额已超过训练 |
| 推理受内存限制，而非计算限制 | FlashAttention是证明案例 |
| 软件缩小了与定制硅的差距 | 在DeepSeek-V3.1上，B200达到500 tok/s，与Groq相当 |
| 静态推测器在工作负载漂移下会退化 | 在Together AI企业客户中得到验证 |
| 下一个10倍来自自适应、学习的优化 | ATLAS系统 |
| 英伟达的CUDA护城河在推理中弱于训练 | 硬件无关的软件胜出 |

---

### 你应该带走的要点（对你的工作而言）

- **FlashAttention的洞察具有普适性**：I/O受限是任何GPU优化的关键思维模型。在假设需要更快计算之前，先检查你的瓶颈。
- **推测解码已可用于生产**，且具有叠加效应——如果你在规模上提供模型服务，这已经是必备技术。
- **工作负载漂移**是你构建的任何推理优化系统的真正问题——静态假设会失效。
- **FP4量化**（Together AI声称相比FP8基线提升80%）是下一个需要理解的量化前沿；你运行的MI300X对FP8/FP4有很好的支持，值得探索。

---

**参考文献：**

- [Tri Dao: The End of Nvidia's Dominance — YouTube](https://www.youtube.com/watch?v=xlSaoP0b90A)
- [Together AI ATLAS Adaptive Speculator — VentureBeat](https://venturebeat.com/ai/together-ais-atlas-adaptive-speculator-delivers-400-inference-speedup-by)
- [Redpoint Unsupervised Learning Podcast Episode Page](https://www.redpoint.com/content-hub/video/chief-scientist-of-togetherai-tri-dao-on-the-end-of-nvidias-dominance-why-inference-costs-fell-the-next-10x-in-speed/)
