---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Config Commands Explained Clearly
translated: false
type: note
---

Not quite! Let me clarify what each command does:

**`npm config ls -l`** (long format):

- Shows **all** config settings, including defaults
- Does NOT directly print `.npmrc` file contents
- Shows where each setting comes from (builtin, global, user, project)
- Shows the merged/effective configuration

**`npm config ls --json`**:

- Shows the same information as `npm config ls -l` but in JSON format
- Also shows all config settings with their sources
- Just formatted as JSON instead of plain text

Neither command directly prints the raw `.npmrc` file contents. Both show the **effective configuration** after npm has:

1. Read all `.npmrc` files (builtin defaults, global, user, project)
2. Merged them together
3. Applied precedence rules

**To see the actual `.npmrc` file contents**, you'd use:

```bash
cat ~/.npmrc           # user config
cat ./.npmrc           # project config
cat /etc/npmrc         # global config
```

**Key difference between `-l` and `--json`**:

- `-l` gives you more verbose output with sources indicated
- `--json` gives you structured JSON output (easier to parse programmatically)
- Both show all settings, not just the ones you've explicitly set
