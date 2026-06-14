---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Liquid标签构建修复
translated: true
type: note
---

{% raw %}

构建通过！🎉

```
状态：已完成
结论：成功
```

以下是事件总结：

根本原因：关于微调管道的文章在文本中包含了裸露的Liquid标签语法（如 `{% %}`）。Liquid尝试将其解析为未闭合的标签，导致构建崩溃。

共提交三次，两种不同的修复方案：

1. `_posts/en|zh/2026-06-12-fine-tuning-pipeline-*` 和 `notes/2026-06-12-*` ——这些文件没有原始包裹，因此裸露的标签语法需要使用raw/endraw对进行内联转义。

2. `_posts/en|zh/2026-06-14-fine-tuning-qwen3-*` 和 `notes/2026-06-14-*` ——这些文件已包含文件级别的原始包裹。我最初在外部包裹内添加的内联raw/endraw对实际上因过早关闭外层原始块而破坏了它们。现已恢复为原始的裸露语法，在现有包裹内是安全的。

{% endraw %}
