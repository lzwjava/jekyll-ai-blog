---
audio: false
date: 2025-09-13
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: GitHub Pages要求使用公开代码库
translated: true
type: note
---

没错——如果将 GitHub Pages 仓库设为私有，就会失去免费的 GitHub Pages 托管服务。

GitHub Pages 仅在仓库为**公开**状态时自动运行。若仓库设为私有，`github.io` 站点将无法发布，除非您使用**支持私有仓库 Pages 功能的 GitHub Enterprise 计划**（此为付费功能，不包含在免费版或标准个人账户中）。

因此对于您的个人博客 `username.github.io`：

* **公开仓库** → GitHub Pages 会自动构建并发布至 `https://username.github.io/`
* **私有仓库（免费账户）** → GitHub Pages 功能将被禁用
* **私有仓库（企业版）** → 仍可正常使用，但需组织启用私有仓库的 Pages 功能

需要我为您说明替代方案吗（例如保持主仓库私有，仅将 `_site` 输出目录同步至单独的公开仓库用于发布）？
