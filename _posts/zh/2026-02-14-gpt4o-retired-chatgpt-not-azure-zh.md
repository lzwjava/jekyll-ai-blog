---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: GPT-4o 在 ChatGPT 中退役，而非在 Azure 中
translated: true
type: note
---

Question: 为什么人们无法通过 Copilot、Azure 服务等使用 GPT-4o？

Answer: 

截至 2026 年 2 月 14 日（停用日期的次日），**GPT-4o 已不再在面向消费者的界面（如主要的 ChatGPT App/Web）中提供**，但其在不同平台上的可用性存在显著差异：

### 在 ChatGPT (OpenAI 的消费者产品) 中

- GPT-4o 已于 2026 年 2 月 13 日正式停用，一同停用的还包括 GPT-4.1、GPT-4.1 mini 和 o4-mini 等模型。
- 在标准版的 ChatGPT 对话中，它已不再可选或可用。
- 对于 ChatGPT Business、Enterprise 和 Edu 用户：仅在 Custom GPTs 中保留对 GPT-4o 的有限访问权限，直至 2026 年 4 月 3 日，届时它将在 ChatGPT 的所有版本中完全停用。
- OpenAI 表示，绝大多数使用量已经转移到 GPT-5.2 等新模型，只有约 0.1% 的日活用户仍在选择 GPT-4o。

### 在 Microsoft Copilot 中

- 目前没有直接证据表明 GPT-4o 在 2026 年 2 月 13/14 日被突然从 Copilot 中移除。
- Microsoft Copilot 在历史上曾使用过多种 OpenAI 模型（有时包含 GPT-4o 变体），但它通常运行在定制化或经过 Enterprise-tuned 的版本上。
- 一些报告显示，Microsoft 可能会在某些 Copilot 功能中转向其他供应商（例如 Anthropic 的 Claude），但 GPT-4o 的停用主要影响的是 OpenAI 自己的 ChatGPT UI —— 并不一定立即影响所有的 Copilot 集成。
- 如果 Copilot 在某些模式下使用了集成 ChatGPT 的后端，它可能在同一时间段内过渡到了 GPT-5 家族等新模型。

### 在 Azure OpenAI Service (Enterprise/API 访问) 中

- **GPT-4o 在 Azure OpenAI 中仍然可用**，特别是对于已部署的模型，尤其是较晚的版本。
- 最新的 GPT-4o 版本（例如 2024-11-20）的停用日期为 2026 年 10 月 1 日（此前曾从更早的日期进行过调整）。
- 早期版本（如 2024-05-13 或 2024-08-06）停用时间较早（某些 Standard 部署为 2026 年 3 月 31 日，并会自动升级到新模型）。
- Provisioned/Global Standard/Data Zone 部署允许继续使用，直到特定版本停用为止（最新款 GPT-4o 最晚可使用至 2026 年 10 月）。
- Azure 在 2026 年 2 月没有立即关停 —— 2 月的时间点是针对 ChatGPT 消费者端访问的，而非底层的 Azure API/服务。
- 开发者和企业仍可以通过 Azure OpenAI 部署并使用 GPT-4o 模型，直到 2026 年各自对应的停用窗口期。

### 为什么存在差异且用户反应强烈

停用对消费者端的 ChatGPT 体验打击最大，因为用户可以在那里直接、个人化地接触到 GPT-4o 具有亲和力的个性，且没有企业级的限制。Azure/Copilot 用户（通常是企业或开发者）拥有更可控、特定版本的访问权限和更长的过渡期，因此那里的“损失感”不那么直接。许多情绪化反应源于在免费或 Plus 版 ChatGPT 界面中失去了那个无限制、像同伴一样的版本。

总结：截至 2026 年 2 月 14 日，你**不能**再在标准 ChatGPT 中使用 GPT-4o，但它通过 Azure OpenAI Service **仍然可以访问**（根据版本的不同，时间线可延续至 2026 年底）。Copilot 的可用性取决于 Microsoft 的具体实现，但它并未以同样突然的方式被完全阻断。

References:  

- [OpenAI announcement: Retiring GPT-4o and other models in ChatGPT](https://openai.com/index/retiring-gpt-4o-and-older-models)
- [OpenAI Help Center: Retiring GPT-4o and other ChatGPT models](https://help.openai.com/en/articles/20001051-retiring-gpt-4o-and-other-chatgpt-models)
- [Azure OpenAI model retirements and deprecations](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic)
- [Microsoft Learn discussion on GPT-4o Azure retirement dates](https://learn.microsoft.com/en-us/answers/questions/5770339/azure-openai-gpt40-auto-upgrade-and-retirement)
- [GitHub issue on Azure OpenAI On-Your-Data and GPT-4o retirement](https://github.com/azure/azure-sdk-for-python/issues/44755)