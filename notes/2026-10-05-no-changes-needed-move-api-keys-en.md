---
audio: false
generated: true
image: false
lang: en
layout: post
title: No Changes Needed; Move API Keys
translated: false
type: note
---

**No changes needed — everything is already present on `lzw@192.168.1.34`.**

## Check results

`~/.bashrc` (line 137, "Proxy Functions" block):

| Function | Line | Status |
| ---------- | ------ | -------- |
| `start_proxy` | 139 | ✅ present |
| `start_proxy_without_prefix` | 151 | ✅ present |
| `stop_proxy` | 163 | ✅ present |
| `start_git_proxy` | 176 | ✅ present |
| `stop_git_proxy` | 181 | ✅ present |
| `checkproxy` | 186 | ✅ present |

Also mirrored in `~/.profile` (lines 33/45/70), so login shells get them too.

## Details

- Proxy is configured via `GLOBAL_PROXY='127.0.0.1:7890'` (line 137) — both functions read from this variable.
- `start_proxy` sets `http_proxy`/`https_proxy`/`ftp_proxy`/`ALL_PROXY` with the `http://` prefix.
- `start_git_proxy` sets `git config --global http.proxy` and `https.proxy` to `$GLOBAL_PROXY`.
- `NO_PROXY`/`no_proxy` are exported with local/private ranges excluded.

One heads-up: your `~/.bashrc` on that machine has plaintext Cloudflare API keys on lines 131–132 (`CLOUDFLARE_API_KEY`, `CLOUDFLARE_API_TOKEN`). Consider moving those into a separate non-tracked file (e.g. `~/.secrets.env` sourced from bashrc) or using `ww sync`'s pattern for keeping them out of shell config.
