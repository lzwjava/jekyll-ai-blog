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

构建通过！🎉

```
状态：已完成
结论：成功
```

以下是事件总结：

根本原因：关于微调管道的文章在文本中包含了裸露的`{% %}`（描述Liquid标签语法）。Liquid尝试将其解析为未闭合的标签，导致构建崩溃。

共提交三次，两种不同的修复方案：

1. `_posts/en|zh/2026-06-12-fine-tuning-pipeline-*` 和 `notes/2026-06-12-*` ——这些文件没有原始包裹，因此裸露的`{% %}`需要进行内联转义：`{% raw %}{% %}{% endraw %}`

2. `_posts/en|zh/2026-06-14-fine-tuning-qwen3-*` 和 `notes/2026-06-14-*` ——这些文件已包含文件级别的`{% raw %}`包裹（第14行至末尾）。我最初添加的内联转义`{% raw %}{% %}{% endraw %}`实际上因过早关闭外层原始块而破坏了它们。现已恢复为原始的`{% %}`，在现有包裹内是安全的。
