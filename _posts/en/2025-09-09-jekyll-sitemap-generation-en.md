---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Generating Sitemap Files for Jekyll
translated: false
type: note
---

A **sitemap.xml** is an XML file that tells search engines like Google and Bing about the pages on your website. It helps crawlers discover and index your site’s structure more efficiently. For a Jekyll blog, this means search engines can find all your posts, pages, and translations (like your `index-zh.html`, `index-fr.html`, etc.) even if they’re not linked everywhere.

### What a Sitemap Does

* Lists all important URLs of your site.
* Provides metadata such as the last modified date (`<lastmod>`), change frequency (`<changefreq>`), and priority (`<priority>`).
* Improves SEO by ensuring crawlers don’t miss pages.

### How to Generate for Jekyll

You have a couple of approaches:

#### 1. Use the `jekyll-sitemap` plugin (recommended)

1. In your Jekyll project’s `Gemfile`, add:

   ```ruby
   gem 'jekyll-sitemap'
   ```
2. In your `_config.yml`, add:

   ```yaml
   plugins:
     - jekyll-sitemap
   ```

   (If you’re on GitHub Pages, `jekyll-sitemap` is already whitelisted, so it works directly.)
3. When you build (`jekyll build` or via `make` if you have it set up), Jekyll will automatically generate a `sitemap.xml` in your `_site/` folder.

#### 2. Manually create a sitemap template

If you prefer more control:

1. Create a file at the project root: `/sitemap.xml`.
2. Add this Liquid template:

{% raw %}
   ```xml
   ---
   layout: nil
   ---
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     {% for page in site.pages %}
       {% if page.sitemap != false %}
         <url>
           <loc>{{ site.url }}{{ page.url | replace:'index.html','' }}</loc>
           <lastmod>{{ page.date | date_to_xmlschema }}</lastmod>
         </url>
       {% endif %}
     {% endfor %}
     {% for post in site.posts %}
       <url>
         <loc>{{ site.url }}{{ post.url }}</loc>
         <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
       </url>
     {% endfor %}
   </urlset>
   ```
{% endraw %}
3. Make sure your `_config.yml` has `url: "https://yourdomain.com"` so links generate correctly.

#### 3. Verify

* After building, check `_site/sitemap.xml`.
* Submit it to Google Search Console for better indexing.

---

👉 Since you already have `_config.yml` and `_plugins/`, the easiest is to just enable `jekyll-sitemap`. That way, you won’t need to maintain the XML manually.

Do you want me to draft the exact `_config.yml` addition for your repo (based on your current files), so you can paste it directly?