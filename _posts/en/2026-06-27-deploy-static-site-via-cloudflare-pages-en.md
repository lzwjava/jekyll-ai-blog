---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploy Static Site via Cloudflare Pages
translated: false
type: note
---

Question: How do I serve a simple `index.html` using Cloudflare?

Answer:

Use **Cloudflare Pages**. It's free, serves static files directly from a repo or direct upload, and gives you a `*.pages.dev` domain plus optional custom domain — no server needed.

## Fastest path: direct upload (no Git)

```bash
npm install -g wrangler
wrangler login            # opens browser to auth

mkdir my-site && cd my-site
echo "<h1>SEC EDGAR GPT</h1>" > index.html

# deploy the current dir as a Pages project
wrangler pages deploy . --project-name=sec-edgar-gpt
```

Output gives you `https://sec-edgar-gpt.pages.dev`. Re-run `wrangler pages deploy .` to update.

## Git-connected (auto-deploy on push)

Dashboard → Workers & Pages → Create → Pages → Connect to Git → pick `lzwjava/sec-edgar-gpt`.

Build settings for a plain static site:

```
Framework preset:    None
Build command:       (leave empty)
Build output dir:    /          # or /docs if index.html lives there
```

Every `git push` to the production branch redeploys. Live at `<project>.pages.dev`.

## Custom domain

Pages → your project → Custom domains → add `sec-edgar-gpt.lzwjava.com`. If `lzwjava.com`'s nameservers are already on Cloudflare, the DNS CNAME is created automatically and HTTPS is provisioned for you. No A records, no cert juggling.

## Pages vs Workers — pick the right tool

- **Cloudflare Pages** → static `index.html` + assets. This is your case.
- **Cloudflare Workers** → if you later want server-side logic (an API endpoint, an LLM proxy for the EDGAR tool). You can serve static assets from a Worker too, but for a pure landing page Pages is simpler.

## Pages vs GitHub Pages for your paper site

Both are free and static. Cloudflare wins if: you want faster global edge caching, you're already on Cloudflare DNS, or you'll later bolt on a Worker (e.g. a `/query` endpoint hitting an LLM). GitHub Pages wins if you want everything in one place with the repo. For `sec-edgar-gpt` specifically — where you might want a live demo calling an LLM — I'd lean Cloudflare so the Worker upgrade path is one step away.

References:

- [Cloudflare Pages — Direct Upload with Wrangler](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Cloudflare Pages — Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/)
