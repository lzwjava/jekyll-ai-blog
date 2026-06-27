---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploying with Cloudflare Pages
translated: false
type: note
---

Not installed. You can either:

**Option A: Cloudflare Dashboard (easiest)**

1. Go to Cloudflare Pages → Create project
2. Connect your GitHub repo `lzwjava/sec-edgar-gpt`
3. Set:
   - Build command: (leave empty)
   - Build output directory: `website`
4. Deploy

**Option B: Install wrangler and deploy from CLI**

```
npm install -g wrangler
wrangler pages deploy website --project-name=sec-edgar-gpt
```

Option A is simpler — just set the output directory to `website` in the dashboard.
