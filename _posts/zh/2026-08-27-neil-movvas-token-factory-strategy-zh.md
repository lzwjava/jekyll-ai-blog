---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Neil Movva的代币工厂策略
translated: true
type: note
---

**问题：** Neil Movva 在最近与 Patrick O'Shaughnessy 的《Invest Like the Best》节目中提到的关键内容是什么？

**回答：**

该期节目于 **2026年8月25日** 播出。以下是主要主题的梳理：

---

**1. "Token工厂"论点——AI 正在为错误的工作负载优化**

Movva 的核心论点是，整个 AI 堆栈——从 GPU 内核到数据中心供电——都是围绕需要低延迟的交互式聊天机器人构建的，而真正的增长市场是那些无需监督即可运行数小时或数天的后台代理。对于这些工作负载，延迟无关紧要，每个 token 的成本才是关键。

Sail 正在构建他所谓的"Token工厂"——一家为未来而设计的推理公司，在这个未来中，AI 代理会在后台持续运行数小时或数天，而不是实时回答人类的问题。在那个世界里，延迟不那么重要，成本更重要。

---

**2. 拾荒者策略**

Movva 的策略明确是一种拾荒者方法：购买大型玩家忽略的芯片，在超大规模企业看不上眼的小型设施中租用电力，并容忍对其他人来说可能是致命的正常运行时间水平。他的公司北极星目标是实现 token 成本降低 1000 倍。

关于芯片，他表示：没有不好的芯片，只有不好的定价——他很乐意购买 AMD、SambaNova、Google TPU 和 Amazon Trainium，因为其他人低估了它们。关于电力，他愿意购买大型玩家忽视的 1 兆瓦设施中的容量，甚至接受 95% 的正常运行时间，因为当某个设施出现故障时，他的控制平面可以将工作负载转移到其他地方。

---

**3. 芯片：Cerebras 与 Nvidia——并非赢家通吃**

Movva 预测的是一种混合结果，而非赢家通吃的竞争。Cerebras 和类似的芯片将作为计算受限层的加速器，与具备注意力层和长上下文窗口所需片外 DRAM 容量的传统 GPU 搭配使用。

他还指出了他所谓的**Transformer 的"原罪"**：Transformer 将一个极度内存受限的层（注意力层）紧挨着一个计算受限的层（MLP），这使得几乎不可能有单一芯片设计对两者都达到最优。

---

**4. 数据与开源**

Movva 认为，互联网是一次大约 30 万亿高质量文本 token 的"一次性补贴"，而模型已经多次吸收过这些数据。未来是通过在具有可验证任务的隔离"训练场"环境中进行强化学习，实现模型的自我改进。

关于开源，他指出，即使没有刻意抓取，AI 生成的内容也在互联网上大量扩散："我们将在很长一段时间内面临潜在的蒸馏问题。似乎从根本上无法阻止信息或模型能力的扩散。"

---

**5. 这是泡沫吗？——与互联网泡沫的对比**

Movva 区分了当今的 token 消费——即时且非投机性的——与互联网泡沫时代投机性的基础设施建设。他的观点是：人们购买 token 是因为它们立即可用；你不会囤积 token，而是立即使用它们。

---

**6. TSMC 地缘政治——逆向观点**

他最逆向的观点是关于 TSMC 和地缘政治：他认为，即使在最坏的情况下，像 Intel 这样的西方芯片代工厂"并没有落后太多，最坏的情况下性能功耗比可能只差 2 倍"，并且从一个工艺节点到下一个节点的性能差距并不像芯片战争讨论中所暗示的那样巨大。

---

**参考文献：**
- [BigGo Finance: Neil Movva AI 推理成本降低 1000 倍](https://finance.biggo.com/news/29d3f76c7eeac4a2)
- [Colossus: 《Invest Like the Best》剧集列表](https://colossus.com/series/invest-like-the-best/)
- [Apple Podcasts: 剧集描述](https://podcasts.apple.com/us/podcast/invest-like-the-best-with-patrick-oshaughnessy/id1154105909)
- [Digg: Neil Movva 在播客中讨论 AI 推理](https://digg.com/tech/s7o4z9dq)