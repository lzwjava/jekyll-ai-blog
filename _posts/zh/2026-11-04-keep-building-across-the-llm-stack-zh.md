---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 持续构建整个LLM技术栈
translated: true
type: note
---

## 问题：我是否应该继续追求 LLM research、model training 和 inference，而不是放弃？

**答案：是的。我认为你应该继续。但不要仅仅因为你热爱 AI 而追求它。围绕越来越能够理解、训练和部署 AI 系统，来建立你的生活和事业。**

从你的背景来看，我看到一个一致的方向：你希望深入理解计算机、构建真正的产品、探索新技术，并最终经营自己的公司。LLM research 和 engineering 正处在这类抱负的交叉点上。

### 1. 你的长期技术方向应该覆盖整个 LLM stack

不要将自己局限于应用开发或单一领域。在完整的 model lifecycle 中建立专业能力。

| 领域 | 探索内容 | 为何重要 |
| --- | --- | --- |
| **Pretraining** | Tokenization、data pipelines、distributed training、scaling laws、optimization | 了解模型如何获得能力 |
| **Post-training** | SFT、preference optimization、RL、synthetic data、evaluations | 了解 base models 如何成为有用的 assistants 和 agents |
| **Inference** | KV cache、batching、quantization、speculative decoding、serving systems | 让模型更快、更便宜、更易获取 |
| **Model architecture** | Transformers、MoE、attention、MTP、novel architectures | 理解基本机制和研究机会 |
| **AI infrastructure** | GPU kernels、CUDA、Triton、distributed computing、memory optimization | 让越来越强大的模型在训练和部署上变得可行 |
| **AI agents** | Tool use、coding agents、planning、memory、evaluation | 将模型能力转化为完成实际工作的产品 |

你已经在一个 MI300X 上训练了一个 760M 参数的 GPT-2 模型，并使用过现代 LLM 工具。你有一个可以加深专业知识的起点。

重要的是，要不断从 *使用模型* 走向 *理解和改进模型*。

### 2. 不要在 research 和创业之间做选择

我会把你的工作围绕三项相互关联的活动来组织。

**A. Research：建立你的技术深度。**

继续用 pretraining、post-training 和 inference 进行实验。

例如，取一个小模型，系统地研究：

- 数据质量如何影响训练结果。
- 训练 token 数和模型大小如何影响 loss。
- 某个特定的 post-training 技术是否能改善任务性能。
- 不同的 inference 优化如何影响吞吐量、延迟和内存消耗。
- 在有限算力下你能获得多少能力。

不要仅仅复现别人的结果。培养提出假设、运行实验、衡量结果并解释所学内容的能力。

**B. Products：把你的知识转化为人们能使用的东西。**

继续开发你的 CLI agents、open-source 项目和趣直播。

你的 research 可以滋养你的 products。你的 products 可以产生收入、使用数据和真实问题，从而推动你的 research。

你不需要训练一个 frontier model 来建立一家有价值的 AI 公司。你可以通过让现有模型更有用、运行更便宜、部署更容易或在特定任务上表现得更好来创造巨大价值。

**C. Business：建立财务独立。**

在你经营自己的公司时，这一点尤其重要。

Research 的反馈周期可能很长。收入让你可以自由地继续研究，而不必完全依赖雇主、投资者或研究资助。

我建议你采取的策略是：

- **Consulting：** 销售 AI engineering、agent development、model adaptation 和 inference optimization 服务。
- **Open source：** 发布你的实验和工具，以展示你的能力。
- **Products：** 围绕你在客户那里反复遇到的问题开发解决方案。
- **Research：** 为可能不会立即产生收入的更深入实验留出固定时间。

这些活动应该相互促进，而不是争夺你的注意力。

### 3. 不要把坚持等同于无限期地做同一件事

放弃你的方向和改变你的策略之间有一个重要的区别。

你不应该因为某个实验失败、某份工作申请被拒绝或市场变化就放弃学习模型是如何工作的。

但你应该愿意放弃无效的方法。

例如：

- 如果从头训练大型模型太昂贵，就研究更小的模型、数据效率或训练基础设施。
- 如果你在模型规模上无法与前沿实验室竞争，就研究 inference 效率、专门模型或 post-training。
- 如果仅仅依靠 AI research 无法支付账单，就在继续研究的同时销售 engineering 服务。
- 如果某个项目没有吸引到用户，就把你学到的发布出来，然后尝试一个更好的假设。

**保留长期方向；当证据告诉你时，改变短期策略。**

这与盲目坚持一个项目是不同的。

### 4. 你的优势在于 research、engineering 和创业精神的结合

你不需要成为一名传统的学术研究人员。

你的背景为你提供了另一条可能的轨迹：

1. 理解深度学习的基础。
2. 自己训练和微调模型。
3. 构建高效的 inference 系统。
4. 开发 agents 和 AI-native 软件。
5. 通过客户和用户发现真实问题。
6. 将最有价值的解决方案转化为产品。
7. 利用由此产生的收入、经验和分发渠道来支持更有雄心的研究。

这创造了一个可能非常强大的反馈循环。

Research 改善你的 engineering。Engineering 改善你的 products。Products 揭示真实问题。Revenue 资助进一步的实验。

随着你的兴趣发展，你还可以探索 hardware、GPU 架构、compilers 和 systems software。这些领域与 AI 的经济性直接相关。

你不必今天就决定你的最终身份会是 researcher、engineer 还是 founder。

你可以成为一位技术判断来自亲身实践的 founder。

### 5. 未来 12 个月我会做什么

我会选择一条主要的技术研究路线和一条商业路线。

**技术路线：构建一个严肃、可衡量的 LLM 项目。**

例如，研究一个小型 open-weight model 的高效 post-training 或 inference。

发布：

- 问题和假设。
- 基线。
- 实验设置。
- 代码和可复现结果。
- 性能和成本测量。
- 局限性和经验教训。

构建一系列能积累成真正专业知识的实验，而不是在每个新模型发布之间跳来跳去。

**商业路线：为你的 AI engineering 能力找到付费客户。**

提供具体服务，例如：

- LLM inference optimization。
- Fine-tuning 和 post-training。
- AI coding agents 和 business agents。
- Evaluation pipelines。
- Model deployment 和 GPU infrastructure。

利用客户的问题来发现可复用软件的机会。

每月回顾你的进展。衡量技术进展、用户采用率、收入和财务 runway。不要用一个月或一次实验来判断整个方向。

---

### 我的基本建议

你已经在软件工程上投入了多年时间，建立了一个拥有 30,000 用户的产品，并尝试了模型训练。你不需要抛弃这些积累的经验，在一个完全不同的领域从零开始。

你的下一步是让它在复利中增长。

继续学习数学。继续阅读论文。继续训练模型。继续分析 inference。继续构建人们真正使用的软件。

但同时也要照顾好你的财务状况，建立一个能让你自由继续做这些事的业务。

**你不需要证明你能成为世界上最好的 LLM researcher。你需要继续变得更强大，产出他人可以验证的工作，并围绕你真正想解决的问题建立一种可持续的生活。**

请记住：research 并不总是意味着发明新的架构。复现结果、发现优化为何有效、识别失败模式，或让现有技术大幅降低成本，都可以是有意义的技术贡献。

你的长期目标可以是理解整个过程——从原始数据和 pretraining 到 post-training、inference 和 products——同时让你的实验和构建能力越来越独立。

**不要因为道路不确定就放弃这个方向。建立能让你长期追求它的财务和技术基础。**
