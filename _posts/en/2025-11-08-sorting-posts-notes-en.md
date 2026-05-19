---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Sorting Posts and Notes
translated: false
type: note
---

### Modified `_includes/sort.html`

Your existing `sort.html` already has the language select with 9 options, which is perfect. No major changes needed here, but I've added a small note in the `<span id="post-number">` to make it more generic (e.g., "entries" instead of "posts") since we're now including notes. This can be dynamically updated by your JS if needed. Here's the tweaked version:

{% raw %}
```html
<div class="sort-container">
  <span id="post-number" class="post-number">
    {{ site.posts.size | plus: site.notes.size }} entries
    ({{ site.posts.size | plus: site.notes.size | divided_by: 7 | times: 6 }} Translated by <a href="https://openrouter.ai">AI</a>)
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

**Key change**: Updated the count to include `site.notes.size` (we'll define this below). The formula stays the same but now factors in notes. If your JS (`index.js`) already updates this span dynamically based on visible items, it will handle language-specific counts automatically.

### Step 1: Configure Notes as a Jekyll Collection (in `_config.yml`)

To treat `_notes` like `_posts` (so Jekyll processes the Markdown files and exposes them via `site.notes`), add this to your `_config.yml`. This is essential—without it, notes won't have `url`, `title`, `date`, etc., like posts do.

```yaml
collections:
  notes:
    output: true
    permalink: /notes/:path/
```

- `output: true` generates pages for notes (optional if you just want data).
- `permalink` ensures URLs like `/notes/es/2025-11-07-tidb-vs-cockroachdb-es/` (adjust if needed).
- Restart your Jekyll server after adding this.

Now `site.notes` works just like `site.posts`, assuming your note files (e.g., `_notes/es/2025-11-07-tidb-vs-cockroachdb-es.md`) have similar frontmatter: `title:`, `date:`, `image:`, `top:`, `translated:`, `generated:`.

### Step 2: Modified Page Layout (e.g., `index.md` or wherever your `<ul class="post-list">` lives)

Your current loop only shows English posts. To add notes and support all 9 languages:

- Define a list of languages once.
- Loop over **all** languages.
- For each language, add matching **posts** (from `_posts/{lang}/`) and **notes** (from `_notes/{lang}/`) as `<li>` items.
- Each `<li>` gets `class="... lang-{lang}"` so your JS can filter them (e.g., hide/show based on `#sort-select` value).
- This populates the entire list upfront (hidden by JS), then switches languages dynamically.
- Sort by date? Add `| sort: 'date' | reverse` to the loops if you want newest first (assuming dates are comparable).

Here's the full updated layout:

{% raw %}
```html
---
layout: page
---
{% include sort.html %}

<ul class="post-list">
  {% if site.posts.size == 0 and site.notes.size == 0 %}
    <li class="list-group-item post-item">No entries available.</li>
  {% else %}
    {% assign langs = "en,zh,ja,es,hi,fr,de,ar,hant" | split: "," %}
    {% for lang in langs %}
      {% comment %} Posts for this language {% endcomment %}
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

      {% comment %} Notes for this language (just like posts) {% endcomment %}
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

**Key changes**:
- **Languages array**: `{% assign langs = "en,zh,ja,es,hi,fr,de,ar,hant" | split: "," %}`—matches your select options. Easy to maintain.
- **Posts loop**: Removed the hard-coded `en` filter; now checks `post.path contains "_posts/{{ lang }}/"` for each lang.
- **Notes loop**: Added identically, checking `note.path contains "_notes/{{ lang }}/"`. Treats notes exactly like posts (same classes, attributes, structure).
- **Sorting**: Added `| sort: 'date' | reverse` to both loops for chronological order (newest first). Remove if not needed.
- **Empty check**: Updated to include `site.notes.size`.
- **Performance**: This generates all ~9 langs' content at build time. Fine for small sites; if huge, consider pagination or JS fetching.

### Optional: Add a Type Switch (Posts/Notes/Both)

You mentioned "add a select/switch , two options select or whatever". If you want a **second dropdown** to filter by type (e.g., Posts only, Notes only, or Both), add this to `sort.html` after the language select:

```html
<select id="type-select">
  <option value="both" selected>Posts & Notes</option>
  <option value="posts">Posts Only</option>
  <option value="notes">Notes Only</option>
</select>
```

Then, add a `data-type` attribute to each `<li>`:
- For posts: `data-type="posts"`
- For notes: `data-type="notes"`

Update your `index.js` to handle `#type-select` changes (e.g., filter `.post-item[data-type="notes"]` to hide/show). This keeps it simple without changing Liquid.

### Next Steps
- Test: Add a sample note like `_notes/es/2025-11-07-tidb-vs-cockroachdb-es.md` with frontmatter (title, date, etc.), rebuild, and switch to "Español" in the dropdown—it should appear.
- JS tweaks: Ensure `index.js` filters by `.lang-{value}` and updates `#post-number` (e.g., count visible `<li>`). If it doesn't handle notes yet, add `data-type` as above.
- If paths differ (e.g., no trailing `/` in dirs), tweak the `contains` checks.

This integrates notes seamlessly while keeping your 9-language setup. Let me know if you need JS snippets or further tweaks!