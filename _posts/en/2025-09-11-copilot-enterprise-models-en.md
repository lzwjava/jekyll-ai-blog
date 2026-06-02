---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Copilot Enterprise Model Options Overview
translated: false
type: note
---

You're asking about which model could be used for **Copilot Enterprise**, specifically whether it's GPT-4.1, GPT-4o, or something else. Here's what’s current and relevant as of **September 2025**:

---

### What models are available for Copilot Enterprise?

#### GitHub Copilot Enterprise & Copilot Chat

* **By default**, GitHub Copilot Enterprise (and Copilot Chat) **runs on GPT-4o**, offering faster responses and improved quality. ([Reddit][1])
* More recently, **GPT-4.1** has become available—but administrators must explicitly **enable it via policy** in the Copilot settings. Once enabled, users can choose GPT-4.1 from the model selector in both VS Code and on github.com. ([The GitHub Blog][2])

#### Visual Studio Copilot

* As of **June 2025**, Visual Studio’s Copilot **now uses GPT-4.1 as its default model**, instead of GPT-4o. Microsoft’s tests showed GPT-4.1 delivers **faster responses, higher-quality suggestions, and greater efficiency**. ([Visual Studio Magazine][3], [Microsoft Learn][4])

#### Microsoft 365 Copilot (Office Productivity Tools)

* Microsoft has begun integrating **GPT-5** into the broader Copilot ecosystem—including Microsoft 365 Copilot, GitHub Copilot, Copilot Studio, and more—via a new “**Smart Mode**” that automatically routes tasks to the most suitable model based on need, improving reasoning, context retention, and interaction quality. ([The Verge][5])
* Additionally, Microsoft announced integration of Anthropic’s **Claude Sonnet 4** for advanced tasks such as presentation design and spreadsheet automation, while still using **GPT-5** (alongside remaining GPT-based routes) for other functions. ([New York Post][6])

---

### Summary — Which model is right for **Copilot Enterprise**?

* **GitHub Copilot Enterprise / Copilot Chat**:

  * Default: **GPT-4o**
  * Optional: **GPT-4.1** (if enabled by admin)
* **Visual Studio Copilot**: Default now is **GPT-4.1**
* **Microsoft 365 Copilot**: Leveraging **GPT-5 Smart Mode**, with higher-performance routing and capabilities—and also integrating **Claude Sonnet 4** for selective enterprise tasks.

---

### Quick rundown (without wide tables, per your preference)

* **GPT-4o**: Default in GitHub Copilot Enterprise; known for speed and quality in enterprise chat.
* **GPT-4.1**: More powerful successor—better at code, instruction following, and long contexts. Available in GitHub Copilot if enabled, and now default in Visual Studio Copilot. ([OpenAI][7])
* **GPT-5**: Latest model, integrated into M365 Copilot via Smart Mode across all Copilot platforms for smarter model selection. ([The Verge][5])
* **Claude Sonnet 4**: Added mainly for Office tasks like PowerPoint and Excel automation, alongside GPT-5. ([New York Post][6])

---

### What to do next?

* If you're an **administrator** managing GitHub Copilot Enterprise, check your settings to **enable GPT-4.1** if you want users to leverage its performance improvements.
* If you're using **Visual Studio Copilot**, you're already on **GPT-4.1** by default.
* For **Microsoft 365 Copilot**, you’ll benefit from the **GPT-5 Smart Mode** rollout and **Claude Sonnet 4** integrations. No action needed—it’s already part of the service layers.

Let me know if you'd like help configuring these settings or navigating model options in your organization's specific environment!

[1]: https://www.reddit.com/r/GithubCopilot/comments/1dx2iq1/github_copilot_enterprise_on_gpt4o/?utm_source=chatgpt.com "GitHub Copilot Enterprise on GPT-4o : r/GithubCopilot"
[2]: https://github.blog/changelog/2025-04-14-openai-gpt-4-1-now-available-in-public-preview-for-github-copilot-and-github-models/?utm_source=chatgpt.com "OpenAI GPT-4.1 now available in public preview for GitHub ..."
[3]: https://visualstudiomagazine.com/articles/2025/06/26/new-default-model-for-visual-studio-copilot-so-how-do-you-choose.aspx?utm_source=chatgpt.com "New Default Model for Visual Studio Copilot, So How Do ..."
[4]: https://learn.microsoft.com/en-us/visualstudio/ide/copilot-select-add-models?view=vs-2022&utm_source=chatgpt.com "Using AI models in Copilot Chat - Visual Studio (Windows)"
[5]: https://www.theverge.com/news/753984/microsoft-copilot-gpt-5-model-update?utm_source=chatgpt.com "Microsoft brings GPT-5 to Copilot with new smart mode"
[6]: https://nypost.com/2025/09/10/business/microsoft-to-add-anthropic-ai-models-as-rift-with-openai-grows-report/?utm_source=chatgpt.com "Microsoft to add Anthropic AI models - as rift with OpenAI grows: report"
[7]: https://openai.com/index/gpt-4-1/?utm_source=chatgpt.com "Introducing GPT-4.1 in the API"
