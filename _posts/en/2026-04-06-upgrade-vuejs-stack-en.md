---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrading an Outdated Vue.js Stack
translated: false
type: note
---

Here's the picture:

**Stack (circa 2016–2020):**
- **Vue 1.x** + Vue Router 0.7 + Vue Resource — *ancient*, Vue 3 is current
- **Webpack 1** — EOL, current is Webpack 5
- **Babel 6** + ES2015 preset — old transpilation
- **plupload** + **qiniu-js-sdk** for uploads, **leancloud-realtime** for real-time chat
- **hls.js 0.7** for video streaming

**Key architecture:**
- SPA with a Node dev server (port 9060) proxying `/api/*` to `https://api.quzhiboapp.com`
- Vue 1 SFC (`.vue` single-file components), stylus for styles
- Targets mobile web for a live streaming product (quzhiboapp)

---

**How to upgrade — two paths:**

### Option A: Incremental (safer)
1. Upgrade Vue 1 → Vue 2 → Vue 3 (two-step)
2. Upgrade vue-router, vue-resource → Vue 3 equivalents (`vue-router@4`, `@vueuse/core` or `axios`)
3. Upgrade Webpack 1 → 4 → 5 (major pain, loader/plugin ecosystem changed completely)
4. Replace deprecated babel-runtime with `@babel/preset-env`

### Option B: Modern rewrite (recommended if you have time)
1. Bootstrap a new project with **Vite** (much faster than Webpack, easy config)
2. Drop in **Vue 3** + Composition API
3. Replace `vue-resource` with **axios**
4. Update `hls.js` to latest (was 0.7, now ~1.x)
5. Drop plupload/qiniu — migrate to **qiniu-js-sdk v2** or just use the current SDK
6. Keep the views/components architecture but rewrite them in Vue 3 SFC syntax

**Biggest risk:** `leancloud-realtime` SDK may be incompatible with newer Node/bundlers. `vue-resource` is abandonware — axios is the drop-in replacement.

Which direction do you want to go?