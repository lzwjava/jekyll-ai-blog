---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Dark Mode Element Checklist
translated: false
type: note
---

When you implement a dark mode in an Angular frontend, you’ll usually start with `body`, `select`, and `option`, but there are quite a few other common HTML elements you’ll want to restyle so the theme feels consistent. Here’s a practical checklist:

### Page-Level and Containers

* `html`, `body` → background and text color.
* `div`, `section`, `article`, `aside`, `header`, `footer`, `main`, `nav` → set background and text colors (especially if they have default white backgrounds).

### Text and Headings

* `h1, h2, h3, h4, h5, h6` → make sure text is visible against dark background.
* `p`, `span`, `a` → adjust text color, link hover colors, and visited link states.

### Forms and Inputs

* `input[type="text"], input[type="password"], input[type="email"], textarea` → background, text color, and border.
* `input[type="checkbox"], input[type="radio"]` → sometimes need special handling for visibility.
* `select, option` → as you mentioned, both background and text color.
* `button` → background, border, and text color, plus hover/active states.
* `label` → ensure text contrasts with dark background.
* `fieldset, legend` → background and border.

### Lists and Tables

* `ul, ol, li` → text color.
* `table` → background, border color, and text color.
* `thead, tbody, tr, th, td` → individual adjustments for backgrounds and borders.

### Interactive Elements

* `details, summary` → background and text.
* `dialog` → background and text.
* `mark` → highlight colors should work on dark (default yellow may be too bright).

### Media and Misc

* `hr` → border color (default is often too light on dark).
* `code, pre` → background and text color for readability.
* `blockquote` → background and border color.
* `progress, meter` → track and value colors.

---

💡 **Best practice**: Instead of using `!important` everywhere, define CSS variables for colors (`--bg-color`, `--text-color`, etc.) and swap them when dark mode is active (e.g., add a `.dark-mode` class to `body`). That way, Angular components and custom elements can also hook into the theme cleanly.

Would you like me to draft a **base CSS snippet** for dark mode (with variables) that you can drop into your Angular project as a starting point?
