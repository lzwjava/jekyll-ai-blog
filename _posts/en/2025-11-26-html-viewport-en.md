---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding the HTML Viewport
translated: false
type: note
---

Here’s a clear and practical way to understand the **viewport** in HTML/CSS, especially the differences you’re noticing between mobile phones and desktop browsers (like Safari on macOS).

### 1. What is the Viewport?
The viewport is **the area of the web page that is currently visible to the user** inside the browser window (or screen).

It is **NOT** the entire web page — it’s just the visible portion at any given moment.

### 2. Two Different Kinds of Viewport You’re Seeing

| Situation                  | What “viewport” means                              | Typical size on mobile | Typical size on desktop |
|----------------------------|----------------------------------------------------|------------------------|-------------------------|
| **Mobile browsers** (iPhone Safari, Chrome on Android, etc.) | The **layout viewport** (the one CSS sees)        | Usually 980px, 375px, or some fixed value set by the browser (not the physical screen width) | Almost never happens on desktop |
| **Desktop browsers** (Safari/Chrome/Firefox on macOS/Windows) | The **visual viewport** = the actual browser window size | –                      | Exactly the inner width/height of the browser window |

### 3. Why Mobile Behaves Differently (This is the key confusion)

By default, mobile browsers lie to your CSS.

- Physical screen of an iPhone 16 Pro: 1290 × 2796 pixels
- But if you open DevTools and run `document.documentElement.clientWidth`, you probably get **390** or **430** CSS pixels.
- Many older sites were designed for ~980px width, so mobile browsers pretend the viewport is ~980px wide (or 375px on modern iPhones with the correct meta tag). This is called the **layout viewport**.

Without this line in `<head>`, mobile Safari assumes you want the old desktop behavior:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

With this meta tag → layout viewport ≈ physical device width in CSS pixels
Without it → layout viewport = 980px (or similar) even on a tiny phone

That’s why on mobile, 100vw can look huge if you forget the meta tag.

### 4. Units You Mentioned: vw and vh

- 1vw = 1% of the **layout viewport width**
- 1vh = 1% of the **layout viewport height**

So:

| Device / Situation                        | 100vw equals…                                      |
|-------------------------------------------|----------------------------------------------------|
| Desktop Safari, Chrome, etc.              | Current browser window width (changes when you resize) |
| Mobile with proper `<meta name="viewport">` | Roughly the screen width in CSS pixels (e.g., 393px on many iPhones) |
| Mobile without the meta tag               | Usually 980px or whatever the browser defaults to  |

### 5. Summary – Answers to Your Exact Questions

- On a mobile phone, the viewport does **not** automatically mean the whole physical screen unless you have the meta viewport tag.
- On Safari macOS (or any desktop browser), yes — the viewport is exactly the browser window size, and vw/vh change instantly when you resize the window.
- The viewport is **never completely fixed** — it always changes when:
  - You resize the browser window (desktop)
  - You rotate the phone (mobile)
  - The on-screen keyboard appears/disappears (mobile)
  - You zoom (though zooming usually doesn’t change the layout viewport on mobile)

### 6. Quick Test You Can Try Right Now

Paste this into any HTML file and open it on phone vs Mac:

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { margin:0; font-family:sans-serif; }
    .box {
      width: 100vw;
      height: 100vh;
      background: #f06d06;
      color: white;
      display: grid;
      place-items: center;
      font-size: 2rem;
    }
  </style>
</head>
<body>
  <div class="box">
    100vw × 100vh<br>
    Width: <span id="w"></span>px<br>
    Height: <span id="h"></span>px
  </div>

<script>
  function update() {
    document.getElementById('w').textContent = window.innerWidth;
    document.getElementById('h').textContent = window.innerHeight;
  }
  update();
  window.addEventListener('resize', update);
</script>
</body>
</html>
```

- On macOS Safari → the orange box resizes exactly with the browser window.
- On iPhone Safari → the orange box fills almost the whole screen (minus Safari UI), and the numbers match your device’s CSS pixel width (e.g., 393px on many iPhones).

That’s the viewport in action!
