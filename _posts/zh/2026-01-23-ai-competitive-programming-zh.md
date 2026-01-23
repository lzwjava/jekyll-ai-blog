---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 人工智能对算法竞赛的影响
translated: true
type: note
---

Question: 既然 AI 在解决 Codeforces 问题方面已经如此先进，那么比赛还有意义吗？人们可以轻松作弊并完成 3 到 4 道题，对吧？

Answer: 

**是的，比赛仍然有意义——但 2025-2026 年的情况已经发生了显著变化。**

AI（特别是像 OpenAI 的 o3 / o4 系列模型）在 competitive programming 方面已经变得极其强大：
- 顶尖 AI 模型达到约 2700-2800 Codeforces rating（处于人类前 0.2-0.3% 的水平，全球排名约为 100-200 名）。
- 它们在 ICPC WF 2025 中达到了金牌水平，并在 IOI 级别的比赛中取得了非常强劲的成绩。
- 在许多 Div. 2 / Div. 3 / Div. 4 轮次中，现代 AI 如果获得题面，可以非常迅速地解决 4-6 道题。

这使得 **cheating 变得比以前容易得多**。许多参赛者现在将题面输入给 AI（有时仅进行极少的修改）并提交。在最近的一些轮次中：
- 在某些情况下，高排名中有一个明显的比例（约 4%）来自被检测出的 AI cheaters，他们的成绩随后被跳过或回滚。
- 在较简单的比赛中，对于任何愿意作弊的人来说，用 AI 解决 3-4 道题是轻而易举的——你甚至不再需要强大的 coding 技能。

尽管如此，对于大多数严肃的参与者来说，比赛 **并非没有意义**。原因如下：

- **纯粹的享受和个人成长** 仍然是核心价值。许多人（可能是大多数活跃参与者）参加比赛是为了乐趣、学习 algorithms、在时间压力下进行训练，以及自己解决难题后的成就感。除非你允许，否则 AI 无法夺走这些。
- 对于诚实的参与者来说，**rating 仍然反映了人类的技能水平**——即使绝对数值因 cheaters 而被抬高或压低。如果你持续进步，随着时间的推移，你的 delta 仍会保持正向（只是基准线与 2-3 年前不同）。
- **顶尖水平的人类竞争** 仍然非常有意义。AI 尚未能在所有比赛形式中持续击败最顶尖的人类（例如 tourist ~3900+ 的水平），特别是在那些不寻常、具有创意或 heavy-implementation 的问题上。
- **Community 和 anti-cheat 措施** 确实存在。Codeforces 会封禁明显的 AI cheaters（特别是 copy-paste 风格的），在抓获大批作弊者时会回滚 ratings，并明确规定禁止在比赛期间使用 AI 辅助（包括在提交失败后使用 AI 进行 debugging）。

目前的现实情况（2026 年初）：
- **Div 4 / Div 3 / 简单的 Div 2** → AI cheating 现象严重，利用 AI 解决 3-4 道题很容易，作弊者的 ratings 有所虚高。
- **困难的 Div 2 / Div 1** → AI 虽然强大，但远非不可战胜；具有创意、侧重 proof 或 heavy-implementation 的问题对当前模型来说仍然很困难。
- **诚实的参与者** 与 2023-2024 年的水平相比，由于 cheater 导致的通胀，rating 通常会下降 100-400 分，但技能的提升依然能从表现中体现出来。

许多强大的 coders 现在更多地将 competitive programming 视为：
- 一种有趣的 puzzle-solving 爱好
- Algorithm 学习和 interview preparation
- 一项与朋友/社区共同参与的类体育活动

而不是纯粹的 rating 追逐。

**底线**：如果你的目标是诚实的自我提升、智力挑战和享受过程 → 比赛仍然非常有意义。  
如果你的唯一目标是高 rating / 顶尖排名 → 是的，由于普遍的作弊现象和 AI 的能力，现在这变得更加困难和令人沮丧。

社区中的大多数人之所以继续参与，是因为他们热爱这个过程，而不仅仅是为了那个数字。

References:  

- [Codeforces blog on AI cheating and top rank rollbacks (2026)](https://codeforces.com/blog/entry/149941)
- [OpenAI o3 model Codeforces performance discussion](https://codeforces.com/blog/entry/134002)
- [Codeforces rule restricting AI usage (2024, still active)](https://codeforces.com/blog/entry/133941)
- [ICPC 2025 AI performance claims](https://codeforces.com/blog/entry/146536)