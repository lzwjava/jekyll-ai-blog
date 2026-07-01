---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么Kimi和MiniMax称霸中国
translated: true
type: note
---

**问题：** 为什么 Kimi (Moonshot AI) 和 MiniMax 在中国 AI 竞赛中成功并击败了像 01.AI、xAI（中国语境）、Baichuan 和王小川的公司这样的竞争对手？

**回答：**

这是一个关于中国 AI 行业内部竞争动态的绝佳问题。以下是 **Kimi (Moonshot AI)** 和 **MiniMax** 领先于早期“AI 老虎”竞争对手如 Baichuan（王小川）、01.AI（李开复）等的原因的全面分析。

---

## 1. 优越的模型性能与竞争性成本

MiniMax M2 在 SWE-Bench Verified 上达到了 69.4%，与成本高出 10 倍的模型竞争。对于典型的企業工作负载（每月 100M 输入 token + 20M 输出 token），MiniMax M2 的成本仅为 24 美元——不是 240 美元，也不是 2,400 美元。这种极致的成本效率是一个决定性优势。

Moonshot AI 的 Kimi K2 Thinking 在多个基准测试中超越了 OpenAI 的 GPT-5 和 Anthropic 的 Claude Sonnet 4.5。Allen Institute for AI 的 Nathan Lambert 称赞 Kimi K2 Thinking 缩小了开源模型与全球领先闭源系统之间的差距。

---

## 2. 架构创新（MoE）

MiniMax M2 采用 Mixture-of-Experts (MoE) 架构，总参数 2000 亿，但每次前向传播仅激活 100 亿参数，从而以大幅降低的计算成本实现前沿性能。

MiniMax 的 M2 仅需 4×H100 GPUs 即可高效运行，并达到 1,500 tokens/秒——这意味着你的基础设施成本大幅下降。

---

## 3. Token 使用量中的主导市场份额

MiniMax M2.5 在 OpenRouter 上的 token 使用量成为最受欢迎的 AI 模型，累计 4.55 万亿 tokens，Kimi K2.5 排名第二，累计 4.02 万亿 tokens——两者在开发者采用率上远超西方竞争对手。

中国模型在全球最大的 LLM API 聚合平台 OpenRouter 上占据了总 token 量的 61%，MiniMax 和 Kimi 领先群雄。

---

## 4. Kimi 的智能生态系统举措（OpenClaw 策略）

2026 年 2 月 OpenClaw 框架爆火时，Kimi 抢先行动——成为第一个向 OpenClaw 用户提供免费 API 积分的模型提供商。Moonshot 还推出了 Kimi Claw，一键云部署服务，订阅用户每月仅 199 元人民币，为非技术用户消除了设置障碍。仅 OpenClaw 就占 Kimi K2.5 海外消费量的约四分之一。

这种快速的生态系统整合是 Baichuan 和 01.AI 未能执行的。

---

## 5. Kimi 的收入爆炸式增长

Kimi K2.5 推出不到 20 天，其累计收入就已经超过 2025 年全年总收入。海外收入首次超过国内收入。

---

## 6. MiniMax 的全球消费者成功

MiniMax 将早期的 Glow 概念转向 Talkie，这是一款针对海外市场的 AI 伴侣应用。到 2024 年 6 月，Talkie 成为美国第五大下载量免费娱乐应用，并超越 Character.AI，成为下载量第一的 AI 伴侣应用，全球月活跃用户超过 1100 万。

MiniMax 报告称，2025 年年度收入增长超出预期 159%，股价飙升 21%，反映了对低成本开源中国模型的强劲需求，这些模型可与硅谷匹敌。

---

## 7. 为什么其他公司（Baichuan / 01.AI）落后

### Baichuan（王小川）

Baichuan 急剧改变方向。其两名联合创始人辞职创业，这仅在另一位高管离开这家数十亿美元公司数月后发生。Baichuan 大幅转向 **medical AI**，缩小了焦点，放弃了通用 LLM 竞赛。

### 01.AI（李开复）

2024 年 8 月，01.AI 失去副总裁黄文昊，他加入了 ByteDance。

01.AI 开始专注于基于 DeepSeek 的企业级解决方案，而不是构建自己的前沿模型，实际上放弃了成为独立模型领导者的竞赛。

---

## 8. DeepSeek 价格战碾压弱势玩家

到 2024 年 5 月，DeepSeek 以每百万 token 仅 0.14 美元的价格推出 API，引发价格战——比市场价低 5–10 倍。到 2025 年 1 月，中国 LLM 的平均价格较 2024 年 5 月下降 92%。没有优越效率的小公司（如 Baichuan 和 01.AI）无法在这种压缩中生存。

---

## 9. 中国人才池优势造就赢家

一位 AI 行业高管指出，中国深厚的人才池是 Moonshot 和 MiniMax 尽管高端芯片和资金远少于许多美国同行，却能超重拳的原因。

---

## 总结表格

| Company | Outcome | Key Reason |
| --- | --- | --- |
| **Kimi (Moonshot AI)** | 🏆 Winner | Benchmark-beating models, ecosystem moves, revenue explosion |
| **MiniMax** | 🏆 Winner | MoE efficiency, global consumer apps, 159% revenue growth |
| **Baichuan / Wang Xiaochuan** | ❌ Declining | Leadership exodus, pivoted to medical niche |
| **01.AI / Li Kaifu** | ❌ Declining | Key talent left, retreated to enterprise using others' models |
| **DeepSeek** | 🥈 Competitor | Research/infra focus, declining consumer traffic |

简而言之：Kimi 和 MiniMax 获胜是因为它们结合了 **前沿模型质量**、**通过 MoE 架构的成本效率**、**智能生态系统伙伴关系** 和 **全球消费者产品执行**——而像 Baichuan 和 01.AI 这样的竞争对手失去了人才、过早缩小焦点，并无法在残酷的 AI 价格战中生存。

**参考文献：**

- [China's Kimi Sets Record as Fastest Decacorn – China AI Daily](https://thechinaacademy.org/kimi-moonshot-ai-becomes-chinas-fastest-decacorn-as-recent-revenue-surpasses-entire-2025-total-china-ai-daily-february-24-2026/)
- [Beyond DeepSeek: Moonshot and MiniMax step up – Yahoo Finance / SCMP](https://finance.yahoo.com/news/beyond-deepseek-moonshot-minimax-step-093000177.html)
- [MiniMax and Kimi Top Token Usage Rankings – SCMP](https://www.scmp.com/tech/tech-trends/article/3344587/chinas-minimax-moonshot-top-ai-token-use-ranking-ending-year-us-dominance)
- [China's Open-Source AI Revolution: MiniMax M2 and Kimi K2 – Medium](https://medium.com/@saidrassai/chinas-open-source-ai-revolution-why-minimax-m2-and-kimi-k2-thinking-signal-the-end-of-90c684a3cae0)
- [Kimi's 20-Day Revenue Spike – Voice of Context](https://voiceofcontext.substack.com/p/kimis-20-day-revenue-spike-chinas)
- [Baichuan's Big Pivot – The Wire China](https://www.thewirechina.com/2025/03/30/baichuans-big-pivot-baichuan-ai-china/)
- [How DeepSeek Made China Investible Again – Deep Tech Asia](https://www.deeptech.asia/p/how-deepseek-made-china-investible)
- [Zhipu AI and MiniMax: Not China's OpenAI – Recode China AI](https://recodechinaai.substack.com/p/zhipu-ai-and-minimax-just-went-public)
- [MiniMax Shares Soar After 159% Revenue Jump – Bloomberg](https://www.bloomberg.com/news/articles/2026-03-02/china-ai-pioneer-minimax-more-than-doubles-sales-in-hot-market)
