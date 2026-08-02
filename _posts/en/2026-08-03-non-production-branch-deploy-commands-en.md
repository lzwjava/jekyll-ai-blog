---
audio: false
generated: true
image: false
lang: en
layout: post
title: Non-production branch deploy commands
translated: false
type: note
---

The short answer: **for non-production branches, use `npx wrangler versions upload`** — that's actually the default, so you can leave the field empty.

## What that command does

Workers Builds (the Git → Worker CI/CD you're configuring) runs a two-step process:

1. **Build command** (optional) — compiles your project
2. **Deploy command** — deploys the Worker, defaults to `npx wrangler deploy`

For commits to any branch **other than your production branch** (e.g. `develop`, `nw`, `test` in this repo), the deploy command is swapped for the **Non-production branch deploy command**, which:

- Defaults to `npx wrangler versions upload`
- Uploads the build as a **version with a preview URL** (visible under Version History → View build)
- Does **not** promote it to the active production deployment — safe to test before merging

So unless you need something custom, just leave the default.

## When you'd customize it

| Situation | Non-production branch deploy command |
|---|---|
| Default (recommended) | `npx wrangler versions upload` |
| Different package manager | `yarn exec wrangler versions upload` |
| Deploy previews to a staging env instead | `npx wrangler versions upload --env staging` |

## ⚠️ Important caveat for *this* project

This repo is a **Jekyll static blog**, not a Worker:

- There is **no `wrangler.jsonc`/`wrangler.toml`**, no worker source, and no `wrangler` dependency in `package.json`
- Workers Builds requires a wrangler config whose `name` matches the Worker name in the dashboard, or the build fails
- With no config, `npx wrangler deploy` triggers **autoconfig**, which opens a PR creating Worker scaffolding for you — likely not what you want for a Jekyll site

For this project, **Cloudflare Pages** is the right product instead:

- **Build command:** `bundle install && bundle exec jekyll build`
- **Output directory:** `_site`
- **Non-production branches:** Pages automatically runs the same build command for previews and gives each branch a `*.pages.dev` preview URL — no separate deploy command needed

If you still want it on Workers (e.g. to serve the static site from a Worker with the assets binding), you'd need to add a wrangler config first. Want me to scaffold that?