---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed Liquid Raw Tags
translated: false
type: note
---

All 23 files are fixed with balanced raw/endraw pairs. Here's a summary:

**Fixed 23 files across 11 post topics** (each with en + zh variants, plus the DRY post)

The problem: Jekyll's Liquid parser runs before markdown rendering, so `{{ }}` and `{% raw %}{% %}{% endraw %}` in code blocks (even fenced ``` blocks) get parsed as Liquid expressions.

The fix: Wrapped each affected fenced code block with `{% raw %}...{% endraw %}` so Liquid leaves the content untouched:

- **Ansible posts** (2 topics): `{{ source_dir }}`, `{{ item.path | relpath(...) }}` etc.
- **JSX post**: `{{ color: "red" }}` style objects  
- **Vault post**: Go template `{{.UserDN}}`
- **Angular posts** (3 topics): `{{ count() }}`, `{{ totalItems$ | async }}`
- **GitHub Actions post**: `{{ inputs.version || 'latest' }}`
- **Gitea Docker posts** (2 topics): `{{range $k,$v ...}}`, `{{.Names}}`
- **Nextcloud post**: `{{.Name}}`, `{{.CPUPerc}}`
- **DRY post** (en + zh): inline `{% include %}` and `{% include ... %}` wrapped individually with `{% raw %}...{% endraw %}`