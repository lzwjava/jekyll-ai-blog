---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mixing Markdown and HTML in Jekyll
translated: false
type: note
---

Question: In Jekyll, how do I mix Markdown and HTML in the same file?

Answer:

Jekyll's Markdown processor (kramdown by default) passes raw HTML through untouched, so you can just inline HTML directly in a `.md` file:

```markdown
# My Heading

Some **markdown** text.

<div class="custom-box">
  <p>Raw HTML works inline.</p>
</div>

More markdown here.
```

The catch: by default, kramdown does **not** parse Markdown *inside* block-level HTML. So this fails:

```markdown
<div class="note">
**This stays literal asterisks**, not bold.
</div>
```

Three ways to fix it depending on what you need:

**1. `markdown="1"` attribute** — tell kramdown to parse Markdown inside that element:

```markdown
<div class="note" markdown="1">
**This becomes bold** and [links](/work) too.
</div>
```

**2. Blank lines around inline content** — kramdown treats a blank line as a span boundary, so this works without the attribute for simple cases:

```markdown
<div class="note">

**This becomes bold** because of the surrounding blank lines.

</div>
```

**3. `parse_block_html: true`** in `_config.yml` — make it global so you never need `markdown="1"`:

```yaml
kramdown:
  parse_block_html: true
```

Trade-off: with this on globally, whitespace-sensitive HTML (like `<pre>` or `<code>` blocks) can get mangled because kramdown now tries to interpret their contents as Markdown. The per-element `markdown="1"` is safer if you only need it occasionally.

For HTML spanning logic (loops, includes), use Liquid in the `.md` file directly — it runs before the Markdown processor:

{% raw %}
```markdown
## Projects

<ul>
{% for project in site.data.projects %}
  <li><a href="{{ project.url }}">{{ project.name }}</a></li>
{% endfor %}
</ul>
```
{% endraw %}

References:

- [kramdown — HTML blocks / parse_block_html](https://kramdown.gettalong.org/syntax.html#html-blocks)
- [Jekyll — Pages & Markdown](https://jekyllrb.com/docs/pages/)
