---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek突然全球爆红
translated: true
type: note
---

问题：DeepSeek 是什么时候在全球出名的？

回答：2025 年 1 月中下旬，由 R1 触发。

时间线：
- **2024 年 12 月** — V3 低调发布（671B MoE，约 37B active）。极客们注意到了 560 万美元训练成本的声明，但尚未引起主流关注。
- **2025 年 1 月 10 日** — DeepSeek 发布了基于 R1 模型的 chatbot app，支持 iOS 和 Android。
- **2025 年 1 月 20 日** — DeepSeek-R1 正式发布——671B open-weight reasoning 模型，附带 technical paper，在多个 benchmarks 上以远低于 API 的价格匹配 OpenAI o1。
- **2025 年 1 月 27 日** — 真正的 "Sputnik moment"：R1 超越 ChatGPT 成为美国 iOS App Store 下载量最高的免费 app，导致 Nvidia 股价下跌 18%。Nvidia 股价暴跌 17%，市值蒸发近 6000 亿美元——这是美股历史上单家公司单日最大损失。
- 同一天，一场大规模 cyberattack 袭击了 DeepSeek 的服务器，迫使 DeepSeek 将新注册限制为中国大陆手机号码、邮箱或 Google 登录。
- **2025 年 1 月底至 2 月** — 禁令接连而来：台湾禁止政府机构使用，德州限制在州设备上使用，NASA/US Navy 出于数据安全担忧发布内部禁令。

真正引发恐慌的并不是模型质量——而是成本声明。值得注意的是，大多数报道中这些数字被混淆了：560 万美元属于 V3 在 2024 年 12 月的训练；R1 的实际训练成本后来在 2025 年 9 月 Reuters 的报道中披露为 294,000 美元。此后：V3.1（2025 年 8 月）合并了 thinking/non-thinking 模式，V4-Pro/V4-Flash 预览版于 2026 年 4 月发布。

如果你想要的是机制层面的解释（MLA、MoE routing、用于 R1 的 RL post-training 的 GRPO），而不是新闻时间线，请说明——那是另一个答案。

参考文献：
- [DeepSeek (chatbot) — Wikipedia](https://en.wikipedia.org/wiki/DeepSeek_(chatbot))
- [DeepSeek | Britannica Money](https://www.britannica.com/money/DeepSeek)
- [DeepSeek History: From Hedge Fund to V4](https://deepseekai.guide/guides/deepseek-history/)