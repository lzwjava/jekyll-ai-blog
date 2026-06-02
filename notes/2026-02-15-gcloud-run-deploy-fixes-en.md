---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix gcloud Run Deploy Command Errors
translated: false
type: note
---

Question: Why does the gcloud run deploy command with --source . give "unrecognized arguments" error, and how to fix it for deploying blog-server to Cloud Run?

Answer:

The error occurs because the shell (zsh in your case) is interpreting the flags after the first line break as separate commands instead of arguments to `gcloud`.

When you paste multi-line commands like this into the terminal:

```bash
gcloud run deploy blog-server \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi
```

zsh treats each line after the backslash as a new command if the continuation isn't handled correctly (common when copying from formatted text/markdown where line breaks are added).

This results in:
- `gcloud run deploy blog-server` runs (or partially runs)
- Then `--allow-unauthenticated` is seen as a standalone command → "command not found"
- Same for `--port`, `--memory`, etc.

The actual "unrecognized arguments" from gcloud likely comes from an incomplete/invalid invocation.

### How to fix it

**Option 1: Run it as a single line** (easiest and most reliable)

```bash
gcloud run deploy blog-server --source . --region asia-northeast1 --allow-unauthenticated --port 8080 --memory 1Gi
```

**Option 2: Use proper line continuation in your terminal**

Paste or type it like this (ensure no extra spaces after `\`):

```bash
gcloud run deploy blog-server \
    --source . \
    --region asia-northeast1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi
```

- After each `\` there should be **only a newline** — no trailing spaces.
- Indentation on continued lines is optional but improves readability.

**Option 3: Put it in a shell script**

Create a file (e.g. `deploy.sh`):

```bash
#!/bin/bash
gcloud run deploy blog-server \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi
```

Then run:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Additional notes (as of February 2026)

- The flags you used are correct and supported for `gcloud run deploy --source .`:
  - `--source .` → builds from current directory (using your `Dockerfile` since it's present)
  - `--region`, `--allow-unauthenticated`, `--port`, `--memory` → all valid
- Make sure your gcloud is up to date (`gcloud components update`) — source-based deploy with Dockerfile has been stable for years.
- If you still get "unrecognized arguments" after fixing the line continuation, run `gcloud run deploy --help` to confirm the flags, or try without `--memory 1Gi` first (default is usually 512MiB or 1GiB depending on CPU).

After successful deploy, you'll see a service URL like `https://blog-server-XXXXXX.a.run.app`.

References:

- [Deploy services from source code | Cloud Run](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [gcloud run deploy reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy)
