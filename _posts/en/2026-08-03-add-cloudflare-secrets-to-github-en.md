---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add Cloudflare Secrets to GitHub
translated: false
type: note
---

You're not logged in to wrangler on this machine, so the fastest path is the dashboard:

1. Go to **dash.cloudflare.com** and log in
2. Look at the **right sidebar** of the dashboard — you'll see a section with your account name and **Account ID** (32-char hex string) with a copy button

That's the value. Put it in GitHub as a repo secret alongside the API token:

- GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**
- Name: `CLOUDFLARE_ACCOUNT_ID` → value: your 32-char Account ID
- Name: `CLOUDFLARE_API_TOKEN` → value: the token from **My Profile → API Tokens → Create Token** (template "Edit Cloudflare Workers")

Once both secrets exist, `npx wrangler deploy` in the workflow will authenticate with the token and know exactly which account's `jekyll-ai-blog` Worker to update.