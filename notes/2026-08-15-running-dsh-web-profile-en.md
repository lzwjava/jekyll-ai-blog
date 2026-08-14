---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running dsh web profile
translated: false
type: note
---

`npx @deepseek-ai/dsh web` **is** the run command — the "Ok to proceed?" prompt was just npx downloading the package into its cache; after it finishes, npx immediately executes it. Once cached, later runs won't re-prompt.

So, in `/mnt/data/bilingual-gpt`:

```sh
npx @deepseek-ai/dsh web
```

That boots the **web profile** (alias of `--profile web`): a server that serves the DeepSeek Harness browser UI.

Useful variants:

```sh
npx @deepseek-ai/dsh web --port 8080        # pick a port (0 = let the OS choose)
npx @deepseek-ai/dsh web --host 0.0.0.0     # bind host
npx @deepseek-ai/dsh web --help             # the web app's own flags
```

Notes:

- If the prompt annoys you, install once and skip npx entirely:

  ```sh
  npm install -g @deepseek-ai/dsh
  dsh web
  ```

- The agent is backed by real DeepSeek API calls, so export `DEEPSEEK_API_KEY` first (or put it in a `.env`), or the web UI won't be able to answer anything.
- Without `--port`, it serves on the profile's composed host/port (configurable via a profile patch; the server prints where it's listening when it starts).

Then open the printed URL (commonly `http://localhost:3080`) in your browser.
