---
audio: false
generated: true
image: false
lang: en
layout: post
title: DOM Size Limits for Large Lists
translated: false
type: note
---

Question: What is the maximum number of such li items that can render in a browser? I now have 7000+ items, is it ok? How about 20k?

Answer:

There is **no hard technical limit** in modern browsers (Chrome, Firefox, Edge, Safari) on the number of `<li>` elements you can put inside a `<ul>` or similar container like a Bootstrap `.list-group`. Browsers can technically handle tens of thousands of DOM elements.

However, **performance is the real constraint**, not a strict maximum. Here is a clear breakdown based on current web performance guidelines (as of 2026):

### Performance Guidelines for DOM Size
- **Under 1,500 total DOM nodes** on the page → Ideal (recommended by Lighthouse/Chrome).
- **1,500 – 5,000 nodes** → Acceptable in many cases, but you may start noticing slower interactions.
- **Over 10,000 nodes** → High risk of issues (slow initial render, janky scrolling, higher memory usage, delayed user interactions like clicks or hover).

Your single `<li class="list-group-item">` element contains:
- The `<li>` itself
- An `<a>` tag
- Several `<span>` elements (date, type, title)

This means **one list item ≈ 5–6 DOM nodes** (plus any Bootstrap-added classes or pseudo-elements).

- **7,000 items** → Roughly **35,000 – 42,000 DOM nodes** just from the list (plus the rest of your page).
  This is **likely to feel sluggish** on many devices, especially during scrolling, searching, or when the browser recalculates layout/styles. Initial page load and JavaScript operations will also slow down.

- **20,000 items** → Roughly **100,000+ DOM nodes**.
  This is **generally not recommended** for good user experience. You will probably see:
  - Slow page loading
  - Janky or laggy scrolling
  - Higher CPU/memory usage
  - Poor scores on tools like Lighthouse (excessive DOM size warning/error)
  - Potential unresponsiveness on lower-end devices or mobile browsers

### Why Large Lists Cause Problems
The browser must:
- Build a large DOM tree
- Calculate styles and layout for every element (even off-screen ones)
- Handle repaints and reflows when anything changes
- Keep all elements in memory

Even if the list renders, **scrolling through 7k+ or 20k items** becomes unpleasant without optimization.

### Recommended Solutions
For lists this large, do **not** render every item at once. Use one of these approaches:

1. **Virtual Scrolling / Windowing** (Best for 7k–20k+ items)
   Only render the items currently visible in the viewport (usually 10–30 items at a time). As the user scrolls, new items are added and old ones removed from the DOM.
   Popular libraries:
   - React: `react-window` or `react-virtualized`
   - Vue: `vue-virtual-scroller`
   - Angular: Angular CDK Virtual Scrolling
   - Vanilla JS: `Clusterize.js` or custom Intersection Observer implementation

2. **Pagination**
   Show 50–200 items per page with "Load more" or page numbers.

3. **Infinite Scroll** (with virtualization)
   Load more items as the user scrolls, but still only keep a limited number in the DOM.

4. **Filtering/Search on the server or client**
   Let users search or filter first so fewer items are shown.

5. **Simple optimizations if you must keep all items**
   - Use `will-change: transform;` or CSS containment
   - Avoid heavy CSS (complex selectors, shadows, etc.) on list items
   - Use `document.createDocumentFragment()` when building the list in JavaScript
   - Consider a `<table>` with fixed layout or a canvas-based list for extreme cases

### Quick Test Recommendation
Try rendering your 7,000 items in an incognito window and check:
- Chrome DevTools → Performance tab (record a scroll)
- Lighthouse audit for "Avoid excessive DOM size"
- Scroll smoothness on a mid-range laptop and a phone

If you notice lag with 7,000 items, you should implement virtualization before going to 20,000.

In summary:
- 7,000 items is **borderline** — it may work but is not optimal.
- 20,000 items is **too much** for a simple rendered list and will likely degrade user experience.

Switching to virtual scrolling will let you comfortably handle 20k, 50k, or even 100k+ items with smooth performance.

References:
- https://developer.chrome.com/docs/lighthouse/performance/dom-size
- https://web.dev/articles/dom-size-and-interactivity
- https://www.debugbear.com/blog/excessive-dom-size
