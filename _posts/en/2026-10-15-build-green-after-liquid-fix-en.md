---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build Green After Liquid Fix
translated: false
type: note
---

✅ **Build is green again.** The workflow run completed with `success` (the scheduled run got cancelled by `concurrency: cancel-in-progress`, which is expected).

## Summary

**Why the build stopped working:** Since **2026-10-13**, every `gh-pages.yml` run failed at the **"Build with Jekyll"** step. The real error:

```
Liquid Exception: Liquid syntax error (line 33): 'raw' tag was never closed
  in _posts/en/2026-10-13-python-jekyll-compatible-static-site-generator-en.md
```

**Root cause:** The post `_posts/en/2026-10-13-python-jekyll-compatible-static-site-generator-*.md` (and its zh translation + the notes collection copy) contained literal `{% raw %}` **inside inline code backticks**:

{% raw %}
```markdown
- Liquid: `{% raw %}` swallows bad tags, `{{ ... }}` renders empty, ...
- `{% seo %}` mirrors jekyll-seo-tag 2.9.1 ...
```
{% endraw %}

Jekyll runs **Liquid before Markdown**, so backticks don't protect tags. The `{% raw %}` opened a raw block that never closed (no `{% endraw %}` anywhere), which is a hard `Liquid::SyntaxError` that aborts the entire site build. The dates line up exactly — the post is dated 2026-10-13, the same day the failures started. (The "github-pages gem can't satisfy your Gemfile" annotation is only an advisory warning, not the cause.)

**Fix applied** in 3 files (en post, zh post, notes source) using Jekyll's canonical escaping syntax:

- `` `{% raw %}` `` → `` `{{ "{%" }} raw %}` ``
- `` `{% seo %}` `` → `` `{{ "{%" }} seo %}` ``
- `` `{{ ... }}` `` → `` `{{ "{{" }} ... }}` ``

The rendered page still displays `{% raw %}` / `{% seo %}` as visible text (verified with Liquid 4.0.4 locally), but they're no longer parsed as tags. Committed as `5919cdb00`, pushed, and the manual workflow run confirmed success.
