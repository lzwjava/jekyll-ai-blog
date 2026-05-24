---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp AI默认模型配置
translated: true
type: note
---

**问题：** 当未配置任何模型时，Warp 默认使用什么 AI 模型？  
**回答：**  

Warp 内置的 AI（品牌名称为 **"Warp AI"**）将查询路由至 **Warp 自己的服务器**，因此你无需自行配置 API 密钥——它们负责处理模型后端。  

截至 2026 年，Warp AI 由 **Oz**（Warp 的编排层）集成 OpenAI 模型驱动。它支持前沿模型，包括 Claude Opus 4.5、GPT-5.2 和 Gemini 3 Pro，付费计划中可自带 API 密钥。  

因此，在未配置任何设置的情况下，默认使用的是 **Warp 托管的后端（Oz + OpenAI）**——具体模型取决于你的套餐等级，免费用户将使用 Warp 选择的默认模型。你可以在 Warp 的 `Settings → AI` 中查看当前账户激活的具体模型。  

注意：默认情况下，查询会经过 Warp 的服务器，在处理敏感信息（如银行工作等）时需留意这一点。