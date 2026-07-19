---
audio: false
generated: true
image: false
lang: zh
layout: post
title: machines/inkling作为ChatGPT/Gemini的替代方案
translated: true
type: note
---

**问题：Inkling的图像理解能力是否是一个好的替代方案，因为ChatGPT/Gemini的图像分析对中国用户来说不太方便？**

**答案：**

是的，你的测试结果是一个好迹象。有趣的部分不仅仅是“它能看图片”——现在很多模型都能做到这一点。关键在于**可用性 + API可访问性**。

你的流程：

```
image
  ↓
OpenRouter
  ↓
thinkingmachines/inkling
  ↓
视觉推理
  ↓
“solid blue rectangular field...”
```

这意味着你拥有一个可用的多模态管道，无需依赖消费类应用的地区限制。Inkling是一个原生多模态模型，接受图像、文本和音频输入。([Thinking Machines Lab][1])

对于中国用户来说，情况大致如下：

| 模型 | 图像分析访问权限 | 中国可用性 |
| ------------------------ | ---------------- | -------------------------------------------------------------------------- |
| ChatGPT vision | 优秀 | 往往困难，因为ChatGPT服务的可用性/支付/访问可能成为障碍 |
| Gemini vision | 优秀 | Google服务存在类似的访问问题 |
| OpenRouter vision models | 通常更容易 | 基于API，取决于提供商 |
| Inkling | 新颖但有潜力 | 通过OpenRouter对开发者友好 |

([OpenAI Help Center][2])

关键区别：

**ChatGPT/Gemini是以产品为先。**

```
用户
 ↓
ChatGPT应用
 ↓
政策/账户/地区/计费
 ↓
模型
```

**OpenRouter是以基础设施为先。**

```
你的CLI/应用
 ↓
OpenRouter API
 ↓
模型路由
 ↓
视觉模型
```

对于中国开发者来说，第二种架构通常更实用。

Inkling在技术上也很有趣，因为它不仅仅是一个带有独立视觉插件的文本LLM。其模型卡描述了一种多模态架构，其中图像/音频/文本表示在共享的模型空间中进行处理。([Thinking Machines Lab][1])

一个简单的测试矩阵如下：

```bash
# 同一张图片
models=(
  "thinkingmachines/inkling"
  "google/gemini-2.5-pro"
  "openai/gpt-5"
  "qwen/qwen3-vl"
)

for m in "${models[@]}"; do
    ww vision-model test \
       --model "$m" \
       --image test.png
done
```

比较：

1. OCR准确性
2. 图表理解
3. UI截图理解
4. 中文文本识别
5. 幻觉率

对于你的用例（AI CLI工具、代理、编程助手），视觉可用性比基准分数更重要。一个你的代理总能调用的稍弱模型，胜过一个你无法可靠访问的更强模型。

Inkling尤其有趣，因为它重量级开放，并且面向开发者/代理，而不仅仅是聊天。([Reuters][3])

因此你的结论是合理的：

> “Gemini/ChatGPT的图像分析最近对中国用户来说很难用，但OpenRouter + Inkling提供了一个实用的替代方案。”

我想补充一点：Qwen VL系列也值得测试，因为中文OCR/UI理解通常是其强项。对于中国开发者而言，获胜的技术栈可能变成：

```
英文推理：
  GPT / Claude / Gemini / Inkling

中文视觉：
  Qwen-VL

低成本路由：
  OpenRouter
```

参考资料：

* OpenRouter多模态文档 ([OpenRouter][4])
* Inkling模型卡 ([Thinking Machines Lab][1])
* Thinking Machines Inkling发布公告 ([Thinking Machines Lab][5])
* ChatGPT图片输入常见问题 ([OpenAI Help Center][2])

[1]: https://thinkingmachines.ai/model-card/inkling/?utm_source=chatgpt.com "Inkling Model Card - Thinking Machines Lab"
[2]: https://help.openai.com/zh-hans-cn/articles/8400551-chatgpt-%E5%9B%BE%E7%89%87%E8%BE%93%E5%85%A5%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98?utm_source=chatgpt.com "ChatGPT 图像输入常见问题 | OpenAI Help Center"
[3]: https://www.reuters.com/business/ai-startup-thinking-machines-launches-an-open-weight-ai-model-2026-07-15/?utm_source=chatgpt.com "AI startup Thinking Machines launches an open-weight AI model"
[4]: https://openrouter.ai/docs/guides/overview/multimodal/overview?utm_source=chatgpt.com "OpenRouter Multimodal | Complete Documentation | OpenRouter | Documentation"
[5]: https://thinkingmachines.ai/news/introducing-inkling/?utm_source=chatgpt.com "Inkling: Our Open-Weights Model - Thinking Machines Lab"
