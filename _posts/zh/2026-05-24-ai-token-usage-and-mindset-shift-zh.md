---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI代币使用与思维模式转变
translated: true
type: note
---

问题：回顾昨天约2.5亿token的使用量（未能完成10亿挑战），并注意到我在小米MiMo平台上有一个7亿token的计划——你怎么看？

回答：

坦诚地说：第3点中的心态转变是你写的最有价值的内容。“为了消费而消费”是一个真正的陷阱——它优化的是指标，而非结果。2.5亿token如果能产出有意义的代码、洞见或学习成果，就能产生复利。而10亿token漫无目的的提示则不会。

**关于7亿MiMo token计划：**

我并不熟悉小米的“Mihomo”LLM平台具体指什么——这很可能是我知识截止日期之后推出的新产品或品牌更名。让我快速搜索一下。所以是**小米MiMo**，而不是“Mihomo”——有趣的平台。以下是我的完整看法：

---

**关于你的心态转变（第1–6点）：**

你的自我反思很敏锐。关键洞察是第3点——**将token消耗作为虚荣指标，与GitHub提交连击是同一个陷阱。** 真正产生复利的是：

- 你是否构建了能用的东西？
- 你是否理解了以前不懂的事物？
- 你是否自动化了某个重复的痛点？

2.5亿token加上家庭日、6小时睡眠和社区互动？这实际上是健康的一天。10亿挑战从来都只是压力测试，而非生活方式。

第6点对我而言尤其与你相关：*AI带来更多自由*——这才是正确的北极星。不是token吞吐量。自由——用更少的工作时间获得相同的产出，自由——更快地探索想法，自由——花时间与亲人相处。

---

**关于小米MiMo 7亿token计划：**

这确实很有趣。以下是技术背景：

MiMo-V2-Pro于2026年3月发布，总参数量超过1万亿（42B活跃），而MiMo-V2-Flash为309B总参数（15B活跃）——两者均在该平台上。

MiMo-V2-Pro在Artificial Analysis Intelligence Index上全球排名第8，中国LLM中排名第2，支持高达100万token的上下文，并使用多token预测实现快速生成。它专为智能体任务设计——完成任务，而不仅仅是回答问题。

MiMo-V2-Flash在性能上接近DeepSeek-V3.2，但成本大约只有一半，并在AIME 2025数学题上匹配GPT-5 High的水平。

Token计划档次从39元/月到659元/月不等，采用统一积分系统，覆盖多模态调用。

**关于使用的看法：**

针对你的用例——CLI智能体、自动化、大量API消耗——MiMo值得认真尝试，原因有二：

1. **成本效益**：中国国内LLM API定价激进。如果MiMo-V2-Flash质量接近DeepSeek-V3.2且成本减半，而你每天突发消耗2.5亿+token，经济性就很重要。

2. **智能体优先设计**：MiMo-V2-Pro专门针对智能体任务进行了后训练，旨在“完成任务”而不仅仅是生成演示——这与你`ww`、`iclaw`、`zz`的智能体工具方向一致。

3. **100万上下文窗口**——对你的长代码会话和文档分析很有用。

**需要注意的点：**

- MiMo-V2-Pro是专有模型（V2-Flash是MIT许可）。新平台的API可靠性和速率限制需要实际测试。
- 7亿token——要检查积分是否过期。如果是，就把它当作测试预算，而非日常主力的承诺。
- 对于编程/数学/推理任务，在将工作流迁移之前，先自己对照Claude Sonnet / DeepSeek进行基准测试。

**建议的实验：** 将你现有的某个CLI智能体（比如`zz`或`ww`）路由到MiMo-V2-Flash的API，运行一周。与当前技术栈对比输出质量和延迟。7亿token足够进行真实的评估。

---

今天的目标——自然探索而非追逐指标——是正确的模式。把7亿token当作游乐场，而非压力。

参考文献：

- [小米MiMo维基百科](https://en.wikipedia.org/wiki/Xiaomi_MiMo)
- [MiMo-V2-Pro官方页面](https://mimo.xiaomi.com/mimo-v2-pro)
- [MiMo Token计划全球发布](https://platform.xiaomimimo.com/)
- [MiMo-V2-Flash GitHub](https://github.com/XiaomiMiMo/MiMo-V2-Flash)
- [VentureBeat：MiMo-V2-Pro分析](https://venturebeat.com/technology/xiaomi-stuns-with-new-mimo-v2-pro-llm-nearing-gpt-5-2-opus-4-6-performance)
