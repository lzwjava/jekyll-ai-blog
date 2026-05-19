---
audio: false
generated: true
image: false
lang: en
layout: post
title: 'Jekyll i18n: Polyglot Plugin & Folder Method'
translated: false
type: note
---

You’ve got three good paths for i18n in a Jekyll blog, from “batteries-included” to “bare-bones.” Here’s how each works and how to set it up.

# 1) Easiest: use a plugin (jekyll-polyglot)

**Best if you can build locally or with CI.** GitHub Pages’ built-in builder doesn’t allow most third-party plugins, so either build locally (`jekyll build`) and push the generated `_site/`, or use GitHub Actions to build and publish.

**Install**

```bash
gem install jekyll-polyglot
# or add to Gemfile:
# gem 'jekyll-polyglot'
```

**\_config.yml**

```yml
plugins:
  - jekyll-polyglot

languages: ["en", "zh", "ja"]   # your languages
default_lang: "en"
exclude_from_localization: ["assets", "images", "CNAME"]  # keep static paths shared
parallel_localization: true
```

**Content structure**

```
_index.md               # optional landing
_posts/
  2024-05-01-hello.en.md
  2024-05-01-hello.zh.md
pages/
  about.en.md
  about.zh.md
```

Polyglot builds language-scoped URLs like `/en/about/` and `/zh/about/`. It also exposes `site.active_lang`.

**Language switcher (in your layout)**

{% raw %}
```liquid
<nav class="lang-switch">
  {% for lang in site.languages %}
    {% if lang == site.active_lang %}
      <span>{{ lang }}</span>
    {% else %}
      <a href="{{ page.url | prepend:'/' | replace_first:'/' | prepend:'/' | absolute_url | replace: '/' | relative_url | prepend:'/' }}">
        {%- comment -%}
        We'll rebuild the current URL for each language:
        {%- endcomment -%}
      </a>
    {% endif %}
  {% endfor %}
</nav>
```
{% endraw %}

A simpler approach with Polyglot is:

{% raw %}
```liquid
<nav>
  {% for lang in site.languages %}
    <a href="{{ site.baseurl_root }}/{{ lang }}{{ page.permalink | default: page.url }}">{{ lang }}</a>
  {% endfor %}
</nav>
```
{% endraw %}

**UI strings via data files**
Create `_data/i18n.yml`:

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

Use in templates:

{% raw %}
```liquid
{{ site.data.i18n[site.active_lang].nav.home }}
```
{% endraw %}

**SEO (hreflang)**
In `<head>` of your layout:

{% raw %}
```liquid
{% assign langs = site.languages %}
{% for l in langs %}
  <link rel="alternate" hreflang="{{ l }}" href="{{ site.url }}/{{ l }}{{ page.url }}" />
{% endfor %}
<link rel="alternate" hreflang="x-default" href="{{ site.url }}/{{ site.default_lang }}{{ page.url }}" />
```
{% endraw %}

# 2) No plugin: per-language folders + Liquid

**Best if you must use GitHub Pages’ built-in builder.**

**Structure**

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

**\_config.yml**

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

**Set a current language**
Add in each page front matter:

```yml
---
layout: default
lang: en
---
```

or infer from path:

{% raw %}
```liquid
{% assign current_lang = page.lang | default: page.path | split:'/' | first | remove:'_' %}
```
{% endraw %}

**Cross-links between translations**
Use a shared identifier in front matter:

```yml
---
layout: post
lang: en
ref: hello-post
---
```

In the Chinese version:

```yml
---
layout: post
lang: zh
ref: hello-post
---
```

Then in the layout, find siblings:

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

**UI strings without plugins**
Use `_data/i18n.yml` as above, and choose the language via `current_lang`.

**Default language redirect (optional)**
Create `index.html` at root:

```html
<!doctype html>
<meta charset="utf-8">
<script>
  const lang = (navigator.language || '').toLowerCase().startsWith('zh') ? 'zh' : 'en';
  location.replace('/' + lang + '/');
</script>
<noscript><a href="/en/">English</a> · <a href="/zh/">中文</a></noscript>
```

# 3) Hybrid: one set of posts, translate only UI

**Best if you don’t translate articles, just the chrome (nav, footer).**
Keep a single `/posts/` set, add `_data/i18n.yml`, and render labels by language. Provide per-language index pages that list the same posts, but with localized dates and UI.

**Localized dates**

{% raw %}
```liquid
{% assign locale = page.lang | default: site.default_lang %}
{{ page.date | date: "%B %-d, %Y" }}  {# or use filters/plugins if you have them #}
```
{% endraw %}

(Jekyll’s built-in `date` is not fully locale-aware; for true locale formatting you’ll need a plugin or preformatted strings in data.)

---

## Practical tips

* **Slugs:** Keep the same `ref` for translated counterparts; let titles vary per language.
* **Images:** Put shared images in `/assets/` and exclude from localization so URLs stay stable.
* **Sitemaps & SEO:** Generate per-language sitemaps or ensure your sitemap lists all language URLs; add canonical tags within each language version.
* **Feeds:** Create per-language feeds by scoping collections: filter posts by `lang` in your feed template.

---

## Minimal working example (no-plugin)

1. `_data/i18n.yml` with strings.
2. `_en/index.md` and `_zh/index.md` with `lang` front matter.
3. Posts under `_posts/en/` and `_posts/zh/` with `lang` and shared `ref`.
4. Layout uses `site.data.i18n[current_lang]` and the sibling lookup snippet above.

If you tell me your current repo structure (and whether you’re building on GitHub Pages directly or via Actions), I can tailor a ready-to-drop config and a couple of starter layouts.