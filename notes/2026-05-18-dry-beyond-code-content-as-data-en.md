---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DRY Beyond Code: Content as Data"
translated: false
type: note
---

Exactly. You've hit on a real insight — DRY isn't just for code. Content has duplication patterns too, and the same mindset applies:

- **Hyperlinks** — what we just did. One canonical location, everywhere else points to it. Simplest form of content "variable."

- **Jekyll `_data` files** — define a YAML/JSON data structure once, then reference it in any page via `site.data.whatever`. If your resume progress was in `_data/education.yml`, both pages could render from it without copying.

- **Jekyll {% raw %}`{% include %}`{% endraw %}** — a shared snippet. Write the progress bullets once in `_includes/associate-degree-progress.md`, then {% raw %}`{% include ... %}`{% endraw %} it into both pages. Truly like a function call for content.

- **Transclusion** — some systems let you embed a section of one page inside another at render time. Obsidian does this natively. For Jekyll you'd need a plugin like `jekyll-crosspost`.

The deeper idea: text is data. Once you see that, you stop copy-pasting and start asking "where does this live, and who references it?" — same instinct you'd have in code.

Your resume and progress post are a perfect case. The next level would be pulling the exam data into `_data/` and having both pages generate their display from that single source. Want to go there?