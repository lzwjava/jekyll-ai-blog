---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 真理实验室单人AI研究实验室
translated: true
type: note
---

完成。我已经构建了 **Truth Labs** —— 一个位于 `/Users/lzwjava/projects/truth-labs` 的个人 AI 研究实验室站点，模仿 Thinking Machines Lab 的美学风格（暗色、极简、衬线字体、重证据而非炒作），并使用与你的博客相同的 Jekyll 工具链驱动。

## 创建了什么

5 个页面，全部来自 `2026-06-02-ai-portfolio-en.md`、`2025-01-11-resume-en.md` 以及你的 `notes/`：

- **`index.html`** —— 主视觉（“Truth through compute — nothing but truth”）、从硬数据提取的统计栏（52 GB VRAM 集群、13 个训练模型、约 5B tokens、12 年）、四大实验室支柱、精选实验，以及单人实验室宣言。
- **`research.html`** —— 开放实验室笔记本：你的完整 **13 次运行训练日志表**、nanoGPT fork（45 次提交、6 个配置）、SEC-EDGAR-GPT、推理工作（nano-vLLM 506 tok/s、从源码构建 SGLang、llama.cpp GGUF、MoE 追踪）、**M40/P100 BIOS 突破** 文章、GPU 拆解，以及 token 使用量表。
- **`services.html`** —— 四条可雇佣方向：AI 推理、GPU 与硬件、训练与微调、咨询 —— 每一条都有公开证据支持，另附合作模式与推荐人。
- **`about.html`** —— 从 NOIP 2011 → LeanCloud → DBS/HSBC → 2023 年转折点 → Truth Labs 的完整路径，以时间线呈现；快速事实、论文，以及为什么是单人实验室。
- **`contact.html`** —— 邮箱、GitHub、博客、作品集链接 + 每种服务应发送的内容。

## 设计

- 暗色主题（`#0a0a0b`）、Newsreader 衬线字体 + Inter、琥珀色“真理金”强调色 `#e3b341`
- 粘性玻璃效果页头、统计条带、带状态徽章的支柱/实验卡片、悬停状态、等宽标签
- 完全响应式（移动端从两列变为一列）、自定义 SVG favicon

## 已验证

`bundle install` + `bundle exec jekyll build` 编译干净；所有 5 个页面和 CSS 从 `jekyll serve` 返回 200。

本地预览：

```bash
cd /Users/lzwjava/projects/truth-labs && bundle exec jekyll serve --livereload
```

附注：我完全基于你作品集/简历中的事实编写，没有虚构内容 —— 建议快速浏览一下，以防你想调整具体细节（例如 about 页面上的论文日期，我根据简历中 2026 年 8 月的引用写成了 2025 年）。
