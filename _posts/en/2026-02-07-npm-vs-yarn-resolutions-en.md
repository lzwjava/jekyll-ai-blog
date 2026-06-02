---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: npm Overrides vs Yarn Resolutions
translated: false
type: note
---

Yes, you're correct!

**npm 8.3.0+**: Introduced the `overrides` field in package.json
**Before npm 8.3.0**: There was no native npm solution - you had to use **Yarn's `resolutions`** field (which is Yarn-specific, not npm)

Here's the breakdown:

## For npm 8.3.0 and later

```json
{
  "overrides": {
    "package-name": "version",
    "parent-package": {
      "dependency-name": "version"
    }
  }
}
```

## Before npm 8.3.0

If you were using **Yarn**, you could use:

```json
{
  "resolutions": {
    "package-name": "version"
  }
}
```

If you were using **npm < 8.3.0**, you had limited options:

- Use `npm-force-resolutions` package as a workaround
- Manually use `npm shrinkwrap`
- Switch to Yarn to use `resolutions`
- Wait for npm 8.3.0+ to get native support

So `resolutions` was never an npm feature - it was always a Yarn feature. npm finally added its own equivalent with `overrides` in version 8.3.0.
