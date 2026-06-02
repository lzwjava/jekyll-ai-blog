---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Blobless Git Clone Benefits
translated: false
type: note
---

The Git command:

```bash
git clone --filter=blob:none <repository-url>
```

is a **partial clone** that downloads **almost no file contents** (blobs) at checkout time. Here's exactly what it does and why it's useful:

### What `--filter=blob:none` means

- `--filter=blob:none` tells Git to use **blobless cloning**.
- Git still downloads:
  - All commits (history)
  - All tree objects (directory structure)
  - All refs/branches/tags
- But it downloads **zero file contents** (blobs) during the initial clone.
- When you later `git checkout` or switch branches, Git downloads only the blobs (file contents) for the files that are actually needed in your working tree at that moment.

### Key benefits

- Extremely fast and tiny initial clone (often just a few MB even for huge repos like Linux kernel, Android, or Windows source).
- Uses much less network bandwidth and disk space at first.
- Perfect for CI/CD, quick look-ups, or when you only need history (e.g. `git log`, blame, diff across commits) without checking out files.

### Example size comparison (real-world)

| Repository       | Normal clone | `blob:none` clone | Speed gain |
|------------------|--------------|-------------------|------------|
| torvalds/linux   | ~5+ GB       | ~300–400 MB       | 10–20× faster |
| microsoft/vscode | ~2–3 GB      | ~200 MB           | much faster   |

### Common follow-up commands after blob:none clone

```bash
# First time you need a working tree:
git checkout <branch>        # downloads only needed blobs

# Or if you want everything later:
git fetch --unshallow        # not needed for blobless
# To fill in missing blobs permanently:
git repack -a -d             # optional, forces downloading all blobs
```

### Related filters you might see

- `--filter=blob:none` → no blobs at all initially (most aggressive)
- `--filter=tree:0`    → downloads trees but no blobs (similar effect)
- `--filter=sparse:oid=<oid>` → for sparse-checkout with partial blobs

### Summary

```bash
git clone --filter=blob:none https://github.com/example/repo.git
```

= “Give me the full history and structure immediately, but download file contents on-demand later.”
Great for huge monorepos or when you just want to browse history without waiting hours.
