---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jekyll 原生支持 HTML 格式文章
translated: true
type: note
---

是的，非常简单 —— Jekyll 原生就支持两者。你不需要一次性迁移所有内容。

**Jekyll 直接处理 `.html` 文件** —— 只需将 HTML 文件放入 `_posts` 或任何位置，它就会按原样渲染并应用你的布局。你可以在同一个站点中自由混合使用 `.md` 和 `.html` 文章。

**最简单的迁移路径：**

保留 Jekyll，只需更改每篇文章的输出格式。将原来的：
```
_posts/2024-01-01-my-post.md
```
改为：
```
_posts/2024-01-01-my-post.html
```

并保持相同的前置元数据（front matter）：
```html
---
layout: post
title: "我的文章"
---

<div class="post-content">
  <!-- 你丰富的 HTML 内容 -->
  <canvas id="chart"></canvas>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script>
  // 图表代码
</script>
```

**真正的工作在于转换器，而非 Jekyll。** 类似这样的脚本：

```python
# md2html.py —— 调用 Claude API 来丰富每篇文章
import anthropic, glob, pathlib

client = anthropic.Anthropic()

for md_file in glob.glob("_posts/*.md"):
    content = pathlib.Path(md_file).read_text()
    # 请求 Claude 将其重写为包含图表的丰富 HTML
    # 写入 _posts/*.html
```

**我的建议：** 不要批量转换 400 篇文章。先挑选 5-10 篇流量高的文章，手动或半自动转换，感受一下效果。如果这种格式值得采用，再考虑自动化。