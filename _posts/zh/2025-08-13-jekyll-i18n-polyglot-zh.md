---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jekyll国际化：多语言插件与目录方法
translated: true
type: note
---

为 Jekyll 博客实现国际化有三种可靠方案，从"开箱即用"到"高度定制"任君选择。以下是每种方案的具体实现方法。

# 1) 最简方案：使用插件（jekyll-polyglot）

**适用于本地构建或持续集成环境**。由于 GitHub Pages 官方构建器不支持大多数第三方插件，您需要在本地执行 `jekyll build` 后推送生成的 `_site/` 目录，或通过 GitHub Actions 实现自动构建发布。

**安装**

```bash
gem install jekyll-polyglot
# 或添加到 Gemfile：
# gem 'jekyll-polyglot'
```

**\_config.yml 配置**

```yml
plugins:
  - jekyll-polyglot

languages: ["en", "zh", "ja"]   # 支持的语言列表
default_lang: "en"
exclude_from_localization: ["assets", "images", "CNAME"]  # 共享静态资源路径
parallel_localization: true
```

**内容结构**

```
_index.md               # 可选首页
_posts/
  2024-05-01-hello.en.md
  2024-05-01-hello.zh.md
pages/
  about.en.md
  about.zh.md
```

Polyglot 会自动生成语言路径如 `/en/about/` 和 `/zh/about/`，同时提供 `site.active_lang` 变量。

**语言切换器（布局文件中）**

{% raw %}

```liquid
<nav class="lang-switch">
  {% for lang in site.languages %}
    {% if lang == site.active_lang %}
      <span>{{ lang }}</span>
    {% else %}
      <a href="{{ page.url | prepend:'/' | replace_first:'/' | prepend:'/' | absolute_url | replace: '/' | relative_url | prepend:'/' }}">
        {%- comment -%}
        此处为每种语言重建当前URL
        {%- endcomment -%}
      </a>
    {% endif %}
  {% endfor %}
</nav>
```

{% endraw %}

更简洁的实现方式：

{% raw %}

```liquid
<nav>
  {% for lang in site.languages %}
    <a href="{{ site.baseurl_root }}/{{ lang }}{{ page.permalink | default: page.url }}">{{ lang }}</a>
  {% endfor %}
</nav>
```

{% endraw %}

**界面文本本地化**
创建 `_data/i18n.yml`：

```yml
en:
  nav:
    home: "Home"
    posts: "Posts"
zh:
  nav:
    home: "主页"
    posts: "文章"
```

模板中调用：

{% raw %}

```liquid
{{ site.data.i18n[site.active_lang].nav.home }}
```

{% endraw %}

**SEO 优化（hreflang）**
在布局文件的 `<head>` 部分添加：

{% raw %}

```liquid
{% assign langs = site.languages %}
{% for l in langs %}
  <link rel="alternate" hreflang="{{ l }}" href="{{ site.url }}/{{ l }}{{ page.url }}" />
{% endfor %}
<link rel="alternate" hreflang="x-default" href="{{ site.url }}/{{ site.default_lang }}{{ page.url }}" />
```

{% endraw %}

# 2) 无插件方案：分语言目录 + Liquid 逻辑

**适用于 GitHub Pages 官方构建器**

**目录结构**

```
_en/
  index.md
  about.md
_zh/
  index.md
  about.md
_posts/
  en/
    2024-05-01-hello.md
  zh/
    2024-05-01-hello.md
```

**\_config.yml 配置**

```yml
defaults:
  - scope: { path: "_posts/en" }
    values: { lang: "en", permalink: "/en/:categories/:year/:month/:day/:title/" }
  - scope: { path: "_posts/zh" }
    values: { lang: "zh", permalink: "/zh/:categories/:year/:month/:day/:title/" }
  - scope: { path: "_en" }
    values: { lang: "en", permalink: "/en/:path/" }
  - scope: { path: "_zh" }
    values: { lang: "zh", permalink: "/zh/:path/" }
```

**设置当前语言**
在每个页面的 Front Matter 中添加：

```yml
---
layout: default
lang: en
---
```

或通过路径推断：

{% raw %}

```liquid
{% assign current_lang = page.lang | default: page.path | split:'/' | first | remove:'_' %}
```

{% endraw %}

**翻译版本互链**
在 Front Matter 中使用共享标识符：

```yml
---
layout: post
lang: en
ref: hello-post
---
```

中文版本：

```yml
---
layout: post
lang: zh
ref: hello-post
---
```

在布局文件中查找对应版本：

{% raw %}

```liquid
{% assign siblings = site.pages | concat: site.posts | where:"ref", page.ref %}
{% for s in siblings %}
  {% unless s.url == page.url %}
    <a href="{{ s.url }}">{{ s.lang }}</a>
  {% endunless %}
{% endfor %}
```

{% endraw %}

**无插件界面文本本地化**
沿用上述 `_data/i18n.yml` 方案，通过 `current_lang` 选择语言。

**默认语言重定向（可选）**
在根目录创建 `index.html`：

```html
<!doctype html>
<meta charset="utf-8">
<script>
  const lang = (navigator.language || '').toLowerCase().startsWith('zh') ? 'zh' : 'en';
  location.replace('/' + lang + '/');
</script>
<noscript><a href="/en/">English</a> · <a href="/zh/">中文</a></noscript>
```

# 3) 混合方案：统一文章库，仅本地化界面

**适用于不需要翻译文章内容，只需本地化导航、页脚等界面元素的情况**
保持单一的 `/posts/` 文章库，配合 `_data/i18n.yml` 实现标签本地化。为每种语言创建独立的索引页，展示相同文章但使用本地化日期和界面。

**本地化日期显示**

{% raw %}

```liquid
{% assign locale = page.lang | default: site.default_lang %}
{{ page.date | date: "%B %-d, %Y" }}  {# 如需完整本地化支持需使用插件或预格式化字符串 #}
```

{% endraw %}

（Jekyll 内置的 `date` 过滤器不具备完整本地化能力，如需真正本地化日期格式需要插件支持或数据文件预格式化）

---

## 实用技巧

* **文章标识：** 翻译对等文章保持相同的 `ref` 值，允许标题按语言差异变化
* **图片资源：** 将共享图片置于 `/assets/` 目录并排除本地化，确保 URL 稳定性
* **站点地图与 SEO：** 生成按语言分类的站点地图，或确保主站点地图包含所有语言版本URL；为每个语言版本添加规范标签
* **内容订阅：** 通过限定集合范围创建分语言订阅源：在订阅模板中按 `lang` 字段过滤文章

---

## 最小可行示例（无插件方案）

1. 配置含本地化字符串的 `_data/i18n.yml`
2. 创建含 `lang` Front Matter 的 `_en/index.md` 和 `_zh/index.md`
3. 在 `_posts/en/` 和 `_posts/zh/` 下创建含 `lang` 和共享 `ref` 的文章
4. 布局文件使用 `site.data.i18n[current_lang]` 并集成上述版本查找代码段

如果您能提供当前仓库结构信息（以及是否直接使用 GitHub Pages 或通过 Actions 构建），我可以为您量身定制即插即用的配置文件和入门布局模板。
