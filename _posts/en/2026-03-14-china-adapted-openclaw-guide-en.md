---
audio: false
generated: true
image: false
lang: en
layout: post
title: China Adapted OpenClaw Setup Guide
translated: false
type: note
---

Question: What version/configuration of OpenClaw do Xianyu technicians install for Chinese users — specifically regarding GFW restrictions, Chinese messaging platforms (Feishu, DingTalk, etc.), and which AI models are used instead of Western ones?

Answer:

## What Chinese Technicians Actually Set Up on Xianyu

This is actually a very layered setup, because vanilla OpenClaw assumes Western services (Telegram, Slack, OpenAI API) that are all blocked behind the GFW. Technicians have to adapt it in multiple ways.

---

### 1. Which Version / Fork Is Installed?

There are two main routes:

**Option A — Official OpenClaw + Chinese Community Plugins**

The official upstream OpenClaw is installed, but supplemented with the **`openclaw-china`** plugin package, which is a community-maintained meta-package. Multiple community forks have been created to provide optimized experiences for Chinese users — including `openclaw-cn` by jiulingyun (with built-in Feishu integration and domestic network environment optimization to address GFW connectivity issues), `openclaw-cn` by AI-ZiMo (regularly synced with upstream), and OpenClaw CN on SourceForge (focused on making the framework usable for Chinese-speaking developers). These forks handle the practical realities of running OpenClaw in China: network routing, API endpoint selection, default model configuration, and UI localization.

**Option B — One-Click Chinese Corporate Distributions**

Bigger tech companies have released their own flavors that are essentially pre-configured OpenClaw out of the box:

- **AutoClaw** by Zhipu AI — billed as the first "one-click install" local version in China, with more than 50 pre-installed skills, and recommends integration with GLM, DeepSeek, Kimi, and other Chinese models.
- **ArkClaw** by ByteDance's Volcano Engine — a cloud SaaS version usable directly via web browser, with deep Feishu and DingTalk integration, 24/7 always-on cloud operation.
- **QClaw** by Tencent — connects to WeChat and QQ, takes about 3 minutes to install, and allows users to remotely control their laptop by sending a command via WeChat on the phone.

Technicians on Xianyu may install any of these depending on the customer's needs and which messaging platform they use.

---

### 2. Messaging Channels: Replacing Telegram/Slack

Since Telegram and Slack are blocked in China, technicians configure Chinese alternatives. The `openclaw-china` plugin package supports DingTalk (钉钉), Feishu (飞书), QQ Bot, WeCom (企业微信 — WeChat Work), and WeCom App as channels.

Here's how each is configured:

- **Feishu (Lark):** The official `feishu-bridge` skill connects via WebSocket long-connection — no public server, domain, or ngrok required. It works behind NAT and firewalls because it initiates an outbound connection from your OpenClaw instance to Feishu's servers. This is considered the easiest and most reliable option for China.
- **DingTalk:** Alibaba released a comprehensive guide for integrating OpenClaw with DingTalk, even offering unlimited API calls until March 31.
- **WeCom / QQ:** Tencent's WorkBuddy allows remote configuration via WeCom in as little as one minute, while also integrating with QQ and DingTalk.

For China-based users, Feishu (Lark) is generally the recommended channel — solid API, stable messaging, and generous free tier. WeChat Work, DingTalk, and QQ are also supported, just a bit more complex to configure.

---

### 3. AI Models: Replacing OpenAI

Since OpenAI's API is also GFW-restricted and requires overseas payment methods, technicians configure domestic Chinese LLMs instead. The most common choices:

| Model | Provider | Notes |
|---|---|---|
| **Qwen (通义千问)** | Alibaba | Most popular default; setup wizard can auto-authorize |
| **DeepSeek** | DeepSeek | Extremely popular, very cheap API |
| **Kimi K2.5** | Moonshot AI | Strong reasoning, used in KimiClaw hosted version |
| **GLM-5** | Zhipu AI | Built into AutoClaw |
| **Doubao** | ByteDance | Used in ArkClaw |
| **MiniMax M2.5** | MiniMax | Supports voice/music generation too |

OpenClaw officially expanded support for Chinese LLMs like Zhipu AI's GLM-5 and MiniMax M2.5, meaning users can connect these models to their OpenClaw installation, essentially giving the AI agent a new brain using a Chinese provider.

The quickest onboarding path recommended in Chinese tutorials is to pick Qwen — it automatically redirects to Qwen's login page for authorization, with no API key needed. This is described as the easiest path for anyone who wants to start immediately.

**OpenRouter** is generally not used in China-facing setups, as it primarily aggregates Western API providers (OpenAI, Anthropic, etc.) that require overseas access.

---

### 4. Cloud vs Local Installs

For users who need 24/7 uptime (to run scheduled tasks while their PC is off), technicians may deploy OpenClaw on a domestic cloud server. Options include Alibaba Cloud ECS (with native Qwen/DingTalk integration), Tencent Cloud (optimized for WeChat/WeCom API calls with very low latency), and VolcEngine (ByteDance's platform).

However, cloud-hosted servers located within mainland China cannot access overseas services like Google or Telegram. For cross-border skills execution or overseas IP requirements, users must use local execution or purchase overseas cloud servers instead.

---

### Summary Flow of a Typical Xianyu Installation

1. **Install** the official OpenClaw CLI (or AutoClaw/ArkClaw Chinese fork)
2. **Configure a Chinese LLM** — usually DeepSeek or Qwen API key
3. **Configure a messaging channel** — usually Feishu or DingTalk (replacing Telegram)
4. **Install skill packs** — e.g., web search, calendar, file management
5. **Test and hand over** — the user can now send messages on Feishu/DingTalk to their AI agent

References:

- [GitHub: BytePioneer-AI/openclaw-china — Chinese Plugin Package](https://github.com/BytePioneer-AI/openclaw-china)
- [OpenClaw Blog: Beyond OpenAI — Chinese LLMs Powering OpenClaw Agents](https://openclaws.io/blog/openclaw-chinese-llm-integrations/)
- [TechFlow: 2026 Hundred Shrimp Battle — OpenClaw Optimized for Chinese Users](https://www.techflowpost.com/en-US/article/30654)
- [SCMP: Chinese Tech Giants Offer Cheap Easy Access to OpenClaw](https://www.scmp.com/tech/article/3346090/chinese-tech-giants-offer-cheap-easy-access-openclaw-amid-lobster-fever)
- [Yicai: Zhipu, ByteDance, Tencent Launch OpenClaw Versions](https://www.yicaiglobal.com/news/zhipu-ai-bytedance-tencent-10-other-chinese-internet-giants-launch-openclaw-versions)
- [StableLearn: OpenClaw Installation Guide for Mac and Windows](https://stable-learn.com/en/openclaw-installation-tutorial/)
- [Trending Topics EU: OpenClaw Expands Support of Chinese AI Models](https://www.trendingtopics.eu/openclaw-expands-support-of-chinese-ai-models-amid-big-tech-interest/)