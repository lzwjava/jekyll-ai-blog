---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Tgz vs Zip for npm Packages
translated: false
type: note
---

The main differences between `.tgz` and `.zip` for npm packages:

## Format & Compression
- **`.tgz`**: A tarball compressed with gzip (tar.gz). This is npm's native format.
- **`.zip`**: A zip archive, more common in Windows environments.

## npm Usage
- **`.tgz`**: The standard format created by `npm pack`. When you run this command, npm creates a `.tgz` file of your package.
- **`.zip`**: Not natively supported by npm commands, though you can manually create one.

## Installation
Both can be installed, but with different syntax:
```bash
npm install package.tgz
npm install package.zip
```

## Key Practical Differences

**File permissions**: `.tgz` preserves Unix file permissions and symbolic links, which `.zip` doesn't always handle well. This matters for packages with executable scripts.

**Consistency**: `.tgz` is what npm's registry uses internally. When you publish to npm, it's stored as a tarball.

**Cross-platform**: `.zip` is more familiar to Windows users, but `.tgz` works fine across all platforms with modern npm.

## When to Use Each
- Use `.tgz` for standard npm workflows (packing, sharing, installing packages)
- Use `.zip` only if you have a specific reason, like distributing to non-developers who might not have tar extraction tools

For npm package development and distribution, stick with `.tgz` — it's the standard and avoids potential compatibility issues.