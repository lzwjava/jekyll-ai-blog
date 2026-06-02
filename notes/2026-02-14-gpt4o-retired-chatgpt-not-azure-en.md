---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: GPT-4o Retired in ChatGPT Not Azure
translated: false
type: note
---

Question: Why can't people use GPT-4o through Copilot, Azure services, etc.?

Answer:

As of February 14, 2026 (the day after the retirement date), **GPT-4o is no longer available in consumer-facing interfaces** like the main ChatGPT app/web, but its availability differs significantly across platforms:

### In ChatGPT (OpenAI's consumer product)

- GPT-4o was fully retired on February 13, 2026, along with models like GPT-4.1, GPT-4.1 mini, and o4-mini.
- It is no longer selectable or usable in standard ChatGPT conversations.
- For ChatGPT Business, Enterprise, and Edu users: Limited access to GPT-4o remains only within Custom GPTs until April 3, 2026, after which it is fully retired everywhere in ChatGPT.
- OpenAI stated that the vast majority of usage had already shifted to newer models like GPT-5.2, with only ~0.1% of daily users still selecting GPT-4o.

### In Microsoft Copilot

- There is no direct evidence of GPT-4o being abruptly removed from Copilot on February 13/14, 2026.
- Microsoft Copilot has historically used various OpenAI models (including GPT-4o variants at times), but it often runs on customized or enterprise-tuned versions.
- Some reports suggest Microsoft may be shifting or hedging toward other providers (e.g., Anthropic's Claude) in certain Copilot features, but GPT-4o retirement primarily affected OpenAI's own ChatGPT UI — not necessarily all Copilot integrations immediately.
- If Copilot was using a ChatGPT-integrated backend for certain modes, it likely transitioned to newer models like GPT-5 family around the same time.

### In Azure OpenAI Service (enterprise/API access)

- **GPT-4o remains available** through Azure OpenAI for deployed models, especially later versions.
- The latest GPT-4o version (e.g., 2024-11-20) has a retirement date of October 1, 2026 (previously adjusted from earlier dates).
- Earlier versions (e.g., 2024-05-13 or 2024-08-06) retired earlier (March 31, 2026 for some Standard deployments, with auto-upgrades to newer models).
- Provisioned/Global Standard/Data Zone deployments allow continued use until the specific version's retirement (up to October 2026 for the newest GPT-4o).
- No immediate February 2026 shutdown for Azure — the February date was specific to ChatGPT consumer access, not the underlying Azure API/service.
- Developers/enterprises can still deploy and use GPT-4o models via Azure OpenAI until their respective retirement windows in 2026.

### Why the difference and strong feelings persist

The retirement hit hardest in the consumer ChatGPT experience, where users had direct, personal access to GPT-4o's warm personality without enterprise guardrails. Azure/Copilot users (often businesses or developers) have more controlled, version-specific access and longer transition periods, so the "loss" feels less immediate there. Many emotional reactions stem from losing the unrestricted, companion-like version in the free/Plus ChatGPT interface.

In summary: You **cannot** use GPT-4o anymore in standard ChatGPT as of February 14, 2026, but it is **still accessible** via Azure OpenAI Service (with version-dependent timelines into late 2026). Copilot availability depends on Microsoft's specific implementation, but it was not fully blocked in the same abrupt way.

References:

- [OpenAI announcement: Retiring GPT-4o and other models in ChatGPT](https://openai.com/index/retiring-gpt-4o-and-older-models)
- [OpenAI Help Center: Retiring GPT-4o and other ChatGPT models](https://help.openai.com/en/articles/20001051-retiring-gpt-4o-and-other-chatgpt-models)
- [Azure OpenAI model retirements and deprecations](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic)
- [Microsoft Learn discussion on GPT-4o Azure retirement dates](https://learn.microsoft.com/en-us/answers/questions/5770339/azure-openai-gpt40-auto-upgrade-and-retirement)
- [GitHub issue on Azure OpenAI On-Your-Data and GPT-4o retirement](https://github.com/azure/azure-sdk-for-python/issues/44755)
