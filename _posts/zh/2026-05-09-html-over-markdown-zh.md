---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Thariq Shihipar 更偏爱 HTML 而非 Markdown
translated: true
type: note
---

问题：Thariq Shihipar 是如何表达 Claude Code 团队中的许多同事不再使用 Markdown 的？

回答：

关于“Claude Code 团队的许多同事不再使用 Markdown”这一具体说法，在 Thariq 已发表的任何文章中似乎并没有直接引述。不过，根据搜索结果，以下是 Thariq 于 2026 年 5 月 8 日发表的关于 Markdown 与 HTML 对比的完整立场背景：

## Thariq 是谁？

Thariq Shihipar 是 Anthropic 公司 Claude Code 团队的成员。他曾是 YC 创始人，大约一年前加入 Anthropic，负责连接工程、内容和客户反馈。他最显著的工程贡献是“向用户提问”工具，该工具使 Claude 能够在计划模式下以交互方式获取需求。

## Thariq 实际说了什么

2026 年 5 月 8 日，Thariq 发帖称：“HTML 是新的 Markdown。我几乎已经停止编写 Markdown 文件，转而使用 Claude Code 为我生成 HTML。”他还发表了一篇配套文章，题为 **《HTML 的不合理有效性》**，解释了原因。

## 他为什么反对 Markdown

他认为 Markdown 有明显局限：超过 100 行的文件难以阅读，可视化、色彩和图表等视觉表达方式有限，分享不方便，而且由于编辑工作常交给 Claude，人们直接编辑文件的频率降低——因此 Markdown 最大的优势已不复存在。

他列举了 HTML 相对于 Markdown 的四个关键优势：

1. **信息密度**——HTML 可以呈现表格、CSS 设计、SVG 插图、JavaScript 交互、空间数据和图像。Claude 在 Markdown 中用 Unicode 字符粗略表达颜色或绘制 ASCII 图表时的低效问题在 HTML 中不复存在。
2. **易于分享**——Markdown 无法被浏览器原生渲染，因此必须以附件形式发送。HTML 如果上传到 S3 等位置，可以通过单个链接分享，使得同事实际打开规划文档、报告和 PR 手册的可能性大大提高。
3. **双向交互**——在 HTML 文档中，可以添加滑块或按钮来直接调整设计选项，并将结果粘贴回 Claude Code，这在 Markdown 中无法实现。
4. **更深度的参与**——他说：“使用 HTML 让我更深度地参与 Claude 所做的事情。我原本担心不仔细阅读规划文档就意味着必须把决策权交给 Claude，但现在我比以往更清楚地理解 Claude 在做什么。”

## 他如何使用 HTML

他将 HTML 用于规划（将草稿选项并排放在单个文件中以便比较）、代码审查（一份 HTML 制作的指南比 GitHub 默认的差异视图更出色）、设计原型、报告，以及自定义编辑界面（如可拖拽卡片和基于表单的设置编辑器）——并且始终附带一个用于复制结果的按钮。

## 他承认的缺点

HTML 的生成时间比 Markdown 长 2 到 4 倍，在版本控制中差异复杂，且消耗更多 token。他的实用规则是：当输出需要反复阅读、团队评审、状态跟踪、比较、筛选或后续编辑时，使用 HTML；对于一次性笔记，则继续使用 Markdown。

## 关于“同事”的说法

“Claude Code 团队的许多同事不再使用 Markdown”这一具体断言在当前的搜索结果或他发表的文章中均未出现。你可能是在某个二手来源中看到了这句话的转述或误引，也可能出自 X（Twitter）上需要登录才能访问的回复帖。可以确认的是，Thariq 本人确实做出了这一转变并公开倡导——但他是否明确将这种观点归因于他的整个团队，目前无法从公开来源验证。

参考资料：

- [Thariq 的 HTML 示例配套网站](https://thariqs.github.io/html-effectiveness/)
- [Simon Willison 对文章的总结](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/)
- [DigitalToday：技术洞察——停止使用 Markdown，转向 HTML](https://www.digitaltoday.co.kr/en/view/54022/tech-insight-stop-using-markdown-move-to-html-why)
- [StableLearn：Claude Code 应输出 HTML，而非仅 Markdown](https://stable-learn.com/en/claude-code-html-output/)
