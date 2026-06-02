---
audio: false
generated: true
image: false
lang: en
layout: post
title: Workflow Token Authentication Clarified
translated: false
type: note
---

All good now. The `ww action` just ran successfully and triggered the workflow.

The error was NOT caused by your SSH→HTTPS switch. Here's what happened:

1. `ww action` uses `gh workflow run` (the `gh` CLI), which uses its OWN OAuth token stored in macOS Keychain — completely separate from SSH keys or `GITHUB_PAT_TOKEN`

2. When `--ref` is omitted, `gh` calls GitHub's GraphQL API to determine the repo's default branch. That call returned 401 Bad credentials — a transient auth issue (possibly token refresh race, GitHub API hiccup, or proxy glitch through mihomo)

3. Your `gh auth status` was fine then and is fine now. The command works now without any changes.

To avoid this in the future, you can pin the ref so `gh` doesn't need to query the default branch:

```bash
ww action gh-pages.yml --ref main
```

Also note: `GITHUB_PAT_TOKEN` (used by `ww github` commands for GraphQL) works for REST but fails for GraphQL. That's a separate issue — your PAT likely lacks the right scopes for GraphQL. The `gh` CLI token works for both. If you want `ww github` commands to work too, you'd need to regenerate the PAT with proper scopes or switch `github_mgmt.py` to fall back to `gh auth token`.
