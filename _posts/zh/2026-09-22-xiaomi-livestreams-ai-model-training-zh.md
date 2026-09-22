---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小米直播AI模型训练
translated: true
type: note
---

**问题：** `https://mimo.xiaomi.com/rl/#overview` 这个页面是什么？

**答案：**

该网址是一个**实时公开仪表板**，小米 MiMo AI 团队在此直播其下一代模型——**MiMo-V2.6-Pro** 和 **MiMo-V2.6-Flash**——在主动训练过程中的实时训练指标。

以下是详细说明：

**什么是 MiMo：** MiMo 是小米开发的一系列大型语言模型（LLM），于 2025 年 4 月首次发布。它是一个专注于推理的模型，是小米“人×车×家”生态中的关键 AI 组件。

**这个仪表板是什么：** 小米 MiMo 团队正通过这个公开仪表板实时直播两个未发布模型——MiMo-V2.6-Pro 和 MiMo-V2.6-Flash——的强化学习（RL）训练阶段。该页面直接显示来自训练器日志的训练指标，包括奖励曲线、滚动次数、步进时间和运行计算成本。

**为何值得关注：** 前沿实验室通常只在训练完成后报告训练后结果。而在这里，任何人都可以在训练仍在进行时观看。

**仪表板显示的内容：** 该页面显示模型训练进度、Token 消耗量、训练成本、样本数量以及多个内部指标的变化。同时展示了 MiMo-V2.6-Pro 和 MiMo-V2.6-Flash 两个版本。截至 2026 年 9 月中旬，两个版本的累计训练总成本已超过 116 万美元。

**背后的动机：** 小米 MiMo 负责人刘付丽表示，团队近半年来一直研究同一个问题：强化学习（RL）究竟可以进一步扩展到什么程度？她透露，团队正在从三个维度扩大规模——计算资源、训练环境和任务系统，以及奖励评估机制。

简而言之，这是小米 AI 模型训练的透明直播窗口——这在行业内相当罕见。

---

**参考文献：**
- [Xiaomi MiMo – 维基百科](https://en.wikipedia.org/wiki/Xiaomi_MiMo)
- [小米实时直播 MiMo-V2.6 RL 训练 – NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/xiaomi-mimo-v2-6-live-rl-dashboard)
- [小米直播 MiMo V2.6 RL 训练 – TechNode](https://technode.com/2026/09/18/xiaomi-livestreams-mimo-v2-6-reinforcement-learning-runs/)
- [MiMo 训练直播报道 – 36Kr](https://eu.36kr.com/en/p/3986962267765767)