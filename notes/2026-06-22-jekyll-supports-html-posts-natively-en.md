---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jekyll Supports HTML Posts Natively
translated: false
type: note
---

Yes, very easy — Jekyll natively supports both. You don't need to migrate everything at once.

**Jekyll handles `.html` files directly** — just put an HTML file in your `_posts` or anywhere, and it renders as-is with your layout. You can mix `.md` and `.html` posts freely in the same site.

**Simplest migration path:**

Keep Jekyll, just change the output format per post. Instead of:

```
_posts/2024-01-01-my-post.md
```

Create:

```
_posts/2024-01-01-my-post.html
```

With the same front matter:

```html
---
layout: post
title: "My Post"
---

<div class="post-content">
  <!-- your rich HTML here -->
  <canvas id="chart"></canvas>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<script>
  // chart code
</script>
```

**The real work is the converter, not Jekyll.** A script like:

```python
# md2html.py — call Claude API to enrich each post
import anthropic, glob, pathlib

client = anthropic.Anthropic()

for md_file in glob.glob("_posts/*.md"):
    content = pathlib.Path(md_file).read_text()
    # ask Claude to rewrite as rich HTML with charts
    # write to _posts/*.html
```

**My suggestion:** don't batch-convert 400 posts. Pick 5-10 high-traffic ones, convert manually/semi-auto, see how it feels. Then automate if the format proves worth it.
