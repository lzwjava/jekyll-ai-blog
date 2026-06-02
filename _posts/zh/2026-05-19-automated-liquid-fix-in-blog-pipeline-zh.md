---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 博客流水线中的自动化Liquid修复
translated: true
type: note
---

两个仓库都已清理并推送。摘要：

---

**已完成的工作：**

1. **修复了 `jekyll-ai-blog` 中的约 160 个博客文件**（位于 `_posts/` 和 `notes/` 目录下）——将未受保护的 `&#123;&#123; &#125;&#125;`/`&#123;&#37; &#37;&#125;` 模式用 `&#123;&#37; raw &#37;&#125;...&#123;&#37; endraw &#37;&#125;` 标签包裹，确保 Jekyll 构建通过（0 个 Liquid 异常，生成了 28K 个站点文件）

2. **为 `ww` 笔记流程添加了自动修复功能**——在 `create_note_utils.py` 中，`fix_liquid_raw_tags()` 会在每次保存笔记前由 `write_note()` 自动调用。该功能：
   - 检测包含 `&#123;&#123; &#125;&#125;` 或 `&#123;&#37; &#37;&#125;` 的围栏代码块
   - 用 `&#123;&#37; raw &#37;&#125;...&#123;&#37; endraw &#37;&#125;` 将其包裹
   - 跳过已包裹的代码块（避免重复包裹）
   - 记录日志：`[fix] Wrapped N code block(s) with raw/endraw tags for Liquid safety`

这意味着通过 `ww note` 创建的未来笔记将再也不会产生 Liquid 构建错误——修复操作在笔记创建时自动完成，远在进入 Jekyll 构建之前。
