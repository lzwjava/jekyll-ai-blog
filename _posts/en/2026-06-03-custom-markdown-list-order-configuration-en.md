---
audio: false
generated: true
image: false
lang: en
layout: post
title: Custom Markdown List Order Configuration
translated: false
type: note
---

**Question:** How to configure markdownlint-cli2 to preserve custom list ordering (e.g., not enforce sequential numbering on ordered lists)?

**Answer:**

The issue is markdownlint's `MD029` rule, which enforces ordered lists to use sequential numbering (1, 2, 3...). Disable it via a `.markdownlint.json` config file:

```json
{
  "MD029": false
}
```

Or more granular — allow any list prefix:

```json
{
  "MD029": {
    "style": "any"
  }
}
```

For your pre-commit hook setup, place `.markdownlint.json` in the repo root:

```yaml
- repo: https://github.com/DavidAnson/markdownlint-cli2
  rev: v0.18.1
  hooks:
    - id: markdownlint-cli2
      args: ["--fix"]
      exclude: (node_modules/|logs/)
```

markdownlint-cli2 automatically discovers `.markdownlint.json` or `.markdownlint.yaml`.

**Other relevant list rules to consider disabling:**

| Rule | Default | What it does | Solution |
|------|---------|-------------|----------|
| `MD029` | `one_or_ordered` | Enforces sequential list numbering | `"MD029": { "style": "any" }` |
| `MD030` | enforces spaces after list markers | `- item` vs `-item` | `"MD030": false` |
| `MD007` | unordered list indentation | Enforces consistent indent | `"MD007": false` |

**Full `.markdownlint.json` to preserve list formatting:**

```json
{
  "MD029": { "style": "any" },
  "MD030": false,
  "MD007": false
}
```

Run `--fix` with this config and your list order survives.
