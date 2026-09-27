---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Laya: 多语言非自回归决策模型'
translated: true
type: note
---

问题：Hugging Face 上的 "laya" 模型 (convaiinnovations/laya) 是什么？

答案：Laya 是一个多语言、非自回归的 "System 1" decision model，它接收 state（文本、邮件、工单或 JSON）以及 typed questions，并在单次 forward pass（约 33 ms）中返回带 calibrated probabilities 的 typed answers，覆盖 100+ 种语言。它从不生成自由文本，所以不存在 hallucination——它面向 classification/routing/scoring/guardrail-type 任务，而不是开放式生成。

关键细节：
- **架构**：英文 checkpoint（本仓库根目录）是一个 ModernBERT-large backbone（395M 参数）完全微调，加上一个从零训练的 decision head，总参数 421M，context 为 512 tokens。多语言变体使用 mmBERT-base backbone（322M 参数，最大 8k context），第三个 checkpoint 专门针对 "typed-decisions" workflows 进行了微调。
- **训练方法**：作者称之为 RLCD（Reinforcement Learning for Calibrated Decisions）——模型针对 strictly proper scoring rules 进行训练，使得报告诚实概率成为 reward-maximizing 策略。
- **许可证**：Apache 2.0（开放权重，允许商用）。
- **定位**：模型卡片明确将其与一个名为 "TypeSafe Jev" 的封闭系统进行比较，声称延迟低得多（32.8 ms vs. 236–276 ms p50），并在多个基准上准确率更高，同时指出 Jev 在非常高基数分类（>20 个标签选项）上仍然领先。
- **坦诚的局限**（作者所述）：基础 checkpoints 在它们自己的 "typed-decisions" benchmark 上 zero-shot 表现接近随机——0.766 的高准确率数字来自在该 benchmark 的 training split 上微调的 checkpoint，而不是原始模型；在 temperature calibration 之前，得分也存在过度自信。
- 通过 `pip install laya` 安装；有 GitHub repo、PyPI package 和在线 HF Space demo。

简言之：这是一个小型、快速、开源的 encoder-based classifier/decision model（不是文本生成器），面向 routing、moderation 和 scoring 等结构化决策任务——定位为封闭 "Jev" 系统的更快、更便宜、开放替代品。

参考：
- [convaiinnovations/laya on Hugging Face](https://huggingface.co/convaiinnovations/laya)
- [Laya GitHub repository](https://github.com/NandhaKishorM/laya)
- [Laya on PyPI](https://pypi.org/project/laya/)