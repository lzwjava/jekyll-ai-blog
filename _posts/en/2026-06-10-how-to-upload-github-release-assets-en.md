---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to upload GitHub release assets
translated: false
type: note
---

**Question:** When drafting a release on GitHub, why don't I see a dedicated "Assets" settings section — where do I attach asset files?

**Answer:**

There is no separate "Assets" settings panel in the draft form — the uploader is the drop zone you already pasted:

> *"Attach binaries by dropping them here or selecting them."*

That box, directly **below the release description textarea**, *is* the asset upload area. Drag files onto it or click it to open a file picker. The familiar **"Assets" section** (the collapsible list showing your binaries + auto-generated `Source code (zip/tar.gz)`) only appears **after** you save the draft or publish — at draft-editing time it's just that drop zone.

Common reasons it looks missing or broken:

- **No tag selected yet** — some controls stay inert until you pick/create a tag.
- **Mobile browser** — the drag-and-drop zone is unreliable on mobile; use desktop or the CLI.
- **File too large** — each asset must be ≤ 2 GiB; oversized files fail silently-ish.
- **Ad blockers / network** — uploads go to `uploads.github.com`, sometimes blocked by proxies.

Since you're terminal-first, skip the UI entirely with `gh`:

```bash
# Create release + attach assets in one shot
gh release create v0.3.0 ./dist/ww-darwin-arm64 ./dist/ww-linux-amd64 \
  --title "v0.3.0" \
  --generate-notes

# Add assets to an existing release/draft
gh release upload v0.3.0 ./dist/ww-darwin-arm64 --clobber

# Draft (don't publish yet)
gh release create v0.3.0 ./dist/* --draft --generate-notes
```

For CI, the same thing via GitHub Actions:

```yaml
- uses: softprops/action-gh-release@v2
  with:
    files: dist/*
  if: startsWith(github.ref, 'refs/tags/')
```

For `ww`, the cleanest long-term setup is a tag-triggered workflow that builds binaries for each platform and uploads them automatically — no manual drag-and-drop ever.

**References:**

- [Managing releases in a repository — GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [gh release create — GitHub CLI manual](https://cli.github.com/manual/gh_release_create)
