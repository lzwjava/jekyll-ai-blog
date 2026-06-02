---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 针对Kimi K2的MuonClip优化器
translated: true
type: note
---

### Muon优化器概述

Muon优化器是由Moonshot AI创始人兼CEO杨植麟（Zhiling Yang）在开发大语言模型Kimi K2时提及的一种前沿优化算法[1][2][3]。这是一种受二阶优化启发的优化器，通过高秩更新更好地适应模型训练过程中损失曲面的几何特性[2]。但该优化器存在训练不稳定的问题，为此Moonshot AI开发了增强版本MuonClip[1][4]。

### 核心特性
- **效率与设计**：Muon追求token效率，即相比传统优化器（如AdamW）处理更少的token即可达到相当或更优的性能。其设计灵感源自二阶优化方法（如牛顿法），但针对大规模深度学习场景进行了适配[2][3]。
- **稳定性问题**：基础版Muon优化器在长时间训练过程中可能引发不稳定性（如损失值突变），因其在特定条件下容易发散[2][1]。
- **MuonClip增强**：Moonshot AI通过将Muon与"QK-Clip"技术结合开发了MuonClip，该技术通过裁剪注意力机制中的查询-键交互来防止训练失稳，最终实现了在15.5万亿token上稳定无突变的Kimi K2训练[1][4][5]。

### 在Kimi K2中的应用
MuonClip对预训练Kimi K2模型（总参数量1万亿的混合专家模型，激活参数量320亿）起到关键作用。该优化器帮助Moonshot AI在Tau2-Bench（66.1）、ACEBench（76.5）和SWE-Bench Verified（65.8）等基准测试中取得领先成绩，且无需扩展思维步骤[4][6]。杨植麟强调这是开源AI发展的重大突破，突显了该技术对实现高效稳定大规模训练的作用[7][8]。

技术细节可参阅arXiv上的Kimi K2论文[1][4]。杨植麟在2025年7月模型发布期间的访谈和公告中对此进行了详细阐述[2][7]。

引用文献：
[1] https://arxiv.org/pdf/2507.20534?
[2] https://artificialintelligencemadesimple.substack.com/p/kimi-k2-is-the-most-important-model?utm_source=post-email-title&publication_id=1315074&post_id=169438943&utm_campaign=email-post-title&isFreemail=true&r=36rt3&triedRedirect=true&utm_medium=email
[3] https://composio.dev/blog/notes-on-kimi-k2
[4] https://arxiv.org/abs/2507.20534
[5] https://www.hpcwire.com/2025/07/16/chinas-moonshot-ai-releases-trillion-parameter-model-kimi-k2/
[6] https://intuitionlabs.ai/pdfs/analysis-of-the-kimi-k2-open-weight-language-model.pdf
[7] https://www.chinatalk.media/p/kimi-k2-the-open-source-way
[8] https://github.com/MoonshotAI/Kimi-K2
