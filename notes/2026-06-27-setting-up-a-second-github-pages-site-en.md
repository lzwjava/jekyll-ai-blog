---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Up a Second GitHub Pages Site
translated: false
type: note
---

Question: I already have one `*.github.io` site (my blog). I want a second GitHub Pages site for my `sec-edgar-gpt` repo, served at a different URL. How do I do that?

Answer:

You're conflating two things. GitHub gives you **one user site** (`lzwjava.github.io`) but **unlimited project sites**. Your `sec-edgar-gpt` repo gets a project site automatically at:

```
https://lzwjava.github.io/sec-edgar-gpt
```

That's a *path* on the same domain, not a new subdomain. GitHub Pages doesn't give you `sec-edgar-gpt.github.io` — only `<username>.github.io` exists per account.

## Option 1: Project page (zero extra cost, do this first)

Enable Pages on the repo:

```bash
# repo Settings → Pages → Source: deploy from branch (main, /root or /docs)
# or push a gh-pages branch
```

If you have an `index.html` or a `docs/` folder, set the source accordingly. Done — live at `lzwjava.github.io/sec-edgar-gpt`.

## Option 2: Custom domain (what you actually want)

Buy a domain (or use a subdomain of one you own) and point it at the project repo. Each repo can have its **own** custom domain via a `CNAME` file.

```bash
# in the sec-edgar-gpt repo root (or /docs)
echo "sec-edgar-gpt.lzwjava.com" > CNAME
git add CNAME && git commit -m "custom domain" && git push
```

DNS side — for a **subdomain**, add a CNAME record at your DNS provider:

```
Type    Name             Value
CNAME   sec-edgar-gpt    lzwjava.github.io.
```

For an **apex domain** (`example.com`) you'd use A records pointing to GitHub's IPs instead:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Then in repo Settings → Pages → Custom domain, enter the domain and check "Enforce HTTPS" once the cert provisions (can take ~15 min to a few hours).

## Key constraint to know

Your blog already occupies `lzwjava.github.io` as the **user site**. Adding a custom domain to a *project* repo doesn't touch that — they're independent. You can give every project its own subdomain (`sec-edgar-gpt.lzwjava.com`, `ww.lzwjava.com`, etc.) all from one DNS zone.

## Recommendation for your trajectory

Since you maintain a knowledge base and ship lots of tools, set up a wildcard pattern: own `lzwjava.com`, point `*.lzwjava.com` via individual CNAMEs to `lzwjava.github.io`, and give each project its own subdomain. Clean, scalable, and the paper site becomes `sec-edgar-gpt.lzwjava.com`.

If you don't want to buy a domain, just use Option 1 — `lzwjava.github.io/sec-edgar-gpt` works fine for a paper landing page.

References:

- [GitHub Pages — Types of sites](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
- [Managing a custom domain for your GitHub Pages site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
