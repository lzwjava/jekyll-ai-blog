---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add AdSense to Jekyll Blog
translated: false
type: note
---

Question: How do I add Google AdSense to my Jekyll blog (lzwjava/jekyll-ai-blog) to monetize it?

Answer:

Your site is static Jekyll on GitHub Pages, so AdSense integration is just a script tag + `ads.txt`. No SDK, no server. Here's the exact diff based on your repo's actual structure.

**1. Apply for AdSense first** — you need approval before ads render. Go to ads.google.com, add `lzwjava.github.io` as a site, wait for review (can take days-weeks). You'll get a publisher ID like `pub-1234567890123456`.

**2. Add `ads.txt` at repo root** (required by Google, or you lose revenue to "unauthorized sellers" warnings):

```bash
cat > /path/to/repo/ads.txt << 'EOF'
google.com, pub-<PLACEHOLDER_PUB_ID>, DIRECT, f08c47fec0942fa0
EOF
```

**3. Add Auto Ads script to `<head>`** in `_layouts/default.html` — insert right after your existing GoatCounter script, before `</head>`:

```diff
   <script data-goatcounter="https://lzwjava.goatcounter.com/count"
         async src="//gc.zgo.at/count.js"></script>
+
+  <!-- Google AdSense -->
+  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-<PLACEHOLDER_PUB_ID>"
+     crossorigin="anonymous"></script>
 </head>
```

That alone enables Auto Ads (Google decides placement). If you want more control and better revenue, add manual in-article units.

**4. Manual in-article ad unit** — in `_layouts/post.html`, drop a unit right before the closing `<hr>` after `{{ content }}` (post-content boundary, decent CTR spot):

{% raw %}

```diff
   {{ content }}

+  <div class="ad-container" style="margin: 24px 0; text-align:center;">
+    <ins class="adsbygoogle"
+         style="display:block"
+         data-ad-client="ca-pub-<PLACEHOLDER_PUB_ID>"
+         data-ad-slot="<PLACEHOLDER_SLOT_ID>"
+         data-ad-format="fluid"
+         data-ad-layout-key="-gw-3+1f-3d+2z"></ins>
+    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
+  </div>
+
   <hr>
```

{% endraw %}

Get `data-ad-slot` from AdSense dashboard → Ads → By ad unit → In-article ad → create one.

**5. Deploy** — your existing GH Actions workflow (`gh-pages.yml`) handles the build/deploy, no changes needed there. Just commit and push.

**Notes specific to your setup:**

- `google_analytics: "UA-66656236-1"` in `_config.yml` is Universal Analytics — that's been sunset since 2023 and does nothing now. Worth swapping for GA4 or dropping it since you already have GoatCounter for real analytics.
- Since your blog is bilingual (`-en`/`-zh`) and AI-translated content, be aware AdSense's policy on "auto-generated content" — pages flagged as `page.generated: true` and `page.translated: true` in your frontmatter could get flagged in a manual review if there's too much unedited AI output. Not a hard blocker but worth knowing.
- At current traffic (2 stars/1 watcher on the repo isn't a traffic signal, but if your `notes` pages — 1992 of them — get real search traffic, that long-tail content is actually where AdSense earns most, since it's indexed niche technical content).

Alternative worth considering given your AI-agent background: skip display ads entirely and monetize via a sponsor/affiliate block (e.g. tools you build — `ww`, `iclaw`, `zz` — or GPU/consulting CTA) since your traffic profile (engineers reading technical notes) converts far better to consulting leads than to $0.50 CPM display ads.

References:

- [Google AdSense - Get started](https://support.google.com/adsense/answer/9711326)
- [ads.txt guide](https://support.google.com/adsense/answer/7532444)
- [Auto ads documentation](https://support.google.com/adsense/answer/9261307)
