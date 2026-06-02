---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClacky Keys 适用于 Claude、DeepSeek 和 Gemini
translated: true
type: note
---

对，基本正确。一些改进点：

**正确**
- `providers.rb:28-76` 定义了 OpenClacky 预设：`base_url: https://api.openclacky.com`，在 `https://www.openclacky.com/ai-keys` 获取密钥。
- 完整的 Claude 系列已预设并可在模型下拉菜单中选择：`abs-claude-opus-4-7 / 4-6`、`abs-claude-sonnet-4-6 / 4-5`、`abs-claude-haiku-4-5`。
- 域名在中国大陆可直连——无需代理或 VPN。

**值得补充**
- 同一密钥也涵盖非 Claude 模型：`dsk-deepseek-v4-pro / flash`（DeepSeek，纯文本）和 `or-gemini-3-1-pro`（Gemini 3.1 Pro，多模态）。因此“自由切换”不仅限于 Claude 系列——一个密钥即可覆盖 Claude + DeepSeek + Gemini。
- `api` 字段为 `"bedrock"`（非 OpenAI 或 Anthropic 的 shim），意味着请求遵循 Bedrock 协议格式。通常透明无感，但如果通过自定义代理前置使用则需注意。
- 与 OpenRouter（上次分析中带有 `models: []` 和“动态 - 从 API 获取”注释的那个）不同，OpenClacky 自带一个固定的 7 个模型静态列表——无需动态获取。

因此更精准的表述是：“OpenClacky aikeys——一个密钥，在 Claude / DeepSeek / Gemini 之间自由切换，中国大陆直连，无需特殊网络。”
