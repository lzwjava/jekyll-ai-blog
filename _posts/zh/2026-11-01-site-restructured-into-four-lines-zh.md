---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 站点重组为四线
translated: true
type: note
---

完成。以下是变更内容——网站现在更名为 **truth-software**，围绕你的四条业务线重新组织，并将 truth-lab 的内容整合其中。

## 新页面结构（单个 `index.html`）

| 部分 | 内容 |
| --- | --- |
| **#lines** (new) | 四条业务线的概览网格 |
| **#ml** — 业务线 01 · 模型训练与推理 (new) | 从头预训练（GPT-2 124M/760M），LoRA/SFT/RLHF，vLLM/SGLang/llama.cpp serving，GPU 工作站，数据处理管道，公开证据（SEC-EDGAR-GPT，benchmarks） |
| **#ai-transform** — 业务线 02 · AI 转型咨询 | 保留，重新启动 |
| **#ai-services** — 业务线 03 · AI 应用与智能体开发 | 保留（工作站/训练卡片已移至业务线 01） |
| **#services** — 业务线 04 · 一般应用开发 | 正是你列出的 4 项：iOS/Android、微信小程序、Web 平台与后台系统、H5 营销与增长活动 |
| **#lab** (new, from truth-lab) | Truth Lab 介绍 + 宣言引用、统计数据、6 个实验、13 次训练表、硬件规格、GitHub 链接 |
| **#team** (new) | 创始人成长历程时间线 *从 NOIP 到 nanoGPT*（8 条） |

## 其他

- Hero/meta/title/nav/footer 已围绕四条业务线重写；nav 现在为：关于 · 业务线 · 训练与推理 · AI 转型 · AI 应用 · 应用开发 · 案例 · 实验室 · 团队 · 计价 · 联系
- 在 `i18n.js` 中新增了约 130 个英文字符串（保留了最长键优先机制），并修复了几个**先前未翻译**的作品卡片（SEC-EDGAR GPT、趣直播）
- 在 `style.css` 中为 lines/lab-table/quote/timeline 添加了新 CSS（浅色 + 深色主题）
- 重新运行了 `scripts/build_cases.py`——案例页面/作品集未变，CI 检查可通过
- 提交为 `c66f342`；已验证 HTML 平衡性、i18n 覆盖率和本地服务（首页 + 作品集 + 案例均返回 200）

**未完成（由你决定）：** 我没有 **push**（你的 CI 在 push 时部署）也没有 **改动** `truth-lab` 仓库——它的内容现已位于此处，因此你可能需要废弃 `truth-lab`（本地目录 + GitHub 仓库）并将 truthlab.cc 重定向。只要你一句话，我就 push 和/或清理。
