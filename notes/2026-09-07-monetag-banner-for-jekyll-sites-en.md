---
audio: false
generated: true
image: false
lang: en
layout: post
title: Monetag Banner for Jekyll Sites
translated: false
type: note
---

Question: How do I put a **normal display banner** from Monetag on my site?

Answer: Use Monetag's **Display Banner / Banner** ad unit and embed the generated JavaScript snippet into your Jekyll layout.

For your Jekyll site, the basic structure is:

```html
<!-- Monetag display banner -->
<div class="ad-container">
  <script src="MONETAG_SCRIPT_URL"></script>
</div>
```

In practice, Monetag gives you the exact `<script>` code after you create the ad zone. You **should not manually construct the script URL**.

### For `lzwjava.com`

I'd put one banner in the article rather than making every click an ad:

```text
┌──────────────────────────────────────┐
│                                      │
│        Your article content          │
│                                      │
├──────────────────────────────────────┤
│             ADVERTISEMENT            │
│          [ Monetag banner ]          │
├──────────────────────────────────────┤
│                                      │
│        Continue reading...           │
│                                      │
└──────────────────────────────────────┘
```

For Jekyll, a clean implementation is:

```text
_includes/
    monetag-banner.html
```

```html
<div class="monetag-banner">
  <!-- paste Monetag's generated banner code here -->
</div>
```

Then wherever you want the ad:

{% raw %}

```liquid
{% include monetag-banner.html %}
```

{% endraw %}

For example, inside your post layout:

{% raw %}

```text
_layouts/post.html

<header>...</header>

<article>
  {{ content }}
</article>

{% include monetag-banner.html %}
```

{% endraw %}

I'd **not** use OnClick/SmartLink for this. A conventional banner is much more predictable: the user sees the ad, and **only an intentional click opens the advertiser**.

If you show me a screenshot of your Monetag dashboard's **Ad Formats / Create Zone** page, I can tell you exactly which option to select and where to put the generated code.
