---
title: Handling Notes in Jekyll
date: 2025-09-13
lang: en
layout: post
audio: false
translated: false
generated: true
image: false
model: openai/gpt-5
---

You’ve got two clean options:

## Option A — Make them real posts

If you want `site.posts` to include your notes, move them into `_posts` and make sure filenames follow the posts pattern:

```
_posts/en/2025-09-13-latest-ai-models.md
_posts/en/2025-09-13-maven-vs-gradle.md
_posts/en/2025-05-10-brt.md
_posts/en/2025-05-10-hyper-connected.md
_posts/en/2025-05-10-laundry-pods.md
```

Pros: works with all post features (pagination, `site.posts`, `jekyll-feed`, archives) without extra config.
Cons: they lose their “separate notes” identity unless you tag/categorize them.

## Option B — Keep them as a separate “notes” collection (recommended if you want `site.notes`)

1. Rename the folder to be a collection (underscore is required):

```
_notes/
  en/
    2025-09-13-latest-ai-models.md
    2025-09-13-maven-vs-gradle.md
    2025-05-10-brt.md
    2025-05-10-hyper-connected.md
    2025-05-10-laundry-pods.md
```

2. In `_config.yml`, declare the collection and turn on output:

```yaml
collections:
  notes:
    output: true
    permalink: /notes/:path/
# optional: if you keep per-lang subfolders
defaults:
  - scope: { path: "_notes/en" }
    values: { lang: "en", layout: "post" } # or your own layout
```

3. Access them in templates with:

```liquid
{% assign notes = site.notes | sort: "date" | reverse %}
{% for n in notes %}
  <a href="{{ n.url }}">{{ n.title }}</a>
{% endfor %}
```

Notes:

* Collection items don’t need date in the filename, but if you want sorting by date, put `date:` in front matter or keep the `YYYY-MM-DD-...` style.
* You can mirror your posts’ language structure under `_notes/en`, `_notes/zh`, etc., and set `lang:` via defaults or front matter.

---

## JSON endpoint for your notes

Create a `notes.json` at the site root:

```liquid
---
layout: null
permalink: /notes.json
---
[
{% assign items = site.notes | sort: "date" | reverse %}
{% for n in items %}
  {
    "title": {{ n.title | jsonify }},
    "url": {{ n.url | absolute_url | jsonify }},
    "date": "{{ n.date | date_to_xmlschema }}",
    "lang": {{ n.lang | default: "en" | jsonify }},
    "tags": {{ n.tags | default: empty | jsonify }}
  }{% unless forloop.last %},{% endunless %}
{% endfor %}
]
```

If you instead move them into `_posts`, just swap `site.notes` for `site.posts` in that file.

---

## Bonus: RSS/Atom feed for notes (if you use `jekyll-feed`)

In `_config.yml`:

```yaml
plugins:
  - jekyll-feed

feed:
  collections:
    - notes
```

This will expose a separate feed for the notes collection.

---

### Quick guidance

* If you want “one unified stream,” move to `_posts` (Option A).
* If you want a distinct bucket with `site.notes` and its own JSON/feed, make a collection (Option B). This keeps your current “notes” concept but the folder must be `_notes/`.
