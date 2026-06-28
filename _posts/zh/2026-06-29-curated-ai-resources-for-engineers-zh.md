---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工程师精选AI资源
translated: true
type: note
---

让我找出当前活跃且值得你关注的内容。搜索结果大多是硬件厂商的SEO文章，不值得你花时间。以下是为训练模型和构建Agent的工程师精心整理的真正有价值的网站列表。

**问题：** 对于一个深度技术型、AI优先的工程师来说，有哪些热门/有趣的AI和GPU网站值得关注？

**回答：**

**训练内部原理与深度技术写作**
- **[Karpathy的博客 + nanochat/nanoGPT仓库](https://github.com/karpathy/nanochat)** — 你已经在关注了，但他的GitHub Discussions和issues才是真正教学发生的地方。关注nanochat仓库的动态。
- **[Lil'Log (Lilian Weng)](https://lilianweng.github.io/)** — 关于注意力机制、扩散模型、RLHF、奖励黑客的权威深度文章。数学密集，完全符合你的需求。
- **[Jay Alammar](https://jalammar.github.io/)** — 图解Transformer/LLM内部原理。可视化但不肤浅。
- **[Sebastian Raschka的Ahead of AI](https://magazine.sebastianraschka.com/)** — 关于LLM训练、微调和架构论文的最佳信噪比通讯。他发布实际的PyTorch实现（他的`LLMs-from-scratch`仓库与文章配套）。
- **[Eleuther AI博客](https://blog.eleuther.ai/)** — GPT-NeoX、扩展定律，那些真正从零训练开源模型的人。

**GPU / CUDA / 内核**
- **[GPU MODE](https://github.com/gpu-mode)**（原CUDA MODE）— Discord + YouTube + 仓库。内核编写、Triton、FlashAttention内部原理的社区。这是你CUDA/推理优化方向的最佳去处。
- **[Horace He / "从第一性原理让深度学习飞起来"](https://horace.io/brrr_intro.html)** — 内存受限 vs 计算受限，所有GPU优化的思维模型。
- **[Modal博客](https://modal.com/blog)** 和 **[Together AI博客](https://www.together.ai/blog)** — 实用的推理/训练基础设施，FlashAttention的作者团队在Together附近。
- **[vLLM博客](https://blog.vllm.ai/)** 和 **[llm-d](https://llm-d.ai/blog)**（上面提到过）— PagedAttention、前缀缓存、分布式推理。最近llm-d关于精确前缀缓存感知调度的文章报告了通过让调度器直接内省分布式vLLM KV缓存而获得的大幅吞吐量提升。

**MoE / 前沿架构（你对DeepSeek v4的兴趣）**
- **[DeepSeek的GitHub + 技术报告](https://github.com/deepseek-ai)** — 阅读实际论文（DeepSeek-V3、MLA、MoE负载均衡）。他们的开源基础设施仓库（FlashMLA、DeepEP、DeepGEMM）是内核级MoE的宝藏。
- **[Tri Dao的博客](https://tridao.me/)** — FlashAttention、Mamba、状态空间模型，来自源头。

**值得关注的聚合器**
- **[Hacker News](https://news.ycombinator.com/)** — 筛选AI/GPU相关帖子；评论线程往往比文章本身更有价值。
- **[r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)** — 开源权重模型、量化、单GPU实验的脉搏。与你的RTX 4070 / MI300X调试工作相符。
- **[The Gradient](https://thegradient.pub/)** 和 **[Sebastian Ruder的NLP通讯](https://newsletter.ruder.io/)** — 研究层面的深度内容。

**与你偶像级别的匹配**
- **[王垠的网站](https://www.yinwang.org/)** — 你知道的；值得重读他的编译器/编程语言文章，学习第一性原理的严谨性。
- **[Simon Willison的博客](https://simonwillison.net/)** — 高产、公开构建、LLM工具和CLI Agent。精神上最接近你的`ww`/`iclaw`/`zz`工作流。

如果必须选三个开始：**GPU MODE**（内核/CUDA）、**Sebastian Raschka**（带代码的从零训练）、**DeepSeek的仓库**（前沿MoE）。这三个直接对应你的MI300X训练、nanochat工作和DeepSeek v4 MoE探索。

**参考资料：**

- [Lil'Log](https://lilianweng.github.io/)
- [Ahead of AI — Sebastian Raschka](https://magazine.sebastianraschka.com/)
- [GPU MODE](https://github.com/gpu-mode)
- [Making DL Go Brrrr — Horace He](https://horace.io/brrr_intro.html)
- [DeepSeek AI GitHub](https://github.com/deepseek-ai)
- [vLLM博客](https://blog.vllm.ai/)
- [llm-d博客](https://llm-d.ai/blog)
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)