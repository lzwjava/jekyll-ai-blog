---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Jekyll中混合使用Markdown和HTML
translated: true
type: note
---

问题：在Jekyll中，如何在同一文件内混合使用Markdown和HTML？

答案：

Jekyll的Markdown处理器（默认使用kramdown）会原样传递原始HTML，因此你可以直接在`.md`文件中内嵌HTML：

```markdown
# 我的标题

一些**Markdown**文本。

<div class="custom-box">
  <p>原始HTML可以以内联方式使用。</p>
</div>

更多Markdown内容。
```

但需要注意：默认情况下，kramdown**不会**解析块级HTML*内部*的Markdown。因此以下写法会失败：

```markdown
<div class="note">
**这仍是字面星号**，并非加粗效果。
</div>
```

根据需求，有三种修复方法：

**1. `markdown="1"`属性**——告知kramdown解析该元素内部的Markdown：

```markdown
<div class="note" markdown="1">
**这会变成加粗**，[链接](/work)也同样有效。
</div>
```

**2. 在内联内容周围添加空行**——kramdown会将空行视为跨度边界，对于简单情况无需属性即可生效：

```markdown
<div class="note">

**因为周围空行的存在，此处会变成加粗。**

</div>
```

**3. 在`_config.yml`中设置`parse_block_html: true`**——全局启用此功能，无需再使用`markdown="1"`：

```yaml
kramdown:
  parse_block_html: true
```

权衡之处：全局启用后，对空白敏感的HTML（如`<pre>`或`<code>`块）可能会被破坏，因为kramdown会尝试将其内容解析为Markdown。如果仅需偶尔使用，按元素添加`markdown="1"`属性更安全。

对于涉及逻辑的HTML（循环、包含文件），可直接在`.md`文件中使用Liquid——它会在Markdown处理器之前执行：

{% raw %}
```markdown
## 项目列表

<ul>
{% for project in site.data.projects %}
  <li><a href="{{ project.url }}">{{ project.name }}</a></li>
{% endfor %}
</ul>
```
{% endraw %}

参考资料：

- [kramdown — HTML代码块与parse_block_html](https://kramdown.gettalong.org/syntax.html#html-blocks)
- [Jekyll — 页面与Markdown](https://jekyllrb.com/docs/pages/)