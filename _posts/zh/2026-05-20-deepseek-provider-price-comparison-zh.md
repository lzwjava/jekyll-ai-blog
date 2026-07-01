---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek 提供商价格对比
translated: true
type: note
---

说得好。我引用的价格（输入 $1.74 / 输出 $3.48）来自搜索结果，很可能反映的是 DeepSeek 在 platform.deepseek.com 上的**官方 API** 定价。

OpenRouter 的价格之所以不同，是因为 **OpenRouter 是一个转售商/聚合平台**——它们会路由到多个提供商，其定价反映了自身的利润空间以及所路由到的提供商。有时 OpenRouter 比官方 API 便宜，有时更贵，具体取决于最终路由到的后端提供商。

在这个案例中：

| 来源 | 输入（$/百万token） | 输出（$/百万token） |
| --- | --- | --- |
| DeepSeek 官方 API | $1.74 | $3.48 |
| OpenRouter | $0.435 | $0.87 |

对于 V4 Pro，OpenRouter 实际上比 DeepSeek 自己的 API **便宜 4 倍**。这可能是因为 OpenRouter 路由到了其他提供商（例如 Fireworks、Together、Nebius），这些提供商自行运行开源权重，并在价格上相互竞争。

这就是 OpenRouter 对于开源权重模型的价值主张——MIT 许可证意味着任何人都可以托管该模型，而提供商之间的竞争会显著降低价格，使其远低于实验室自身的 API 价格。

因此，针对你的路由决策，修正后的实际价格为：OpenRouter 上 V4 Pro **输入 $0.435/M，输出 $0.87/M**，V4 Flash 则为 **输入 $0.112/M，输出 $0.224/M**。这使得 V4 Flash 在高频 agent 循环中更加划算。
