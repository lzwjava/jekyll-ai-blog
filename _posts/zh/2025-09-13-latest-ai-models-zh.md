---
audio: false
date: 2025-09-13
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 最新AI模型及其应用
translated: true
type: note
---

以下是我们目前（截至2025年9月中旬）对GPT-5、Gemini 2.5 Pro、GPT-5 mini及其在Copilot/高级模型中的应用情况的总结：

---

## GPT-5（OpenAI）

* **发布时间**：2025年8月7日（[OpenAI][1]）
* **模型特性**：统一架构的大型语言模型，具备更强的推理能力、更低幻觉率，在编程、数学、写作、健康、视觉感知等领域表现提升。包含面向高要求任务的“GPT-5 pro”版本（[OpenAI][1]）
* **推理机制**：具备“快速推理”与“深度推理”双模式，用户可通过选择“GPT-5思考模式”或使用“请深入思考”等提示词触发深度推理（[OpenAI][1]）
* **访问层级与限制**：
  * 所有ChatGPT用户（免费+付费）均可使用（[OpenAI][1]）
  * 免费用户存在使用次数限制，超额后可能自动切换至轻量版“GPT-5 mini”（[OpenAI][1]）
  * 付费用户（Plus/Pro/Team/Enterprise/EDU）享有更高使用额度，Pro用户可调用“GPT-5 pro”（[OpenAI][1]）

---

## Gemini 2.5 Pro（谷歌）

* **发布轨迹**：
  * 实验版于2025年3月25日首次发布（[blog.google][2]）
  * 稳定版于2025年6月17日正式推出（[Google Cloud][3]）
* **核心能力**：Gemini 2.5系列最先进模型，具备百万token上下文窗口、强推理能力、编程支持、多语言处理等特性（[blog.google][2]）

---

## GPT-5 mini

* **定位与发布时间**：GPT-5的轻量化版本，2025年8月中旬在GitHub Copilot进入公开预览阶段（[The GitHub Blog][4]）
* **应用场景**：适用于GitHub Copilot Chat（网页版）、VS Code插件、GitHub移动端（iOS/Android），并出现在用户模型选择列表中（[The GitHub Blog][4]）
* **配额策略**：在GitHub Copilot付费计划中调用GPT-5 mini不消耗“高级请求”额度（[The GitHub Blog][4]）

---

## 在Copilot/高级服务中的集成情况

* **GitHub Copilot**：
  * 所有计划（含免费版）均已支持GPT-5 mini（[The GitHub Blog][4]）
  * 完整版GPT-5仅向付费用户开放（[The GitHub Blog][5]）
  * 用户可根据订阅计划在模型选择器中切换GPT-5/GPT-5 mini等模型（[The GitHub Blog][4]）

* **微软生态集成**：
  * Copilot Studio支持开发者选用GPT-5，系统会自动路由至适合的GPT-5变体（对话型/推理型）（[Microsoft Developer][6]）
  * 高级功能（如强化推理模型）通常需企业级订阅或付费方案（[OpenAI][1]）

---

是否需要进一步了解**性能对比数据**（GPT-5 vs Gemini 2.5 Pro等）或**未来功能传闻**？

[1]: https://openai.com/index/introducing-gpt-5/?utm_source=chatgpt.com "GPT-5发布公告"
[2]: https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/?utm_source=chatgpt.com "Gemini 2.5：谷歌最智能AI模型"
[3]: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions?utm_source=chatgpt.com "模型版本生命周期 | Vertex AI生成式AI"
[4]: https://github.blog/changelog/2025-08-13-gpt-5-mini-now-available-in-github-copilot-in-public-preview/?utm_source=chatgpt.com "GPT-5 mini现已在GitHub Copilot公开预览"
[5]: https://github.blog/changelog/2025-09-09-openai-gpt-5-and-gpt-5-mini-are-now-generally-available-in-github-copilot/?utm_source=chatgpt.com "OpenAI GPT-5与GPT-5 mini全面上线GitHub Copilot"
[6]: https://developer.microsoft.com/blog/gpt-5-for-microsoft-developers?utm_source=chatgpt.com "面向微软开发者的GPT-5"
