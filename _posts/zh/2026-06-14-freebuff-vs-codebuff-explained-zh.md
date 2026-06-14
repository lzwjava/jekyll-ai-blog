---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Freebuff vs Codebuff 详解
translated: true
type: note
---

**问题：** freebuff.ai 与 Codebuff 之间是什么关系？

**回答：**

**Freebuff 是 Codebuff 的免费广告支持版**——同一家公司，同一套代码库，只是盈利模式不同。

完整情况如下：

**Codebuff**（`codebuff.com`）是一个由 [CodebuffAI](https://github.com/CodebuffAI/codebuff) 构建的付费终端编码代理。它支持 OpenRouter 上的任何模型（Claude、GPT、DeepSeek、Qwen 等），并使用 TypeScript 生成器实现自定义代理工作流，代理可以生成子代理、根据条件分支并运行多步骤流程。定价从每月 49 美元起，最高至每月 249 美元。

**Freebuff**（`freebuff.com` / `npm i -g freebuff`）是 Codebuff 的免费变体——无需订阅、无需积分、无需配置。它通过 CLI 中显示的广告来支持运营，声称比 Claude 快 3–5 倍的 token 处理速度，并内置了网络搜索和浏览器使用功能。

关于 Freebuff 的关键技术细节：
- 默认模型为 DeepSeek V4 Pro（最智能，但其 API 会收集数据用于训练）或 DeepSeek V4 Flash 作为主要编码代理。
- 支持 `@filename` 引用文件、`@AgentName` 调用专门代理、`!command` 或 `/bash` 执行终端命令，以及 `knowledge.md` 提供项目级上下文。
- 使用 GitHub OAuth 进行用户身份验证并管理每日使用配额。

**创始人背景：** 由 James Grugett 创立，他曾创办 Manifold Markets（15 万用户，月访问量数百万）。其策略是使用最佳开源模型完全免费提供消费级代理产品，通过广告盈利——Freebuff 作为入门产品，Codebuff 作为付费升级版。

**对你的工作流程的简要总结：** Freebuff = Claude Code 的竞争对手，免费、基于 DeepSeek、广告支持的 CLI 代理。既然你已经深入使用 DeepSeek V4 Flash/Pro，值得一试。需要注意的是，DeepSeek V4 Pro 的数据训练条款在你运行银行代码时可能需留意。

**参考：**
- [CodebuffAI/codebuff GitHub](https://github.com/CodebuffAI/codebuff)
- [freebuff README](https://github.com/CodebuffAI/codebuff/blob/main/freebuff/README.md)
- [freebuff on npm](https://www.npmjs.com/package/freebuff)
- [Freebuff on YC](https://www.ycombinator.com/companies/freebuff)