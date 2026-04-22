---
audio: false
generated: true
image: false
lang: en
layout: post
title: Marp's Fullscreen Presentation API
translated: false
type: note
---

Question: Why does Marp HTML export run in full screen in Safari, what technology does it use, and why normal HTML doesn’t have a full-screen option?

Answer:

Marp’s HTML export works in full-screen mode in Safari because it is built on top of the **browser Fullscreen API** plus a slide-style presentation layout (essentially a web app designed for presentations).

### 1. What Marp actually exports

Marp doesn’t export “just HTML pages” in the traditional sense. It exports a **presentation web app**, which typically includes:

* A single HTML file (or a small bundle)
* CSS that turns each “slide” into a full viewport page (`100vw × 100vh`)
* JavaScript to handle navigation (arrow keys, click, etc.)
* A fullscreen trigger button

So it behaves more like:

> a mini PowerPoint running inside a browser

---

### 2. The key technology: Fullscreen API

Marp uses the browser’s built-in:

* **Fullscreen API**

  * `element.requestFullscreen()`
  * `document.exitFullscreen()`

When activated, Safari (and other browsers) can:

* Hide address bar / tabs
* Expand the content to fill the screen
* Lock focus on the presentation element

This is why Marp can feel like a native presentation app.

---

### 3. Why Safari allows this nicely

Safari supports Fullscreen API well for:

* video players
* presentations
* web apps (like slides)

Marp likely targets a full-screen `<div>` container, for example:

```js
document.documentElement.requestFullscreen()
```

or a slide container like:

```js
slideContainer.requestFullscreen()
```

Once activated, Safari switches into a “presentation mode-like” state.

---

### 4. Why “normal HTML” doesn’t automatically go full screen

Normal HTML pages do NOT enter fullscreen because:

#### (1) Security restriction

Fullscreen must be:

* triggered by a **user action** (click, key press)
* not automatically on page load

So normal websites just stay inside the browser UI.

---

#### (2) No layout enforcement

Regular HTML:

* is not designed to occupy full viewport intentionally
* doesn’t force slide-like dimensions (`100vh`)
* scrolls instead of paging

So even if fullscreen is enabled, it still looks like a webpage unless designed for it.

---

#### (3) Fullscreen is not default behavior

Browsers assume:

* users want tabs, address bar, navigation controls
* fullscreen is “opt-in immersive mode”

---

### 5. Why Marp feels different from normal HTML

Marp adds the missing pieces:

| Feature           | Normal HTML      | Marp HTML            |
| ----------------- | ---------------- | -------------------- |
| Fullscreen API    | Optional         | Actively used        |
| Layout            | Flowing document | Fixed slide viewport |
| Navigation        | Scroll           | Slide-based (JS)     |
| Presentation mode | None             | Built-in             |

So Marp is basically:

> HTML + CSS + JS + Fullscreen API = presentation engine

---

### 6. Why it works especially well in Safari

Safari tends to:

* aggressively optimize fullscreen rendering
* treat fullscreen elements like “app-like surfaces”
* smooth out scaling for fixed-layout pages

So Marp’s slide structure aligns perfectly with Safari’s fullscreen behavior.

---

If you want, I can break down how to build a mini “Marp-like” system yourself using just HTML + CSS + 20 lines of JavaScript.