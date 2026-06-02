---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 对NeurIPS会议实践的批判
translated: true
type: note
---

问题：关于 NeurIPS 有哪些鲜为人知的观点？

答案：
NeurIPS（神经网络信息处理系统）是机器学习和人工智能领域的顶级会议，在研究界引起了强烈反响。尽管它因推动该领域发展而备受赞誉，但许多参与者对其规模、流程和优先事项表示不满。下面，我整理了一些在 Reddit 的 r/MachineLearning 和 X（前身为 Twitter）等平台上讨论的鲜为人知的观点。这些观点突出体现了在评审季或会后反思期间经常出现的批评。它们之所以“鲜为人知”，是因为它们挑战了NeurIPS的崇高地位，但它们得到了评审员、作者和与会者广泛流传的轶事的证实。

### 关于评审过程

- **由于规模和激励机制，评审质量正在下降，会议应收取投稿费以适当支付评审员。** 投稿数量激增（仅 NeurIPS 2024 就超过 13,000 份），评审员是负担过重的志愿者，导致评审仓促、肤浅，甚至由 AI 生成。一位研究人员认为，如果没有经济激励，“评审和讨论期的质量最终会降为零”，建议收取费用以资助专业评审。
- **评审员之间的匿名性导致懒惰或心怀恶意的评审。** 历史上，评审员可以看到彼此的名字，这培养了问责制。现在，匿名同行允许“简短/无内容/心怀恶意”的批评（例如，“你为什么不引用我的论文？”），而不必担心被评判。取消评审员之间的匿名性——同时对作者保密——可以缓和行为，而不会吓到初级研究人员。
- **反驳大多无效，应视情况而定。** 作者在回复上投入了大量精力，但评审员很少有意义地参与。一个建议是：让领域主席在评审后决定是否需要反驳，从而避免所有人的不必要工作。
- **禁止不合格的评审员未来投稿早就该实施了。** Anima Anandkumar 等知名人士点名批评了“糟糕的”评审（例如，一句话的驳斥或重大误解），并主张禁止违规者发表论文，直到他们负责任地进行评审。这与呼吁追踪“业力”的呼声不谋而合，尽管执行仍然遥遥无期。
- **简单、优雅的解决方案因缺乏“花哨的数学”而被拒绝。** 评审员经常将好点子斥为“不新颖且过于简单”，这促使作者在论文中填充不必要的定理或复杂性。一位 NeurIPS 评审员总结道：“一个重要问题的漂亮解决方案，但不够新颖且过于简单。”

### 关于论文质量和内容

- **投稿越来越无聊、令人困惑，甚至完全是欺诈性的。** 评审员报告了 LLM 生成的论文（简短、错误百出、没有实验）、不同标题下的重复投稿，或使用私人公司数据编写的无法重现的工作。有一批五篇论文中只有一篇“相当不错”；其余的都令人费解或不道德。
- **NeurIPS 奖励数学而非真正的进展。** 会议偏爱“花哨的数学”论文，但现代 AI 进展（例如，更好的数据整理、过滤和反馈循环）“不性感”且未受到重视。这种不匹配忽略了真正“移动损失曲线”的东西。
- **太多论文都是流程拼接或没有影响的利基基准。** 常见的抱怨：现成的模块次优组合用于指标，或者利基领域的新基准缺乏用户相关性或范式转变。这些感觉更像是打卡练习而非突破。
- **群体思维扼杀了创新。** 与会者注意到围绕最新思想存在一种“保护主义”氛围，导致边缘基准调整。下一个重大飞跃不会来自 transformer 或 LLM，而是来自更大胆、风险更高的工作。

### 关于会议体验和可访问性

- **NeurIPS 感觉像一个公司机场休息室，而不是“思想交流会”。** 拥有 20,000 多名与会者，它是一个充满赠品、人脉过度的会议——招聘、“协同效应”聊天和令人疲惫的徽章收集——而不是深入的讨论。真正的价值？偶然的酒吧餐巾纸草图，而不是大型会议。
- **它是一个有缺陷的“排名机制”，顶尖人才会跳过。** 被视为 IMO/IOI 式的竞赛，用于筛选“更聪明的孩子”，它给学者带来了负担，而“最聪明”的人加入了初创公司。许多人对演讲不感兴趣，非研究人员（例如行业招聘人员）占据主导地位。
- **虚拟参会的“即时驳回”歧视弱势研究人员。** 会议截止日期后悄悄更改政策，要求现场注册，这让那些无法承担旅行费用的人受到了打击。在一个已经精英云集的领域，为什么要惩罚全球参与？
- **非法或噱头海报削弱了会议的声望。** 玩笑海报（例如，“生成式奶茶”或模仿真实海报的创业公司广告）利用了梦寐以求的版面，使来之不易的录用变成了附加节目。这是激发乐趣还是仅仅为了蹭热度？

这些观点反映了一个处于十字路口的会议：NeurIPS 推动了 AI 的发展，但也因其成功而倍感压力。许多人建议进行改革，例如分设专题、更好的激励措施或强调可重现性。如果您正在投稿或参加会议，请准备好应对混乱——这是魅力（或诅咒）的一部分。

参考文献：

- [NeurIPS Paper Reviews Released, Controversies Resurface](https://medium.com/syncedreview/neurips-paper-reviews-released-controversies-resurface-4c7347861bd7)
- [r/MachineLearning: [D] NeurIPS 2024 Paper Reviews](https://www.reddit.com/r/MachineLearning/comments/1efscr2/d_neurips_2024_paper_reviews/)
- [r/MachineLearning: [D] NeurIPS 2025 Reviews](https://www.reddit.com/r/MachineLearning/comments/1m74ugv/d_neurips2025_reviews/)
- [X Post by @jxmnop on reviewing awful papers](https://x.com/jxmnop/status/1937949143084810625)
- [X Post by @DBahdanau on NeurIPS as a ranking mechanism](https://x.com/DBahdanau/status/1953968232777289733)
- [X Post by @tsunghan_wu on unexciting paper types](https://x.com/tsunghan_wu/status/1983080396779901184)
- [X Post by @rao2z on inter-reviewer anonymity](https://x.com/rao2z/status/1771272256498594218)
- [X Post by @NeelNanda5 on virtual attendance policy](https://x.com/NeelNanda5/status/1958636440478273725)
- [X Post by @arrtnem on conference overload](https://x.com/arrtnem/status/1996836872119554347)
