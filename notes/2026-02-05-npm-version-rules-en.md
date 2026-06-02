---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Caret and Tilde Version Rules
translated: false
type: note
---

In `package.json`, the `~` and `^` characters control how npm updates your dependencies:

**`^` (caret) - minor and patch updates**
- Allows updates that don't change the leftmost non-zero digit
- `^1.2.3` → allows `1.2.4`, `1.3.0`, `1.9.9` but NOT `2.0.0`
- `^0.2.3` → allows `0.2.4`, `0.2.9` but NOT `0.3.0` (because in 0.x versions, the second digit is considered major)
- This is the **default** when you run `npm install package`

**`~` (tilde) - patch updates only**
- Only allows patch-level changes
- `~1.2.3` → allows `1.2.4`, `1.2.9` but NOT `1.3.0`
- More conservative than `^`

**Practical example:**
```json
{
  "dependencies": {
    "react": "^18.2.0",     // can update to 18.x.x
    "lodash": "~4.17.21",   // can only update to 4.17.x
    "express": "4.18.2"     // exact version, no updates
  }
}
```

Most projects use `^` because it balances getting bug fixes and new features while avoiding breaking changes. If you need maximum stability (like in production apps), you might use `~` or exact versions, and commit your `package-lock.json` to ensure everyone gets identical dependencies.
