---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare credentials for GitHub Actions
translated: false
type: note
---

Question: Are these dashboard steps for getting `CLOUDFLARE_ACCOUNT_ID` / `CLOUDFLARE_API_TOKEN` and wiring them into GitHub Actions correct for `wrangler deploy`?

Answer: Yes, that's the current flow. Confirmed against Cloudflare's docs:

**Account ID** — to find your Cloudflare account ID, refer to Find account and zone IDs. Zoom out to make sure your account (not a zone) is selected — the ID shown is a 32-char hex string in the right sidebar.

**API Token** — in the Cloudflare dashboard, go to the Account API tokens page, select Create Token, under Permission policies open the Custom dropdown and select Edit Cloudflare Workers, customize your token name, then scope your token to the specific account (don't leave it "All accounts" if you have multiple).

**GitHub secrets** — exactly as you have it: repo → `Settings → Secrets and variables → Actions → New repository secret`, add both `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN`.

One correction worth noting since it's a common footgun: don't store the value of CLOUDFLARE_API_TOKEN in your repository, as it gives access to deploy Workers on your account — instead use your CI/CD provider's support for storing secrets (which is exactly what you're doing).

Minimal workflow step once both secrets exist:

{% raw %}
```yaml
- name: Deploy Worker
  uses: cloudflare/wrangler-action@v4
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
    command: deploy
```
{% endraw %}

Or if you're calling `npx wrangler deploy` directly in a `run:` step instead of the action, just export both as env vars on that step:

{% raw %}
```yaml
- name: Deploy
  run: npx wrangler deploy
  env:
    CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```
{% endraw %}

Wrangler auto-detects these two env var names — no extra config needed for `jekyll-ai-blog`.

References:
- [GitHub Actions · Cloudflare Workers docs](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/)
- [cloudflare/wrangler-action](https://github.com/cloudflare/wrangler-action)