---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploy Jekyll Blog to Cloudflare Pages
translated: false
type: note
---

Question: How to deploy a Cloudflare website like `lzwjava/jekyll-ai-blog`?

Answer:

A Jekyll blog is a **static site**, so the best Cloudflare deployment path is:

```
GitHub repo
    |
    | push
    v
Cloudflare Pages build
    |
    | Jekyll build
    v
Static HTML/CSS/JS
    |
    v
Cloudflare CDN + custom domain
```

No VPS needed.

## 1. Prepare your Jekyll repo

Your repo:

```
https://github.com/lzwjava/jekyll-ai-blog
```

should have something like:

```
.
├── _config.yml
├── _posts/
├── index.md
├── Gemfile
├── Gemfile.lock
├── assets/
└── _layouts/
```

Test locally:

```bash
git clone https://github.com/lzwjava/jekyll-ai-blog.git
cd jekyll-ai-blog

bundle install
bundle exec jekyll serve
```

Open:

```
http://localhost:4000
```

---

## 2. Create Cloudflare Pages project

Go to:

Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git

Select:

```
GitHub
    |
    └── lzwjava/jekyll-ai-blog
```

---

## 3. Configure build settings

Cloudflare Pages needs:

### Framework preset

Choose:

```
Jekyll
```

or manually:

Build command:

```bash
bundle exec jekyll build
```

Output directory:

```
_site
```

Environment:

```
Ruby version: 3.2
```

---

## 4. Add Ruby dependencies

Your `Gemfile`:

```ruby
source "https://rubygems.org"

gem "jekyll"
gem "github-pages"
```

Commit:

```bash
git add Gemfile
git commit -m "setup cloudflare pages"
git push
```

Cloudflare automatically rebuilds.

---

## 5. Add custom domain

Example:

```
blog.example.com
```

Cloudflare:

```
Pages
 |
 └── Custom domains
        |
        └── Add domain
```

Cloudflare automatically creates:

```
CNAME

blog.example.com
        |
        v
your-project.pages.dev
```

---

## 6. Optional: GitHub Actions instead

Another architecture:

```
GitHub Actions
      |
      | bundle exec jekyll build
      |
      v
_site/
      |
      v
Cloudflare Pages deploy
```

Example:

`.github/workflows/deploy.yml`

{% raw %}
```yaml
name: deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'

      - run: bundle install
      - run: bundle exec jekyll build

      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          accountId: ${{ secrets.CF_ACCOUNT_ID }}
          directory: ./_site
```
{% endraw %}

---

## For your blog specifically

Your current architecture:

```
Jekyll
+
GitHub
+
Cloudflare CDN
```

is actually a very good setup for a technical AI blog.

Advantages:

* zero server maintenance
* global CDN
* HTTPS automatically
* Git-based publishing
* very cheap
* good SEO

A typical workflow:

```bash
vim _posts/2026-08-03-vllm-kernel.md

git add .
git commit -m "write vllm article"
git push
```

Then:

```
GitHub webhook
       |
       v
Cloudflare Pages rebuild
       |
       v
online in ~1 minute
```

For an AI engineer blog, this is probably the same deployment style used by many open-source projects: **Git as the database, static build as the application, CDN as the runtime.**
