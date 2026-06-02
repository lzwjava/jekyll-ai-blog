---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Google Fonts Import in Cayman Theme
translated: false
type: note
---

Yes — that’s very likely the reason.

When you write:

```scss
@import "jekyll-theme-cayman";
```

you’re not just pulling in some local SCSS — you’re importing the entire **theme’s stylesheet**, which itself contains (or links to) the Google Fonts import. Cayman uses **Open Sans** as its default font, and it pulls it from `https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap`.

So the flow looks like this:

1. Your SCSS says `@import "jekyll-theme-cayman";`.
2. Jekyll expands that into the theme’s `_sass` files.
3. Inside Cayman’s SCSS, there’s a line like:

   ```scss
   @import url("https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap");
   ```
4. That’s the network request you’re seeing in DevTools.

---

### How to remove or override

* **Override the font import**: Copy the theme’s main SCSS into your project (e.g. `assets/css/style.scss`), delete the Google Fonts line, and tell Jekyll not to import it.

* **Just override the font family**: Keep the rest of Cayman but force a system font stack in your own CSS:

  ```css
  html, body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu,
                 "Helvetica Neue", Arial, "Noto Sans", sans-serif;
  }
  ```

  Even if the Google Fonts request happens, the browser won’t use it.

* **Self-host Open Sans**: If you like Open Sans but don’t want the external call, download the font files and define them with `@font-face` in your own CSS, then remove Cayman’s `@import url(...)`.

---

👉 If you want, I can show you exactly which Cayman SCSS file has the Google Fonts line and how to override it cleanly in your Jekyll setup. Do you want me to walk through that step by step?
