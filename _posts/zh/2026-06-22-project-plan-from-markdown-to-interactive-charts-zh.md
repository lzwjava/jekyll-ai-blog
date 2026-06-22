---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 项目计划：从Markdown到交互式图表
translated: true
type: note
---

很好！那么计划很明确了：

- 等待几天让代码模型完成训练
- 本周将博客从 markdown 转换为带图表/可视化的交互式 HTML
- 调查小组件为你提供真实用户反馈来证明投入的价值

当你准备开始 HTML 转换时，有几个事项值得思考：

**架构方案：**
1. 静态站点生成器（Jekyll/Hugo）→ 输出嵌入 JS 图表的 HTML —— 你已经在使用 GitHub Pages，阻力最小
2. 构建一个小型 Python 脚本，接收你的 markdown 文章 + AI 摘要 → 为每篇文章生成带有 D3/Chart.js 可视化的丰富 HTML
3. 混合方案 —— 保持 markdown 作为数据源，在之上添加渲染层

考虑到你"快速交付"的风格，方案 2 最适合 —— 一个调用 Claude API 从每篇文章提取关键数据点并自动生成图表的 `md2html.py` 脚本。你可以在工作站上一夜之间批量处理 400 篇文章。

**让博客文章真正可视化的要素：**
- 每篇文章的代码频率/语言分解 → 饼图/柱状图
- 文章时间线 → 活动热力图（类似 GitHub 贡献图）
- 主题聚类 → 力导向图
- 每篇文章的阅读时间 + 复杂度评分

当模型完成训练时，分享结果 —— 很好奇你为代码模型使用了什么数据集和目标函数。