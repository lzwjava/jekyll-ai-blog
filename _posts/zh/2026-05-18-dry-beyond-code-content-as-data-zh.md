---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越代码的DRY：内容即数据
translated: true
type: note
---

确实如此。你触及了一个深刻的洞察——DRY（不要重复自己）原则并不只适用于代码。内容也存在重复模式，同样的思维方式同样适用：

- **超链接** —— 正是我们刚才所做的。一个规范位置，其他所有地方都指向它。这是内容“变量”最简单形式。
- **Jekyll `_data` 文件** —— 定义一次 YAML/JSON 数据结构，然后通过 `site.data.whatever` 在任何页面中引用。如果你的简历进度信息放在 `_data/education.yml` 中，两个页面都可以从该文件渲染数据，无需复制。
- **Jekyll {% raw %}`{% include %}`{% endraw %}** —— 共享代码片段。将进度列表一次性写入 `_includes/associate-degree-progress.md`，然后通过 {% raw %}`{% include ... %}`{% endraw %} 将其引入两个页面。这就像是对内容的函数调用。
- **嵌入（Transclusion）** —— 某些系统允许在渲染时将一页的一部分嵌入到另一页中。Obsidian 原生支持此功能。对于 Jekyll，你需要像 `jekyll-crosspost` 这样的插件。

更深层的理念是：文本即数据。一旦认识到这一点，你就会停止复制粘贴，开始问“这段内容应该存在于何处，又有哪些地方引用了它？”——这与你在编码时的直觉完全一致。

你的简历和进度更新文章正是一个完美案例。更进一步的做法是将考试数据放入 `_data/` 目录，让两个页面都从这一单一来源生成显示内容。想继续深入探讨吗？