---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Novita AI 受欢迎程度解析
translated: true
type: note
---

问题：作为 Hugging Face 登录/推理合作伙伴出现的推理提供商 Novita AI（novita.ai）有多受欢迎？

回答：

让我先查找当前数据，而不是猜测。Novita AI 目前是 HF 生态系统中较受欢迎的无服务器推理提供商之一，绝非小众选择。

你看到的“登录/集成”实际上是 HF 的 **Inference Providers** 路由层。Novita 已注册为提供商，因此当你使用 `HF_TOKEN` 访问 `https://router.huggingface.co/v1` 时，HF 可以将你的请求路由到 Novita 的后端。你可以通过两种模式运行——HF 路由模式（HF 向你收费，PRO 用户每月获得 2 美元额度）或自定义密钥模式（你添加 Novita API 密钥，直接通过你的 Novita Studio 账户计费）。这种双计费设置正是你觉得新颖的地方。

关于受欢迎程度：

- 它于 2026 年 4 月成为 **HF 官方推理合作伙伴**，服务于超过 500 万 HF 开发者社区，并且是 Gemma 4 的发布日合作伙伴。Novita AI 和 Hugging Face 宣布建立战略合作伙伴关系，为 Hugging Face 上的超过 500 万开发者提供最新 AI 模型的实惠、可靠推理，同时 Novita 也是 Gemma 4 的发布日合作伙伴。
- 其应用范围已超越 HF——Novita AI 受到 AI 生态系统中领先团队的信任，包括 Hugging Face、Quora、OpenRouter、Vercel、Kilo Code 和 Genspark。因此，你可能已经通过 OpenRouter 间接路由到了它。
- 规模：该平台通过单一的 OpenAI 兼容和 Anthropic 兼容 API 覆盖了 120 多个大语言模型，并在每个新模型发布当天即可使用。
- 基准测试在一定程度上支持了这些宣传——在 Artificial Analysis 的 GPT-OSS-120B 提供商基准测试中（2026 年 4 月），Novita 在 GPQA Diamond 上以 79.0% 排名第一，在 AIME 2025 上达到 93.3%，在 IFBench 上以 68.9% 排名第五。

对你来说实际的角度：它是 Together AI / Fireworks / Groq 的真正竞争对手，定位在成本（声称便宜高达 50%）和模型发布日可用性上。既然你已经通过 OpenRouter 消耗了约 20 亿 token，一个有趣的做法是将 Novita 的直接端点与你当前最常用开放模型（DeepSeek V4、Qwen、GLM）的路由进行 A/B 测试——OpenAI 兼容 API 意味着只需一行 `base_url` 替换：

```python
from openai import OpenAI
client = OpenAI(base_url="https://api.novita.ai/v3/openai", api_key="<API_KEY>")
r = client.chat.completions.create(model="deepseek/deepseek-v4-pro", messages=[{"role":"user","content":"ping"}])
```

或者保持在 HF 路由内部，通过在模型 ID 后添加 `:novita`（例如 `deepseek-ai/DeepSeek-V4-Pro:novita`）。

关于受欢迎程度的一个说明：上述最强的描述大多来自 Novita 自己的公关和自行委托的基准测试，因此请将“#1”和“最佳性能”等说法视为供应商自身的宣传。信任信号（HF、OpenRouter、Vercel 的采用）是更中立的证据，表明它确实被广泛使用。

参考来源：

- [Novita AI 加入 Hugging Face 成为官方推理合作伙伴](https://www.prnewswire.com/news-releases/novita-ai-joins-hugging-face-as-official-inference-partner-302741097.html)
- [Novita AI 被评为最佳性能且可靠的推理层](https://www.morningstar.com/news/pr-newswire/20260421sf38721/novita-ai-ranked-as-the-best-performing-reliable-inference-layer)
- [HF Inference Providers — Novita 文档](https://huggingface.co/docs/inference-providers/providers/novita)