---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepWiki form width update
translated: false
type: note
---

Done. The DeepWiki form is now exactly **26rem** wide (and caps at `100%` so it never overflows small screens).

Compiled CSS confirms:
```css
.sort-container .deepwiki-link .deepwiki-form {
  width: 26rem;
  max-width: 100%;
  ...
}
```

Build passes. Note the `.dark-mode` override from before is untouched, so the form keeps its dark-mode styling too. These changes (along with the earlier badge removal + dark-mode fix) are still **uncommitted** — want me to commit them?
