---
audio: false
generated: true
image: false
lang: en
layout: post
title: CI Fix Push with Proxy Workaround
translated: false
type: note
---

Pushed. GitHub `main` is now at `5ca3c4aa9` containing the CI fix.

**Summary of what happened:**

1. **Committed** `5ca3c4aa9 fix(ci): use patch-less python version for ubuntu-latest` (8 workflow files, all hooks passed).
2. **Push** was troublesome:
   - `git push origin` (SSH via `git@github.com`) fails right now — your local SOCKS proxy (`localhost:7891`) is intermittently MITM-ing port-22 SSH (unusual banner `SSH-2.0-5ec5cb2f`, keys rejected), even though it worked minutes earlier.
   - HTTPS push through the proxy initially failed with GitHub `Internal Server Error` — that's an HTTP/2-through-proxy issue. Forcing **HTTP/1.1** fixed it:

     ```
     git -c http.version=HTTP/1.1 push https://github.com/lzwjava/jekyll-ai-blog.git main
     ```

3. **Verified**: `git ls-remote ... refs/heads/main` → `5ca3c4aa9`.

Two notes:

- If you want future pushes to be reliable, consider `git config --global http.version HTTP/1.1` (helps the HTTPS path) and/or switching `origin` to the HTTPS URL (`git remote set-url origin https://github.com/lzwjava/jekyll-ai-blog.git`) since your `gh` token works with it. Say the word and I'll apply either.
- There are now uncommitted changes (`_includes/sort.html`, `_sass/layout.scss`) that appeared after my `git add -A` — I left them untouched. Want me to commit/push those too?
