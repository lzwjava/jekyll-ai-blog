---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 公司理念部分已添加
translated: true
type: note
---

全部完成。公司哲学现已展示在“我们信奉什么”（What We Believe）部分。

**改动：**

1. **`index.html`** — 在 About 部分的六张信念卡片之后，添加了一个高亮的公司哲学横条：
   - 标签：**公司哲学**
   - 标题：**又快又好 —— 快，绝不牺牲质量**（Fast AND good — speed without sacrificing quality）
   - 描述：快是一种承诺（小步推进、每周交付、当天启动、绝不让客户等待）；好是基线（整洁代码、可持续架构、每次发布都能经受上线与时间考验）—— 通过流程、自动化和 AI 杠杆让两者同时成立。

2. **`style.css`** — 新增 `.philosophy` 横条样式：居中的卡片，带渐变边框（与站点的橙色→粉色→紫色强调渐变匹配），内部使用自适应的 `--bg-alt` 以适配浅色/深色主题，并在 ≤640px 时提供响应式尺寸。

3. **`i18n.js`** — 添加了英文翻译，使该横条能随 EN 切换正确切换：
   - 公司哲学 → Our Company Philosophy
   - 又快又好 —— 快，绝不牺牲质量 → Fast AND good — speed without sacrificing quality
   - 完整描述也已翻译。

我验证了 i18n 键与 HTML 文本节点完全匹配，因此语言切换将正确翻译新增的横条。
