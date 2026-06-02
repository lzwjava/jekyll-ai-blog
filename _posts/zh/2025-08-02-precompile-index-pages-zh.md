---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预编译语言专属索引页
translated: true
type: note
---

是的，您可以为不同语言预编译独立的索引页面（例如 `index-zh.html`、`index-en.html`），以提升性能和用户体验，尤其是在您的网站拥有大量文章或希望减少客户端 JavaScript 处理的情况下。这种方法会在构建过程中为每种语言生成静态 HTML 文件，而不是依赖 JavaScript 在客户端动态筛选和排序文章。

下面，我将概述如何使用 Jekyll 实现这一点，重点介绍如何为每种语言创建独立的索引页面（`index-zh.html`、`index-en.html` 等），同时保持您当前设置的功能。这将利用 Jekyll 的构建系统来预计算每种语言的筛选后文章列表，减少对复杂客户端 JavaScript 的需求。

---

### 预编译 `index-zh.html`、`index-en.html` 等的方法

要为特定语言预编译索引页面，您可以为每种语言创建独立的 Jekyll 页面模板，并在构建过程中使用 Liquid 按语言筛选文章。这样，每个页面（`index-en.html`、`index-zh.html` 等）将仅包含相关文章，而排序/筛选逻辑将在构建时处理，而不是在浏览器中处理。

以下是具体步骤：

---

#### 1. 创建语言特定的页面模板

在您的 Jekyll 项目根目录中为每种语言创建独立的页面文件，例如：

- `index-en.html`
- `index-zh.html`
- `index-ja.html`
- ...以及其他语言（`es`、`hi`、`fr`、`de`、`ar`、`hant` 等）的类似文件。

每个文件将使用与您提供的代码类似的结构，但会使用 Liquid 筛选特定语言的文章。以下是 `index-en.html` 的示例：

{% raw %}
```html
---
layout: page
lang: en
permalink: /en/
---

<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign en_posts = site.posts | where: "lang", "en" %}
    {{ en_posts.size }} 篇文章
    ({{ en_posts | where: "translated", true | size }} 篇由 <a href="https://mistral.ai">AI</a> 生成)
  </span>

  <select id="sort-select">
    <option value="author-picks|en">精选</option>
    <option value="date-desc|all">全部</option>
    <option value="date-desc|original">原创</option>
    <option value="date-desc|en" selected>English</option>
    <option value="date-desc|zh">中文</option>
    <option value="date-desc|ja">日本語</option>
    <option value="date-desc|es">Español</option>
    <option value="date-desc|hi">हिंदी</option>
    <option value="date-desc|fr">Français</option>
    <option value="date-desc|de">Deutsch</option>
    <option value="date-desc|ar">العربية</option>
    <option value="date-desc|hant">繁體中文</option>
  </select>
</div>

<ul class="post-list">
  {% if en_posts.size > 0 %}
    {% for post in en_posts %}
      <li class="list-group-item post-item lang-en" data-top="{{ post.top | default: 0 }}" data-translated="{{ post.translated | default: false }}" data-generated="{{ post.generated | default: false }}">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}图片{% else %}文字{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">暂无文章。</li>
  {% endif %}
</ul>

<footer class="site-footer">
  <span class="site-footer-credits">
    由 <a href="https://jekyllrb.com/">Jekyll</a> 驱动<br>
    由 <a href="https://mistral.ai">Mistral</a> 点燃<br>
    更新于 <a href="https://github.com/lzwjava/lzwjava.github.io/commit/{{ site.release }}">{{ site.release | slice: 0, 6 }}</a><br>
    版权所有 © {{ site.starting_year }}–{{ site.time | date: "%Y" }}
  </span>
</footer>
```
{% endraw %}

对于 `index-zh.html`，您需要替换 `lang` 和 `where` 筛选器：

{% raw %}
```html
---
layout: page
lang: zh
permalink: /zh/
---
<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign zh_posts = site.posts | where: "lang", "zh" %}
    {{ zh_posts.size }} 篇文章
    ({{ zh_posts | where: "translated", true | size }} 篇由 <a href="https://mistral.ai">AI</a> 生成)
  </span>
  <!-- 同上 sort-select -->
</div>

<ul class="post-list">
  {% if zh_posts.size > 0 %}
    {% for post in zh_posts %}
      <li class="list-group-item post-item lang-zh" data-top="{{ post.top | default: 0 }}" data-translated="{{ post.translated | default: false }}" data-generated="{{ post.generated | default: false }}">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}图片{% else %}文字{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">暂无文章。</li>
  {% endif %}
</ul>

<!-- 同上 footer -->
```
{% endraw %}

为每种语言（`ja`、`es`、`hi`、`fr`、`de`、`ar`、`hant` 等）重复此过程，相应调整 `lang` 前置数据和 `where` 筛选器。

---

#### 2. 更新文章前置数据

确保您的 `_posts` 目录中的每篇文章都有一个 `lang` 前置数据变量，对应其语言（例如 `en`、`zh`、`ja` 等）。例如：

```yaml
---
title: 我的英文文章
lang: en
date: 2025-08-01
translated: true
generated: false
top: 1
---
```

这允许 `where` 筛选器正确按语言识别文章。

如果您的文章组织在子目录中，如 `_posts/en/`、`_posts/zh/` 等，您可以从路径推断语言，而不使用 `lang` 变量。例如，在 `index-en.html` 中：

{% raw %}
```liquid
{% assign en_posts = site.posts | where_exp: "post", "post.path contains '_posts/en/'" %}
```
{% endraw %}

---

#### 3. 简化 JavaScript

由于语言筛选现在在构建时处理，您可以简化 JavaScript，仅处理排序（例如按日期或作者精选）和语言页面之间的导航。以下是更新后的 JavaScript 版本：

{% raw %}
```javascript
window.addEventListener('load', function () {
  const sortSelect = document.getElementById('sort-select');
  const postNumber = document.getElementById('post-number');
  const postList = document.querySelector('.post-list');

  function updatePosts() {
    const selectedValue = sortSelect.value;
    const [sortOption, langFilter] = selectedValue.split('|');

    // 如果选择的语言与当前页面不匹配，则重定向
    const currentLang = '{{ page.lang }}';
    if (langFilter !== currentLang && langFilter !== 'all' && langFilter !== 'original' && sortOption !== 'author-picks') {
      window.location.href = `/${langFilter}/?sort=${selectedValue}`;
      return;
    }

    // 获取所有文章
    const posts = document.querySelectorAll('.post-list li.post-item');
    let processedPosts = [];

    if (sortOption === 'author-picks') {
      // 筛选 'data-top' > 0 的文章
      processedPosts = Array.from(posts)
        .filter(post => parseInt(post.dataset.top || 0, 10) > 0)
        .map(post => ({ element: post }));
    } else if (sortOption === 'date-desc' && langFilter === 'original') {
      // 筛选原创（非翻译、非生成）文章
      processedPosts = Array.from(posts)
        .filter(post => post.dataset.translated === 'false' && post.dataset.generated === 'false')
        .map(post => {
          const dateElement = post.querySelector('.date');
          const dateStr = dateElement ? dateElement.textContent.trim().replace(/\./g, '-') : null;
          return { element: post, date: dateStr ? new Date(dateStr) : null };
        })
        .filter(item => item.date)
        .sort((a, b) => b.date - a.date);
    } else {
      // 按日期降序排序
      processedPosts = Array.from(posts)
        .map(post => {
          const dateElement = post.querySelector('.date');
          const dateStr = dateElement ? dateElement.textContent.trim().replace(/\./g, '-') : null;
          const aElement = post.querySelector('a');
          const href = aElement ? aElement.getAttribute('href') : '';
          const fileName = href ? href.split('/').pop() : '';
          return { element: post, date: dateStr ? new Date(dateStr) : null, fileName };
        })
        .filter(item => item.date)
        .sort((a, b) => {
          const dateComparison = b.date - a.date;
          return dateComparison !== 0 ? dateComparison : a.fileName.localeCompare(b.fileName);
        });
    }

    // 清空现有列表
    postList.innerHTML = '';

    // 追加处理后的文章或显示消息
    if (processedPosts.length > 0) {
      processedPosts.forEach(item => {
        if (item.element) {
          postList.appendChild(item.element);
        }
      });
    } else {
      const noPostsMessage = document.createElement('li');
      noPostsMessage.className = 'list-group-item post-item';
      noPostsMessage.textContent = '暂无文章。请刷新页面。';
      postList.appendChild(noPostsMessage);
    }

    // 更新文章计数
    const translatedCount = processedPosts.filter(item => item.element && item.element.dataset.translated === 'true').length;
    postNumber.innerHTML = `${processedPosts.length} 篇文章 (${translatedCount} 篇由 <a href="https://mistral.ai">AI</a> 生成)`;

    // 显示列表
    postList.style.display = 'block';
  }

  // 从 localStorage 恢复或设置默认值
  const savedSort = localStorage.getItem('sortOption');
  if (savedSort) {
    sortSelect.value = savedSort;
  } else {
    sortSelect.value = 'date-desc|{{ page.lang }}';
  }

  updatePosts();

  // 下拉菜单变化的事件监听器
  sortSelect.addEventListener('change', function () {
    localStorage.setItem('sortOption', sortSelect.value);
    updatePosts();
  });
});
```
{% endraw %}

主要变更：
- 脚本检查所选语言是否与当前页面的语言（`{{ page.lang }}`）匹配。如果不匹配，则重定向到相应的语言页面（例如，中文为 `/zh/`）。
- 不再需要语言筛选，因为文章已由 Liquid 模板预筛选。

---

#### 4. 配置永久链接和导航

确保每个语言特定页面在其前置数据中具有唯一的永久链接（例如，`index-en.html` 的 `permalink: /en/`）。这允许用户直接导航到 `/en/`、`/zh/` 等。

您可能还需要更新网站的导航，以包含指向这些语言特定页面的链接。例如，在您的布局或页眉中：

```html
<nav>
  <a href="/en/">English</a>
  <a href="/zh/">中文</a>
  <a href="/ja/">日本語</a>
  <!-- 添加其他语言 -->
</nav>
```

---

#### 5. 处理“全部”和“原创”筛选器

对于下拉菜单中的“全部”和“原创”选项：
- **全部**：您可以创建一个包含所有文章的 `index.html`（类似于您的原始设置），或重定向到某个语言特定页面。
- **原创**：您可以创建一个 `index-original.html`，筛选 `translated: false` 和 `generated: false` 的文章：

{% raw %}
```html
---
layout: page
lang: original
permalink: /original/
---
<div class="sort-container">
  <span id="post-number" class="post-number">
    {% assign original_posts = site.posts | where: "translated", false | where: "generated", false %}
    {{ original_posts.size }} 篇文章
    (0 篇由 <a href="https://mistral.ai">AI</a> 生成)
  </span>
  <!-- 同上 sort-select -->
</div>

<ul class="post-list">
  {% if original_posts.size > 0 %}
    {% for post in original_posts %}
      <li class="list-group-item post-item lang-{{ post.lang }}" data-top="{{ post.top | default: 0 }}" data-translated="false" data-generated="false">
        <a href="{{ post.url }}">
          <span class="date">{{ post.date | date: "%Y.%m.%d" }}</span>
          <span class="type">{% if post.image %}图片{% else %}文字{% endif %}</span>
          <span class="title">{{ post.title }}</span>
        </a>
      </li>
    {% endfor %}
  {% else %}
    <li class="list-group-item post-item">暂无文章。</li>
  {% endif %}
</ul>

<!-- 同上 footer -->
```
{% endraw %}

---

#### 6. 预编译的优势

- **性能**：在构建时筛选文章减少了客户端 JavaScript 处理，使网站更快，特别是对于设备或连接速度较慢的用户。
- **SEO**：搜索引擎可以更好地索引语言特定页面（`/en/`、`/zh/` 等），提高可发现性。
- **更简单的 JavaScript**：JavaScript 仅需处理排序和导航，而不需要语言筛选。
- **可靠性**：预编译的页面避免了客户端错误（例如，您原始代码中的“已知错误待修复”消息）。

---

#### 7. 注意事项

- **构建时间**：预编译多个索引页面会增加构建时间，特别是如果您有许多文章或语言。然而，除非您有数千篇文章，否则这通常可以忽略不计。
- **维护**：您需要维护多个索引文件（`index-en.html`、`index-zh.html` 等）。为了减少重复，您可以使用 Jekyll 包含或布局来共享通用代码。
- **动态排序**：JavaScript 仍然处理排序（例如作者精选、日期降序），但如果您想要完全静态输出，可以预计算每个页面的排序版本（尽管这会创建更多文件，例如 `index-en-picks.html`）。

---

#### 8. 示例目录结构

您的 Jekyll 项目可能如下所示：

```
├── _posts/
│   ├── en/
│   │   ├── 2025-08-01-post1.md
│   │   ├── 2025-08-02-post2.md
│   ├── zh/
│   │   ├── 2025-08-01-post1-zh.md
│   ├── ja/
│   └── ...
├── _layouts/
│   ├── page.html
├── index-en.html
├── index-zh.html
├── index-ja.html
├── index-original.html
├── _includes/
│   ├── header.html
│   ├── footer.html
├── assets/
│   ├── js/
│   │   ├── sort.js
```

---

#### 9. 测试和部署

- 使用 `jekyll serve` 在本地测试，确保每个语言页面（`/en/`、`/zh/` 等）显示正确的文章。
- 验证下拉菜单导航在语言页面之间正确重定向。
- 部署到您的托管平台（例如 GitHub Pages），并检查永久链接是否按预期工作。

---

### 参考
- [Jekyll 文档](https://jekyllrb.com/docs/)
- [Mistral AI](https://mistral.ai)

如果您有进一步的问题或需要帮助实现特定部分，请告诉我！
