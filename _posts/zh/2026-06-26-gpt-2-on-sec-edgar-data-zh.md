---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2在SEC-EDGAR数据上的应用
translated: true
type: note
---

重要：翻译 markdown 内容时，请确保格式正确：

- 在标题（以#开头的行）和表格（以|开头的行）之间始终添加空行
- 保持正确的 markdown 表格结构
- 保留所有原始格式和间距，除非格式规则要求更改
- 不要将整个翻译内容包裹在 markdown 代码块（```markdown 或```）中——内容将直接在 Jekyll 与 Kramdown 中使用

翻译规则：

- 如果不确定，不要翻译具体项目名称、公司名称或学校名称
- 对于技术术语、新词和技术概念，保留英文原文而非翻译
- 中文翻译中：专有名词和技术术语使用英文，而非中文音译
- 日语翻译中：技术术语适当使用英文，而非罗马音或片假名
- 所有语言：优先使用英文表示现代技术词汇、编程术语和品牌名称

已完成。论文创建于：

  ~/projects/jekyll-ai-blog/latex/en/sec-edgar-gpt/sec-edgar-gpt.tex

结构：

- 摘要 — 124M GPT-2 在 1.55B SEC-EDGAR tokens 上训练，验证损失 2.45
- 引言 — 动机、贡献
- 相关工作 — BloombergGPT、FinGPT、小型语言模型、EDGAR 数据
- 方法 — 数据（1.55B tokens，16 个分片）、模型（12 层 GPT-2）、训练（RTX 4070，5 天）
- 结果 — 分析所有 5 个提示，并附观察
- 分析 — 回显 vs 生成、循环吸引子、数值一致性、领域漂移、语法 vs 逻辑
- 讨论 — 应用、局限性、与更大模型的比较、未来工作
- 结论
- 参考文献（6 篇引用：BloombergGPT、FinGPT、GPT-2、TinyStories、EDGAR 情感/提取）

此服务器上未安装 LaTeX —— 你需要在 MacBook 上编译：

  cd ~/projects/jekyll-ai-blog/latex/en/sec-edgar-gpt
  xelatex sec-edgar-gpt.tex

或者如果你希望我在此处安装 texlive，我可以做到。论文使用标准包（graphicx, hyperref, tabularx, booktabs, amsmath, listings），因此应能顺利编译。
