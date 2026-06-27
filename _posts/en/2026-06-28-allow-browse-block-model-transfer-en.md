---
audio: false
generated: true
image: false
lang: en
layout: post
title: Allow Browse, Block Model Transfer
translated: false
type: note
---

Question: When using Symantec Web Filter (Blue Coat ProxySG) for a corporate proxy, can we write a special rule for huggingface.co that allows staff to browse/explore the site but blocks pushing or pulling models?

Answer:

Yes — but you can't do it with a single domain rule. The trick is that "browsing" and "model transfer" on Hugging Face split across **different hostnames and HTTP methods**, so you filter on those, not on `huggingface.co` as a whole.

## How HF traffic actually splits

| Activity | Host / path | Method |
|---|---|---|
| Browse model cards, search, docs | `huggingface.co` (HTML, `/models`, `/datasets`) | `GET` |
| Web UI XHR/API | `huggingface.co/api/...` | `GET` |
| **Pull** (download weights) | `cdn-lfs.huggingface.co`, `cdn-lfs-us-1.huggingface.co`, `*.hf.co`, LFS pointers resolve to these | `GET` (large) |
| Resolve file blobs | `huggingface.co/.../resolve/...` | `GET` |
| **Push** (upload weights) | `huggingface.co/.../*.git/...`, LFS `POST/PUT` to `cdn-lfs*` | `POST`, `PUT` |
| Git operations | `huggingface.co/<repo>.git/info/refs?service=git-receive-pack` (push) vs `git-upload-pack` (pull) | `GET`/`POST` |

This is the key lever: **git smart-HTTP exposes intent in the URL**. `git-upload-pack` = clone/pull, `git-receive-pack` = push.

## Recommended ProxySG / WebFilter policy (CPL)

Allow the site category, then layer method/host/path exceptions. Order matters — most specific deny first.

```
<Proxy>
; --- Block model pushes (git receive-pack + LFS uploads) ---
url.host=huggingface.co url.path.regex="git-receive-pack" deny
request.method=(POST,PUT) url.host.regex="cdn-lfs.*\.huggingface\.co" deny
request.method=(POST,PUT) url.host.regex="cdn-lfs.*\.hf\.co" deny

; --- Block model pulls (weight downloads via LFS CDN + resolve endpoint) ---
url.host.regex="cdn-lfs.*\.huggingface\.co" deny
url.host.regex="cdn-lfs.*\.hf\.co" deny
url.path.regex="/resolve/" deny
url.path.regex="git-upload-pack" deny

; --- Allow everything else on the main domain (browsing, search, docs, API) ---
url.host=huggingface.co allow
url.host=hf.co allow
</Proxy>
```

Effect: staff can read model cards, datasets, docs, and the API-driven UI, but any actual blob transfer (`/resolve/`, LFS CDN) and any git push/pull is blocked.

## Things that will bite you

1. **HTTPS = SSL interception required.** All HF traffic is TLS. Without SSL interception (MITM) on ProxySG, you can only filter on **SNI hostname**, not path or method. That means you *can* block `cdn-lfs*.huggingface.co` (kills downloads + uploads) but you **cannot** distinguish `git-upload-pack` from `git-receive-pack`, nor block `/resolve/`. So:
   - **No SSL interception** → easiest policy is: allow `huggingface.co`, deny all `cdn-lfs*` hosts. Browsing works, downloads die (because weights live on the CDN), uploads die too. You lose the "allow pull, block push" granularity but you get "allow browse, block transfer."
   - **With SSL interception** → full path/method control as in the CPL above.

2. **`hf_transfer` / CLI fallbacks.** `huggingface-cli download` and `hf_hub_download` hit `cdn-lfs*` for the actual bytes, so the CDN deny catches them. But watch for `HF_ENDPOINT` overrides and any mirror configs staff might set.

3. **Small files slip through.** Config files, tokenizer JSON, and tiny model shards under the LFS threshold are served directly from `huggingface.co/.../resolve/`, not the CDN. If you only block the CDN host, those still download. Block `/resolve/` (needs SSL interception) to be thorough.

4. **xet backend.** HF is migrating large-file storage to Xet (`*.xethub.hf.co` / `cas-*.huggingface.co`). Add those hosts to your CDN deny list or downloads via the new path will bypass `cdn-lfs` rules.

## Sanity-test from a client behind the proxy

```bash
# Should succeed (browse)
curl -sI https://huggingface.co/models | head -1

# Should be blocked (pull)
huggingface-cli download gpt2 --quiet || echo "pull blocked ✓"

# Should be blocked (push) — dry run
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/<​USER>/<​REPO> && \
  cd <​REPO> && git push 2>&1 | grep -qi deny && echo "push blocked ✓"
```

Bottom line: the clean "explore yes, transfer no" policy needs SSL interception. Without it, deny the `cdn-lfs*` / xet CDN hosts and accept that you're blocking *all* model transfer, not just push.
