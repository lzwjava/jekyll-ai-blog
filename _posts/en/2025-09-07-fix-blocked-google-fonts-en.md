---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Fixing Blocked Google Fonts Request
translated: false
type: note
---

That request is your page trying to load a webfont stylesheet from Google Fonts:

* **What it is:** `https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap` is the CSS that defines the **Open Sans** font faces. Your theme or custom CSS is including it so the site can render in Open Sans.
* **Why you see “Status: — / 0 B / no headers”:** DevTools shows that when the request is **blocked or canceled** (e.g., by an ad-/privacy-blocker, a strict Content-Security-Policy, a flaky network, or country-level blocking). The page still *tries* to request it, hence the network row.

### Where it likely comes from in a Jekyll blog

One of these is usually true:

1. **Theme includes it in the `<head>`**
   Look for a line like
   `<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap" rel="stylesheet">`
   in `_layouts/default.html` or `_includes/head.html` (or the theme’s equivalent if you use `remote_theme`).

2. **SCSS imports it**
   Check `/assets/css/*.scss` or `/_sass/**` for
   `@import url("https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap");`

3. **Remote theme** (e.g., jekyll-theme-cayman) hardcodes Google Fonts in its head include. Overriding the theme’s head/layout in your repo will let you remove it.

### How to find it fast

From your site repo root, try any of:

```
rg -n "fonts.googleapis.com"
rg -n "Open Sans"
rg -n "display=swap"
```

### Options to fix or change it

**A) Remove Google Fonts and use a system font stack (fastest & privacy-friendly)**

1. Delete the `<link>` (or the SCSS `@import`) that pulls Google Fonts.
2. In your main stylesheet, set a system stack:

   ```css
   html, body {
     font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu,
                  "Helvetica Neue", Arial, "Noto Sans", sans-serif,
                  "Apple Color Emoji", "Segoe UI Emoji";
   }
   ```

   (In Jekyll, put this in `assets/css/style.scss` with front-matter `---` lines at the top.)

**B) Keep Open Sans but self-host it**

1. Download WOFF2 files for Open Sans (400 & 700) and place them under `assets/fonts/`.
2. Add to your CSS:

   ```css
   @font-face {
     font-family: "Open Sans";
     font-style: normal;
     font-weight: 400;
     font-display: swap;
     src: url("/assets/fonts/OpenSans-400.woff2") format("woff2");
   }
   @font-face {
     font-family: "Open Sans";
     font-style: normal;
     font-weight: 700;
     font-display: swap;
     src: url("/assets/fonts/OpenSans-700.woff2") format("woff2");
   }
   body { font-family: "Open Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
   ```

3. Remove the Google Fonts `<link>`/`@import`.

**C) Leave it as-is but stop the request from failing**

* Disable the blocking extension for your site, or loosen your CSP to allow `https://fonts.googleapis.com` and `https://fonts.gstatic.com`.
* If you’re in a region where those domains are blocked, prefer A or B.

### Jekyll-specific override tips

* **Remote theme:** copy the theme’s `/_includes/head.html` or `/_layouts/default.html` into your repo with the same path, remove the Google Fonts line, and Jekyll will use your override.
* **Minified head include:** sometimes the theme injects fonts via a variable. If so, set that variable to empty or override the include to exclude fonts.

If you paste your theme name (or your `_config.yml` `theme` / `remote_theme`) I can show the exact file to override and the minimal diff.
