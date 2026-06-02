---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Install Behavior Modifiers Guide
translated: false
type: note
---

Here are similar npm install options that modify behavior without doing a full installation:

**Lock file related:**

- `--package-lock-only` - Only update package-lock.json, don't install packages
- `--no-package-lock` - Don't read from or write to package-lock.json at all
- `--lockfile-version <n>` - Set the lockfile format version (1, 2, or 3)

**Dry run / simulation:**

- `--dry-run` (or `-n`) - Show what would happen without actually installing or modifying anything

**Installation scope:**

- `--global` (or `-g`) - Install packages globally instead of locally
- `--production` - Only install dependencies, skip devDependencies
- `--omit=dev` - Skip devDependencies (newer syntax)
- `--omit=optional` - Skip optionalDependencies
- `--only=prod` - Only install production dependencies (older syntax)
- `--only=dev` - Only install devDependencies

**Package resolution:**

- `--legacy-peer-deps` - Ignore peer dependency conflicts (use old npm 6 behavior)
- `--strict-peer-deps` - Fail installation if peer dependency requirements can't be met
- `--force` - Force install even if there are conflicts

**Cache related:**

- `--prefer-offline` - Use cached packages when available, only go to network if needed
- `--offline` - Only use cached packages, never hit the network
- `--no-audit` - Skip security audit during install

**Other useful ones:**

- `--ignore-scripts` - Don't run pre/post install scripts
- `--no-save` - Install packages but don't update package.json

These give you fine-grained control over what npm does during installation.
