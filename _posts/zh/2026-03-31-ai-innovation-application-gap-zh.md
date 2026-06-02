---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 创新与应用鸿沟
translated: true
type: note
---

问题：近年来，LLM 模型创新（如 FlashAttention、RoPE 等）是否远少于 LLM 应用（如 menus、OpenClaw、OpenCode 等）？基础算法的改进是否仍然更难，投入的人员更少，重大突破也更少？

回答：

是的 —— 你的直觉大体上是正确的。在以下两者之间存在着**巨大的失衡**：

* **基础 LLM 算法创新**（稀少、困难）
* **LLM 应用 / 工具 / agents**（普遍、爆发式增长）

但其原因在于**结构性**因素，而不仅仅是“人们更喜欢做应用”。

---

# 1. 基础 LLM 创新极其困难

诸如此类的事物：

* FlashAttention
* RoPE
* ALiBi
* Mixture-of-Experts (MoE) 扩展
* KV-cache 优化
* Speculative decoding
* Transformer 架构调整

这些需要：

* 深厚的数学功底
* GPU kernel 知识
* distributed systems (分布式系统)
* 大规模训练经验
* 接触海量 compute (算力) 的机会
* 强大的研究背景

只有**极少数团队**能做到这些：

* 大型实验室 (big labs)
* 顶尖大学
* 少数精英开源研究者

所以很自然地：

> 更少的人员 → 更少的突破

---

# 2. LLM 应用的构建门槛要低得多

诸如以下应用：

* agents
* OpenClaw 风格的电脑控制
* menus / 工作流
* RAG 系统
* copilots
* 自动化工具

仅需要：

* prompt engineering
* API 调用
* 胶水代码 (glue code)
* orchestration (编排)

无需进行：

* 训练模型
* 发明数学公式
* 修改 attention
* 编写 CUDA kernels

因此：

> 庞大的开发者群体 → 应用程序的爆发

---

# 3. 创新难度对比

| 级别 | 难度 | 示例 | 谁能胜任 |
| :--- | :--- | :--- | :--- |
| LLM 理论 | 极难 | 新的 attention 机制 | 研究实验室 |
| 训练算法 | 很难 | FlashAttention | infra 研究员 |
| 模型架构 | 很难 | MoE routing | 精英团队 |
| 推理优化 | 难 | vLLM / paged attention | 系统专家 |
| Agent 框架 | 中等 | OpenClaw 风格 | 资深工程师 |
| 应用程序 | 简单–中等 | 聊天工具, copilots | 广大开发者 |

所以，是的 —— **基础性的改进要罕见得多。**

---

# 4. 此外：算法改进的边际收益在递减

早期阶段：

* Transformer（巨大的飞跃）
* Attention（巨大的飞跃）
* Scaling laws（巨大的飞跃）

现在：

* 改进多为增量式的
* 3–10% 的提升
* 效率提升
* 内存占用减少

获得以下成果要困难得多：

> “10倍量级的突破”

因此，创新会**自然地放缓**。

---

# 5. 与此同时，应用领域仍大有可为

应用领域依然拥有：

* UI 创新
* 工作流创新
* multi-agent 系统
* 电脑控制
* 集群控制
* 自主编码 (autonomous coding)
* 个人助手

因此，**应用层仍处于早期阶段**，而：

> 模型架构已经趋于成熟

---

# 6. 这是技术演进中的正常现象

同样的模式在以前也发生过：

阶段 1
算法突破
(Transformer 时代)

阶段 2
基础设施优化
(vLLM, FlashAttention)

阶段 3
应用爆发 ← 我们目前所处的阶段

阶段 4
系统级智能
(agent 集群, 自主系统)

---

# 7. 但重要的一点是：应用仍在推动模型创新

尽管基础创新较少，但：

应用层的需求倒逼：

* 更长的 context (上下文) → RoPE scaling
* 更快的推理 → FlashAttention
* 更廉价的服务 → MoE
* 工具使用 (tool use) → function-calling 训练
* 内存/存储 → RAG-aware 训练

因此：

> 应用间接地推动了算法的突破

---

# 最终结论

是的 —— 你的看法是正确的：

* 基础 LLM 创新**更难**
* 从事相关工作的人更少
* 出现的重大突破更少
* 应用层爆发速度更快

这在技术成熟过程中是符合预期且正常的。

但**下一次重大突破**很可能来自：

* 推理时计算 (inference-time compute)
* agent-native 模型
* 集成了内存的 transformers
* 多模型路由 (multi-model routing)
* 分布式思考模型 (distributed thinking models)

因此，我们正处于一个**宁静但深层的创新阶段**，而非停滞不前。
