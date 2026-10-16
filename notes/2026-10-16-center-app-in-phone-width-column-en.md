---
audio: false
generated: true
image: false
lang: en
layout: post
title: Center App in Phone-Width Column
translated: false
type: note
---

Yes — I capped the whole app to a centered, phone-width column on desktop. Everything compiled cleanly with `npm run build`.

## What was the problem

The page stretched `width: 100%` across the whole monitor. Also, two bars use `position: fixed` (`.tab-bar`, `.attend-section`), which resolves `100%` against the **viewport**, so even a wrapper max-width wouldn't have contained them.

## Changes

**`src/stylus/variables.styl`** — single source of truth for the column width:

```stylus
$app-max-width = 480px
```

**`src/App.vue`** — constrain and center the `#wrapper` column:

```stylus
#wrapper
  position relative
  width 100%
  max-width $app-max-width
  margin 0 auto
  min-height 100%
  background-color #e7e7e7

// Desktop: make the centered column read like a phone screen.
@media screen and (min-width: 481px)
  #wrapper
    box-shadow 0 0 24px rgba(0, 0, 0, .35)
    min-height 100vh
```

Since `.view` is `position: absolute; width: 100%` inside `#wrapper`, every route (`/lives`, profile, room…) is automatically limited too.

**`src/components/Tabbar.vue`** — the fixed bottom tab bar (was `max-width: 700px` but left-aligned to the viewport) now centers on the column:

```stylus
.tab-bar
  position fixed
  left 50%
  transform translateX(-50%)
  width 100%
  ...
  max-width $app-max-width
```

**`src/views/IntroView.vue`** — `.attend-section` had a broken media query (`margin: 0 auto` doesn't center fixed elements); replaced with the same `left: 50%` + `translateX(-50%)` + `max-width $app-max-width` pattern.

## Result

- Mobile (≤480px viewport): unchanged, full width.
- Desktop: a 480px-wide centered column with a subtle shadow, tab bar and attend bar aligned exactly with it — looks like a phone screen on the gray background.
- Overlays/toasts stay viewport-centered (modal dimming covers the full screen), which is the usual desktop behavior.

Note: `$app-max-width` lives in `variables.styl`, so if you want a different size (e.g. `414px` for iPhone-ish, or `600px` roomier), change that one line and rebuild.
