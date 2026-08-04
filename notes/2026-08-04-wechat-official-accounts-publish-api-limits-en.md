---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Official Accounts Publish API Limits
translated: false
type: note
---

Question: WeChat Official Account doesn't support an API to publish articles, right?

Answer: **Mostly correct — WeChat Official Accounts do not provide a general public API that allows normal accounts to directly publish articles to the public platform.** However, there are some limited publishing APIs.

The situation:

### 1. Normal WeChat Official Account (公众号)

For most accounts:

* ✅ API to:

  * upload images/materials
  * manage menus
  * get followers
  * send template/service messages (with restrictions)
  * manage drafts (newer APIs)
* ❌ No unrestricted "publish this article now" API

Historically, the workflow is:

```
Your CMS
    |
    v
WeChat API
    |
    v
Draft article
    |
    v
Human clicks "Publish" in WeChat Admin UI
```

The final publish step usually requires manual confirmation.

---

### 2. WeChat API has draft + publish interfaces

Tencent introduced content publishing APIs for some scenarios.

Typical flow:

```
POST /cgi-bin/material/add_news
        |
        v
create draft
        |
        v
POST /cgi-bin/freepublish/submit
        |
        v
publish
```

The endpoint:

```
https://api.weixin.qq.com/cgi-bin/freepublish/submit
```

allows submitting drafts for publication.

But requirements apply:

* account must have the required permissions
* account type matters
* some features require verification
* rate limits apply

Many small personal公众号 accounts cannot use it.

---

### 3. Why WeChat restricts this

WeChat's ecosystem is different from blogs/Twitter:

If anyone could do:

```python
wechat.publish(
    title="xxx",
    content="spam"
)
```

then millions of bots could flood:

* spam articles
* fake news
* SEO farms
* phishing pages

So Tencent keeps publishing behind account permissions and review.

---

### 4. Common automation architecture

Large publishers usually build:

```
Markdown
   |
   v
CMS
   |
   +--> Jekyll / Hugo blog
   |
   +--> WeChat formatter
           |
           v
       Draft API
           |
           v
       WeChat Admin approval
```

Tools like:

* Markdown → 微信排版
* mdnice
* OpenWrite
* 自建 CMS

usually automate **formatting + draft creation**, not fully unattended publishing.

---

### 5. For your AI blog / community use case

Given you already run `lzwjava.github.io` and AI content:

A practical pipeline would be:

```
GitHub Markdown
       |
       v
GitHub Actions
       |
       +--> Jekyll website
       |
       +--> Generate WeChat HTML
                    |
                    v
              Upload draft to 公众号
                    |
                    v
              One-click publish
```

You can automate 95% of the process, but keep the final publish action manual unless your公众号 has the necessary API permissions.

References:

* WeChat Official Account API documentation: [https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
* WeChat Free Publish API: [https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html](https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html)
