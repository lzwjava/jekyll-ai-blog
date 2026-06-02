---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Domain Verification Guide
translated: false
type: note
---

Question: How do I create and deploy a WeChat verification file for my blog, and when does WeChat require such verification?

Answer:

## 1. What you need to do

You were given a file like:

```
198976a221b3bd8c.txt
```

with content:

```
5354e
```

This is a **domain ownership verification file** required by WeChat.

### ✅ Step-by-step

#### Step 1 — Create the file locally

Inside your repo (`/Users/lzwjava/projects/lzwjava.github.io`):

```bash
cd /Users/lzwjava/projects/lzwjava.github.io

echo "5354e" > 198976a221b3bd8c.txt
```

#### Step 2 — Place it at the root

Make sure the file is at the **root of your deployed site**, not inside a subfolder:

```
lzwjava.github.io/
├── index.html
├── 198976a221b3bd8c.txt   ✅ MUST be here
├── ...
```

#### Step 3 — Commit and push

```bash
git add 198976a221b3bd8c.txt
git commit -m "Add WeChat verification file"
git push
```

Your GitHub Pages workflow (`.github/workflows/gh-pages.yml`) will deploy it automatically.

---

## 2. Verify deployment

After deployment, test:

```
https://lzwjava.github.io/198976a221b3bd8c.txt
```

It should return exactly:

```
5354e
```

⚠️ No HTML, no formatting, no newline issues ideally.

---

## 3. Important GitHub Pages details

Check your workflow (`gh-pages.yml`) to ensure:

* It does NOT exclude `.txt` files
* It copies **all root files** to the final build output

If you are using a static generator (like Jekyll, Hexo, etc.):

* Put the file in:

  * `public/` (Hexo)
  * `_site/` (Jekyll output)
  * or root static folder

Example for Hexo:

```bash
cp 198976a221b3bd8c.txt source/
```

---

## 4. When does WeChat require this?

WeChat requires this verification in several scenarios:

### 1. WeChat Official Account (公众号)

When you:

* Bind a **website domain** to your account
* Enable features like:

  * JS-SDK (sharing, payments)
  * OAuth login

👉 They must confirm you **own the domain**

---

### 2. WeChat Open Platform (开放平台)

When configuring:

* Website App login
* UnionID system
* Third-party integrations

---

### 3. WeChat Mini Program (小程序)

When using:

* Web-view pages
* Business domain configuration

---

### 4. WeChat Pay (微信支付)

When setting:

* Payment callback URLs
* API endpoints

---

## 5. Why this method?

WeChat uses this simple method because:

* No DNS access required
* Easy to verify ownership
* Similar to:

  * Google Search Console
  * Cloudflare domain verification

---

## 6. Common mistakes (very important)

* ❌ Putting file in subdirectory (`/assets/` etc.)
* ❌ File content mismatch (extra spaces/newlines)
* ❌ Not publicly accessible (private repo or blocked)
* ❌ Using wrong domain (e.g., `www` vs non-`www`)
* ❌ GitHub Pages caching delay (wait 1–2 min)

---

## 7. Quick checklist

* File exists at root ✅
* Content matches exactly ✅
* Accessible via URL ✅
* HTTPS works ✅

---

If you want, I can also:

* Inspect your `gh-pages.yml` and ensure it won't strip the file
* Help automate verification file injection during CI/CD
* Or set up multi-domain verification strategy (useful for scaling traffic via WeChat SEO-like distribution)
