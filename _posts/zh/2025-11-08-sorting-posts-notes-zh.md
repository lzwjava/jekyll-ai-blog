---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 文章与笔记排序
translated: true
type: note
---

### 修改后的 `_includes/sort.html`

您现有的 `sort.html` 已经包含带有9个选项的语言选择器，这非常完美。这里不需要大的改动，但我在 `<span id="post-number">` 中添加了一个小注释，使其更通用（例如，使用"entries"而不是"posts"），因为我们现在包含了笔记。如果需要，这可以通过您的JS动态更新。以下是调整后的版本：

{% raw %}
```html
<div class="sort-container">
  <span id="post-number" class="post-number">
    {{ site.posts.size | plus: site.notes.size }} 个条目
    ({{ site.posts.size | plus: site.notes.size | divided_by: 7 | times: 6 }} 由 <a href="https://openrouter.ai">AI</a> 翻译)
  </span>
  <select id="sort-select">
    <option value="en" selected>English</option>
    <option value="zh">中文</option>
    <option value="ja">日本語</option>
    <option value="es">Español</option>
    <option value="hi">हिंदी</option>
    <option value="fr">Français</option>
    <option value="de">Deutsch</option>
    <option value="ar">العربية</option>
    <option value="hant">繁體中文</option>
  </select>
</div>
```
{% endraw %}

**关键更改**：更新了计数以包含 `site.notes.size`（我们将在下面定义这个）。公式保持不变，但现在考虑了笔记。如果您的JS（`index.js`）已经根据可见项动态更新此span，它将自动处理特定语言的计数。

### 步骤1：将笔记配置为Jekyll集合（在 `_config.yml` 中）

要将 `_notes` 像 `_posts` 一样对待（以便Jekyll处理Markdown文件并通过 `site.notes` 公开它们），请将此添加到您的 `_config.yml` 中。这至关重要——没有它，笔记将无法像文章一样拥有 `url`、`title`、`date` 等属性。

```yaml
collections:
  notes:
    output: true
    permalink: /notes/:path/
```

- `output: true` 为笔记生成页面（如果只需要数据，则为可选）。
- `permalink` 确保URL如 `/notes/es/2025-11-07-tidb-vs-cockroachdb-es/`（如果需要，请调整）。
- 添加此配置后，请重新启动Jekyll服务器。

现在 `site.notes` 就像 `site.posts` 一样工作，假设您的笔记文件（例如 `_notes/es/2025-11-07-tidb-vs-cockroachdb-es.md`）具有类似的前言数据：`title:`、`date:`、`image:`、`top:`、`translated:`、`generated:`。

### 步骤2：修改后的页面布局（例如 `index.md` 或您的 `<ul class="post-list">` 所在的位置）

您当前的循环仅显示英文文章。要添加笔记并支持所有9种语言：

- 定义一次语言列表。
- 循环遍历**所有**语言。
- 对于每种语言，添加匹配的**文章**（来自 `_posts/{lang}/`）和**笔记**（来自 `_notes/{lang}/`）作为 `<li>` 项。
- 每个 `<li>` 获得 `class="... lang-{lang}"`，以便您的JS可以过滤它们（例如，根据 `#sort-select` 值隐藏/显示）。
- 这将预先填充整个列表（由JS隐藏），然后动态切换语言。
- 按日期排序？如果您希望最新的在前（假设日期是可比较的），请在循环中添加 `| sort: 'date' | reverse`。

以下是完整的更新后布局：

{% raw %}
```html
---
layout: page
---
{% include sort.html %}

<ul class="post-list">
  {% if site.posts.size == 0 and site.notes.size == 0 %}
    <li class="list-group-item post-item">暂无可用条目。</li>
  {% else %}
    {% assign langs = "en,zh,ja,es,hi,fr,de,ar,hant" | split: "," %}
    {% for lang in langs %}
      {% comment %} 此语言的文章 {% endcomment %}
      {% for post in site.posts | sort: 'date' | reverse %}
        {% if post.path contains "_posts/{{ lang }}/" %}
          {% assign translated = post.translated %}
          {% assign generated = post.generated %}
          {% if translated == nil %}{% assign translated = false %}{% endif %}
          {% if generated == nil %}{% assign generated = false %}{% endif %}
          <li class="list-group-item post-item lang-{{ lang }}" data-top="{{ post.top }}" data-translated="{{ translated }}" data-generated="{{ generated }}">
            <a href="{{ post.url }}">
              <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
              <span class="type">{% if post.image %}image{% else %}text{% endif %}</span>
              <span class="title">{{ post.title }}</span>
            </a>
          </li>
        {% endif %}
      {% endfor %}

      {% comment %} 此语言的笔记（与文章相同） {% endcomment %}
      {% for note in site.notes | sort: 'date' | reverse %}
        {% if note.path contains "_notes/{{ lang }}/" %}
          {% assign translated = note.translated %}
          {% assign generated = note.generated %}
          {% if translated == nil %}{% assign translated = false %}{% endif %}
          {% if generated == nil %}{% assign generated = false %}{% endif %}
          <li class="list-group-item post-item lang-{{ lang }}" data-top="{{ note.top }}" data-translated="{{ translated }}" data-generated="{{ generated }}">
            <a href="{{ note.url }}">
              <span class="date">{{ note.date | date: "%Y.%m.%d" }}</span>
              <span class="type">{% if note.image %}image{% else %}text{% endif %}</span>
              <span class="title">{{ note.title }}</span>
            </a>
          </li>
        {% endif %}
      {% endfor %}
    {% endfor %}
  {% endif %}
</ul>

{% include footer.html %}
<script src="/assets/js/index.js"></script>
```
{% endraw %}

**关键更改**：
- **语言数组**：`{% assign langs = "en,zh,ja,es,hi,fr,de,ar,hant" | split: "," %}`—与您的选择选项匹配。易于维护。
- **文章循环**：移除了硬编码的 `en` 过滤器；现在检查每种语言的 `post.path contains "_posts/{{ lang }}/"`。
- **笔记循环**：以相同方式添加，检查 `note.path contains "_notes/{{ lang }}/"`。将笔记完全视为文章（相同的类、属性、结构）。
- **排序**：在两个循环中添加了 `| sort: 'date' | reverse` 以按时间顺序排列（最新的在前）。如果不需要，请移除。
- **空检查**：更新为包含 `site.notes.size`。
- **性能**：这在构建时生成所有约9种语言的内容。对于小型站点来说没问题；如果内容庞大，请考虑分页或JS获取。

### 可选：添加类型切换器（文章/笔记/两者）

您提到“添加一个选择器/切换器，两个选项选择或任何东西”。如果您想要**第二个下拉菜单**来按类型过滤（例如，仅文章、仅笔记或两者），请在语言选择器之后将此添加到 `sort.html`：

```html
<select id="type-select">
  <option value="both" selected>文章 & 笔记</option>
  <option value="posts">仅文章</option>
  <option value="notes">仅笔记</option>
</select>
```

然后，为每个 `<li>` 添加一个 `data-type` 属性：
- 对于文章：`data-type="posts"`
- 对于笔记：`data-type="notes"`

更新您的 `index.js` 以处理 `#type-select` 的更改（例如，过滤 `.post-item[data-type="notes"]` 以隐藏/显示）。这在不更改Liquid的情况下保持简单。

### 后续步骤
- 测试：添加一个示例笔记，如 `_notes/es/2025-11-07-tidb-vs-cockroachdb-es.md`，并包含前言数据（标题、日期等），重新构建，并在下拉菜单中选择"Español"—它应该出现。
- JS调整：确保 `index.js` 通过 `.lang-{value}` 过滤并更新 `#post-number`（例如，计算可见的 `<li>`）。如果它尚未处理笔记，请如上所述添加 `data-type`。
- 如果路径不同（例如，目录中没有尾随 `/`），请调整 `contains` 检查。

这无缝集成了笔记，同时保持了您的9语言设置。如果您需要JS代码片段或进一步调整，请告诉我！