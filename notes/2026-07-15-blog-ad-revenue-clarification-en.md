---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blog Ad Revenue Clarification
translated: false
type: note
---

Question: Clarifying — you want ads displayed on your own blog to earn revenue, not to advertise elsewhere, correct?

Answer: Yes — that's exactly what my last answer does. To be clear about what each piece does:

- **`ads.txt`** — this isn't about "sharing" ads anywhere. It's a file Google requires *on your own domain* (`lzwjava.github.io/ads.txt`) that says "I, pub-XXXX, authorize Google to sell ad space on this site." Without it, Google won't serve ads on your pages at all. It's a prerequisite, not a separate ad placement.
- **The `<script>` in `_layouts/default.html`** — this is the actual thing that makes ads appear on your blog pages. It loads Google's ad library on every page (since `default.html` is the base layout all pages inherit).
- **The `<ins class="adsbygoogle">` block in `post.html`** — this is a literal ad slot that renders *inside your blog posts*, between the content and the footer. This is the ad the reader sees on your site.

So the full flow is:
1. Apply at ads.google.com → get approved for `lzwjava.github.io`
2. Get your `pub-XXXXXXXXXXXXXXXX` ID
3. Drop `ads.txt` at repo root
4. Add the script tag to `_layouts/default.html` head
5. Add the `<ins>` ad unit to `_layouts/post.html`
6. Push → GitHub Pages rebuilds → ads show on your blog posts

There's no step here that sends your content or ads to another site. AdSense just injects ad `<iframe>`s into your own pages, and Google pays you per impression/click on your traffic.

If instead you meant something different — like embedding a banner for *your own* products (Fun Live, your AI consulting) rather than Google's network ads — that's a different, simpler build (just a static `<div>` with your own CTA, no AdSense approval needed, no revenue-share cut to Google). Which one do you actually want?
