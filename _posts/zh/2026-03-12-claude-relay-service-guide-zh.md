---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 中继服务详解
translated: true
type: note
---

**问题：** pincc.ai 的平台是什么，它做什么？另外，https://github.com/Wei-Shaw/claude-relay-service 的 GitHub 项目是什么？

**回答：**

## pincc.ai — 平台概述

**pincc.ai** 是 **Claude Relay Service (CRS)** 的官方文档和支持网站——这是一个自托管的开源 AI API 中继/代理服务。它**与**医疗 NGO “PINCC”（Preventing Cervical Cancer，预防宫颈癌）**无关**，后者是一个完全独立的组织。

---

## 什么是 Claude Relay Service (CRS)？

CRS 是一个支持多账号管理的自托管 Claude API 中继服务。它旨在解决三大问题：区域限制（用户无法直接访问 Claude Code）、对第三方镜像服务的隐私担忧，以及希望与他人共享 Claude Code Max 订阅成本（成本分摊 / “拼车”）。

简而言之，CRS 充当 AI 客户端与实际 AI API 之间的**中间件代理**。

---

## 它做什么？

Claude Relay Service 是一个多平台的 AI API 中继服务，支持 Claude（Official/Console）、Gemini、OpenAI Responses (Codex)、AWS Bedrock、Azure OpenAI、Droid (Factory.ai)、CCR 等多种账号类型。它提供完整的多账号管理、API Key 认证、代理配置、用户管理、LDAP 认证、Webhook 通知，以及现代化的 Web 管理界面。该服务充当客户端（如 Claude Code、Gemini CLI、Codex、Droid CLI、Cherry Studio 等）与 AI API 之间的中间件，提供认证、限流、监控、定价计算和成本统计。

主要功能包括：

- **统一调度器**：智能地将请求路由到多个账号和平台
- **成本分摊 / “拼车”**：多个用户共享一个 Claude 订阅以分摊成本
- **客户端限制**：控制哪些客户端（通过 User-Agent）可以使用每个 API key
- **使用统计**：跟踪输入/输出 token 并计算每个用户的成本
- **Web 管理 UI**：用于管理账号、密钥和用户的仪表板

---

## GitHub 仓库 (Wei-Shaw/claude-relay-service)

该仓库在 GitHub 上拥有超过 9,200 个星标和 1,400+ 个 fork，显示出强大的社区采用度。截至 2026 年 3 月初的最新版本为 v1.1.292。

**技术栈：** Node.js 18+、Redis、Docker 兼容。

**部署选项**（来自 pincc.ai 文档）：
- 一键脚本安装（`crs` 命令行工具）
- Docker / Docker Compose
- 通过 `git clone` + `npm install` 手动部署

**项目本身的免责声明：** 使用本项目可能违反 Anthropic 的服务条款。作者不对任何账号封禁、服务中断或其他损失负责，并声明该项目仅用于技术学习和研究目的。

---

## 总结

| 项目 | 详情 |
|---|---|
| **平台** | pincc.ai — Claude Relay Service 的文档/门户 |
| **核心功能** | 自托管 AI API 代理/中继 |
| **支持的 AI** | Claude、OpenAI、Gemini、AWS Bedrock、Azure、Droid |
| **主要用例** | 多账号管理 + 成本分摊（“拼车”） |
| **技术** | Node.js + Redis，可通过脚本或 Docker 部署 |
| **风险** | 可能违反 Anthropic ToS — 自行承担风险 |

**参考资料：**

- [pincc.ai 部署指南](https://pincc.ai/en/installation)
- [GitHub: Wei-Shaw/claude-relay-service](https://github.com/Wei-Shaw/claude-relay-service)
- [GitHub README (English)](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)