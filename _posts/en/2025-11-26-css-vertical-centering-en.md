---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: CSS Vertical Centering Is Easy Now
translated: false
type: note
---

It's not *actually* hard anymore (since ~2015), but it **feels** hard because CSS went through a long, painful history of half-broken solutions before giving us good ones. That's why everyone has PTSD about vertical centering.

Here’s why it used to be a nightmare and why most old tutorials still traumatize people:

### The Dark Ages (before Flexbox/Grid)

1. **Block elements don’t have natural height centering**
   `margin: auto` only works horizontally. Vertically? Nothing. The box model simply had no built-in way.

2. **The terrible hacks people actually used in production:**

   ```css
   /* 1. Table-cell (works but semantically awful) */
   .parent { display: table; }
   .child { display: table-cell; vertical-align: middle; }

   /* 2. Absolute + negative margin (requires known height) */
   .child {
     position: absolute;
     top: 50%;
     margin-top: -50px; /* half of fixed height */
   }

   /* 3. Absolute + transform (most popular hack 2010-2015) */
   .child {
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
   }

   /* 4. Ghost element (yes, people did this) */
   .parent:before {
     content: '';
     height: 100%;
     display: inline-block;
     vertical-align: middle;
   }
   ```

All of these are fragile, require extra markup, break with dynamic content, or feel like black magic.

### The Modern Era (2015+) – It’s literally one or two lines now

**Flexbox (the go-to solution since 2016):**

```css
.parent {
  display: flex;
  justify-content: center;    /* horizontal */
  align-items: center;        /* vertical */
  min-height: 100vh;          /* or whatever height you need */
}
```

Done. Works with unknown heights, responsive, no hacks.

**Grid (also trivial):**

```css
.parent {
  display: grid;
  place-items: center;        /* shorthand for align-items + justify-items */
  min-height: 100vh;
}
```

**Even the new hotness (2023+):**

```css
.parent {
  display: grid;
  grid-template-rows: 1fr auto 1fr;  /* or just center with margin */
}
.child { margin: auto; }
```

### So why does it still *feel* hard in 2025?

1. **Old tutorials never die** – Google still shows 10-year-old “15 ways to vertically center” articles full of hacks.
2. **You learned the hacks first** – Muscle memory and trauma stick.
3. **Edge cases still exist** – centering text in a button with `line-height` vs `padding`, or inside `inline-block`, etc.
4. **Tailwind/Bootstrap sometimes fight you** – they override `display` or heights in weird ways.

### TL;DR – The correct answer in 2025

Just use Flexbox or Grid. 99% of the time:

```css
.center-everything {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

or

```css
.center-everything {
  display: grid;
  place-items: center;
}
```

If you're still fighting vertical centering today, you're either:

- Working on an ancient codebase that can’t use flexbox (IE11-era)
- Overcomplicating it
- Reading the wrong tutorial

Vertical centering stopped being hard years ago — we just all carry the scars. Let them go. Use flexbox and be free. 😭
