---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 液体修复后的绿色建造
translated: true
type: note
---

✅ **构建再次通过。** 工作流运行以 `success` 完成（计划运行被 `concurrency: cancel-in-progress` 取消了，这是预期行为）。

## 总结

**为什么构建停止工作：** 自 **2026-10-13** 起，每次 `gh-pages.yml` 运行都在 **"Build with Jekyll"** 步骤失败。真正的错误：

```
Liquid Exception: Liquid syntax error (line 33): 'raw' tag was never closed
  in _posts/en/2026-10-13-python-jekyll-compatible-static-site-generator-en.md
```

**根本原因：** 文章 `_posts/en/2026-10-13-python-jekyll-compatible-static-site-generator-*.md`（以及其中文翻译和笔记集合副本）在行内代码反引号中包含字面量 `{% raw %}`：

{% raw %}

```markdown
- Liquid：`{% raw %}` 会吞掉错误标签，`{{ ... }}` 渲染为空，...
- `{% seo %}` 镜像了 jekyll-seo-tag 2.9.1 ...
```

{% endraw %}

Jekyll 在 **Markdown 之前**运行 **Liquid**，因此反引号无法保护标签。`{% raw %}` 打开了一个从未关闭的原始块（任何地方都没有 `{% endraw %}`），这是一个硬 `Liquid::SyntaxError`，导致整个站点构建中止。日期完全吻合——文章日期为 2026-10-13，与失败开始的时间是同一天。（"github-pages gem can't satisfy your Gemfile" 注释只是咨询性警告，不是原因。）

**已应用的修复** 在 3 个文件中（英文文章、中文文章、笔记源）使用了 Jekyll 的规范转义语法：

- `` `{% raw %}` `` → `` `{{ "{%" }} raw %}` ``
- `` `{% seo %}` `` → `` `{{ "{%" }} seo %}` ``
- `` `{{ ... }}` `` → `` `{{ "{{" }} ... }}` ``

渲染后的页面仍然会显示 `{% raw %}` / `{% seo %}` 作为可见文本（已在本地使用 Liquid 4.0.4 验证），但它们不再会被解析为标签。已提交为 `5919cdb00`，推送后，手动工作流运行确认成功。