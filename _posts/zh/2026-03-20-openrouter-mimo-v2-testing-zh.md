---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenRouter 对 MiMo-V2-Pro 的匿名测试
translated: true
type: note
---

**问题：** OpenRouter 为什么匿名测试 MiMo-V2-Pro 模型，以及这是如何实现的？

**回答：**

## The "Hunter Alpha" Mystery — OpenRouter's Anonymous Model Testing

这是一个刚刚在过去几天（2026 年 3 月）展开的迷人故事。以下是完整情况：

---

### What Happened?

一个名为 "Hunter Alpha" 的强大匿名 AI 模型于 2026 年 3 月 11 日出现在 OpenRouter 上，引发了广泛猜测，认为它是 DeepSeek V4。它仅被描述为“stealth model”。

该模型迅速登上 OpenRouter 的使用排行榜，并在 stealth testing 阶段处理了超过 1 万亿 tokens。

随后，小米正式宣布，“Hunter Alpha” 实际上是他们新旗舰模型 **MiMo-V2-Pro** 的早期内部 beta 版本。

---

### Why Did OpenRouter Test It Anonymously?

这是小米故意采用的 **deliberate stealth testing strategy**，而非仅由 OpenRouter 决定。原因如下：

1. **Unbiased real-world validation** — 小米需要 MiMo-V2-Pro 的能力边界和系统鲁棒性通过真实复杂场景中的开发者来验证和优化。通过隐藏名称，用户纯粹基于模型本身的优点进行评估，而不受品牌偏见影响。

2. **Organic stress testing** — 该模型匿名测试后仍登上 agent benchmarks 的榜首，这充分证明了其真实能力。有时，最好的模型无需著名名称即可证明价值——它们只需正常工作即可。

3. **Gathering real developer usage data** — 在 OpenRouter 上以 Hunter Alpha 代号进行早期测试期间，coding tools 的使用占比最高，这表明开发者发现该模型在真实工作流程中实用且可靠。

---

### How OpenRouter Enables This

OpenRouter 是一个 API aggregation platform，允许 AI 提供商列出模型——包括匿名或 "stealth" 模型——供公众测试。MiMo-V2-Pro 是小米的旗舰 foundation model，总参数超过 1T，context length 为 1M，针对 agentic scenarios 深度优化。

您看到的说明——*"All prompts and completions for this model are logged by the provider and may be used to improve the model"*——是早期模型测试的标准做法。这意味着小米正在收集真实使用数据以改进最终发布版本。

---

### What Is MiMo-V2-Pro?

MiMo-V2-Pro 总参数量超过 1 万亿，激活参数 420 亿。其 context window 已扩展至 100 万 tokens，支持超长任务链和复杂工作流程。

MiMo 部门由 Luo Fuli 领导，她是 DeepSeek 突破性模型（尤其是 R1 和 V-series）的核心贡献者。她于 2025 年底加入小米，带来了中国最受尊重的开源实验室的重要架构 DNA。

---

### Summary

简而言之：小米将 OpenRouter 用作 **neutral testing ground**，在真实开发者工作负载下匿名验证 MiMo-V2-Pro，而不受品牌知名度影响。该模型表现如此出色，以至于登上排行榜首位并引发猜测，随后小米才正式认领。

**参考资料：**

- [The Mystery Solved: Hunter Alpha on OpenRouter is Xiaomi MiMo-V2-Pro - DEV Community](https://dev.to/hubert_shelley_32028fa7a7/the-mystery-solved-hunter-alpha-on-openrouter-is-xiaomi-mimo-v2-pro-3dmd)
- [MiMo-V2-Pro Official Page - Xiaomi](https://mimo.xiaomi.com/mimo-v2-pro)
- [Mystery AI Model Is Xiaomi's MiMo-V2, Not DeepSeek V4 - ResultSense](https://www.resultsense.com/news/2026-03-19-xiaomi-mystery-ai-model-hunter-alpha-mimo-v2)
- [MiMo-V2-Pro on OpenRouter](https://openrouter.ai/xiaomi/mimo-v2-pro)
- [Xiaomi Unleashes MiMo-V2 Family - Quasa](https://quasa.io/media/xiaomi-unleashes-mimo-v2-family-trillion-parameter-agent-powerhouse-mimo-v2-pro-ex-hunter-alpha-multimodal-omni-and-expressive-tts-hit-the-scene)
