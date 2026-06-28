---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek 杀线代币经济学
translated: true
type: note
---

我看不到页面内容——让我去获取它。**问题：** ZenMux 的《Token 经济学》博客文章讲了什么？

**回答：**

这是 ZenMux（模型聚合平台）的一篇研究文章，其核心论点是：LLM 市场的真实信号并非基准测试或发布会演讲，而是开发者实际花费 token 的地方。中心概念是 **"DeepSeek 杀线"**。

**核心论点**

当 DeepSeek V4 Pro 推出时，它在 ZenMux 上的使用量增长足够快，一度在调用量上与 Claude Opus 4.8 持平甚至超越。他们将此归因于真正的模型质量 *以及* 激进的定价加上业界最佳的缓存命中表现。"杀线"指的是：一旦某个模型提供可接受的性能 + 极低的价格 + 稳定的生产环境访问，它就会在开发者心中成为 **新的价格锚点**，迫使其他所有模型证明其溢价合理性。

**方法论**（对你来说有趣的部分）

他们将所有因素简化为两个可观测变量——价格和使用量——并定义了一个 `Value` 指标：

1. **NormalizedUsage** = `模型发布后前 14 个工作日内的活跃工作日日均 token 数中位数`。使用中位数（而非平均数）以避免发布日峰值导致偏差；14 天窗口用于标准化不同时间发布的模型。

2. **NormalizedPrice** = `0.1 × InputPrice + 0.001 × OutputPrice`（每百万 token 的美元价格）。权重来源于对真实编码工作流的测量——Claude Opus 4.8 在 Claude Code 中和 GPT-5.5 在 Codex 中都显示出约 **100:1 的输入输出 token 比例**。因此"标准篮子"是 100K 输入 + 1K 输出 token，这大大放大了输入价格（实际上主导了代理/编码账单的因素）。

3. **Value** = `NormalizedUsage / NormalizedPrice` → 每（美元·天）的 token 数。明确 *不是* "最便宜者获胜"的指标——没人用的便宜模型得分低；真实使用量很大的昂贵模型（Claude Opus）得分高。

**研究发现**

- **DeepSeek V4 Pro = 价值排名第一**，毫无悬念——与 V4 Flash 同处于"低价、高使用量"象限。
- **GLM 5.2** 是惊喜——进入全球顶级梯队，值得注意的是它 *不再是地板价* 了。文章将其描述为第一个打破"廉价替代品"叙事、进入真正旗舰定位的中国模型。
- **Claude Opus 4.8/4.7/4.6** 在"高价格、高使用量"象限中保持强势——证明了如果能力/稳定性/信任度足够高，昂贵的模型不会被抛弃。Anthropic = 高端玩法，市场愿意买单。
- **OpenAI** 覆盖所有领域，但便宜的 GPT 模型（Nano 级别）*并未*转化为使用量；昂贵的旗舰模型（GPT-5.4/5.5）则偏向高端象限。注意：他们观察到的 GPT 使用量被低估了，因为 Codex/ChatGPT 订阅将调用从 API 转移走了。
- **Gemini 3.5 Flash** 正在 *向上移动市场*——即使是"廉价"旗舰模型在提价方面也变得更加自信。

**实验**

他们正在进行一个实时的 **"DeepSeek 杀线挑战"**：人为地将大约 20 个东方模型（GLM、Kimi、Qwen3.7 Max、MiniMax M3、MiMo-V2.5/Pro、Doubao Seed 2.1、ERNIE 5.1、KAT-Coder 等）的价格折扣到与 DeepSeek V4 Pro/Flash 相同的水平——将价格作为变量"拉平"，以观察哪些模型能保持真实使用量。部分折扣幅度很大（Qwen3.7 Max 折扣 82.8%，GLM 5.2 折扣 69.3%）。

**结论：** "价格是提供商贴在模型上的标签，使用量是用户用金钱投出的选票。"存在三条战略路径——Claude 的高端路径、DeepSeek 的杀线路径，或者 GLM 5.2 的"打破廉价替代品地位"路径。

**他们指出的注意事项：** 并非全球市场份额（仅基于 ZenMux 数据），缓存命中率尚未建模（对真实有效成本而言是一个重大遗漏），以及提供商的产品策略（Codex 配额）会扭曲观察到的使用量。

与你的技术栈相关——你已经在使用 deepseek-v4-flash/pro 和 mimo-2.5-pro，所以这基本上是对你模型选择直觉的数据支撑。排行榜在 `arena.zenmux.ai/token-economics?view=live` 实时展示，仓库是开源的。

**参考资料：**

- [Token Economics: What Happens When We Price Every "Eastern Model" to Match DeepSeek? — ZenMux](https://zenmux.ai/blog/token-economics)
- [zenmux-arena（开源仓库）](https://github.com/ZenMux/zenmux-arena)
