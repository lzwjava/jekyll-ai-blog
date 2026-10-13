---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Vue 3 Migration: Core Flows Broken"
translated: false
type: note
---

Working tree is clean (probe removed, dev server stopped). Here's the full assessment.

## Current progress

**Completed (committed, `6fc4b76`):**

- **Vite + Vue 3 migration scaffold done**: `src/main.js` (`createApp`), `src/router/index.js` (vue-router 4, hash history, all 21 routes + catch-all redirect), root `index.html`, `public/` assets, `vite.config.js` (alias `@`, stylus imports, dev proxy), `.env.production`.
- **All ~50 SFCs converted to `<script setup>`**: zero Vue 2 remnants (`new Vue`, `filters:`, `.sync`, `slot-scope`, `this.$set`, `beforeDestroy` — no hits).
- **Build & dev both work**: `npm run build` succeeds (1.7s, output → `static/`), `npm run dev` serves on :5173.
- **`api.js` rewritten with axios** (X-Session header, unified reject), router lazy-loading, deploy chain (fabfile rsync + nginx `website.conf`) updated.
- **Browser smoke test across 22 routes**: all render, no page errors.

## Remaining work (verified by code inspection + headless-browser probe)

**P0 – core flows broken**

1. **Dynamic `<component :is="'string'">` never resolves.** Proven in browser: overlay rendered `<login-options-form>…</login-options-form>` (unknown element) instead of the component. Affects `src/App.vue:30` (login/register), `src/views/IntroView.vue:48` (报名 options/share/subscribe/QR-pay), `src/views/LiveView.vue:54` (reward/control). Fix: keep imported component objects in the refs, not string names.
2. **报名/join flow missing**: no `attendances/create` call anywhere; old `pay()`/`createAttend()`/`wxPay`/`payFinish` all dropped (`wechat.wxPay` unused, `QrcodePayForm`'s `payFinish` and `SubscribeForm`'s `close` aren't listened to).
3. **App.vue event plumbing dead**: `provide(...)` has no `inject` consumers; `defineExpose({$dispatch})` is only reachable via root proxy; `@hide="hideForm"` ignores the type arg so `handleHideLoginOptionsForm` (login↔register switch) is unreachable; `Tip` imported but never rendered.

**P1 – LiveView (core page) regressions** (1011 → 328 lines)

4. **Chat non-functional**: no LeanCloud realtime client (`leancloud-realtime` dep unused), `msgs` never populated, `sendMsg` only clears input, `membersCount` never set.
5. **Playback**: only `videoEl.src = webHlsUrl` (native HLS = Safari/iOS/WeChat only); `hls.js` unused → Android Chrome can't play; 切换线路 is a `location.reload()` instead of switching `hlsUrls`.
6. **Reward broken**: `RewardForm` emits `reward`, LiveView listens only `@close`; no `rewards` API call.
7. **`null` component crashes**: `ControlForm.vue` calls `show(null, …)` → `null.$dispatch` TypeError on 开始/结束直播; same for `configWeixin(null)`/`shareLive(null,…)` → `show(comp,…)`/`comp.$emit` in `wechat.js` callbacks.

**P2 – uploads / editing**

8. **`src/common/qiniu.js` is a 15-line placeholder stub** → markdown image upload (button has no handler at all), EditLiveView cover + courseware upload, EditUserView avatar (`// Implement avatar change`) are all dead; `files/uptoken` never called. `plupload` submodule empty, `qiniu-js` dep unused.
9. **`markdown-area.vue` `v-model` mismatch**: prop `content` + `update:content` but parents pass `v-model` → detail/notice editing never binds (writes empty content). `date_picker` is correct (`modelValue`).
10. **EditLiveView lost features**: cover, 付费/门票, shareIcon, 分类, 主播介绍, 公告 links, 课件, 提交审核 — only subject/planTs/detail remain.
11. **Endpoint drift to verify vs backend**: `lives/my` (old `lives/attended` + `lives/me`), `self/bindPhone` (old `users/bindPhone`), `lives/user/:id` (old `lives/userLives` + `lives/attended`).

**P3 – rendering & housekeeping**

12. **Markdown**: marked v12 ignores removed `sanitize`/`highlight` options (hljs never runs), and `github-markdown-css` + `highlight.js/styles/solarized-light.css` imports were dropped → tables/code unstyled; `sanitize` loss is also an XSS regression.
13. **Dead config**: `.env.production` never applied — `vite.config.js` reads `process.env.VITE_BASE_URL` (undefined; built HTML confirms base `/`), nothing reads `VITE_API_BASE_URL`. Use `loadEnv` or delete.
14. **Legacy files to delete**: `webpack.config.js`, `server.js` (webpack-dev-server), `yarn.lock`, `plupload` submodule + `.gitmodules`, unused deps (`weui`, `rupture`, `dayjs`, `font-awesome` — though ProfileView uses `fa fa-pencil-square-o` with no FA CSS linked, so the icon is invisible), unused components (`nav.vue`, `loading.vue`, `logo.vue`, `dropdown.vue`, `InputTextForm`, `RecommendLiveList`, `tip.vue`).
15. **Security**: `uploadqn.json` has **hardcoded Qiniu access/secret keys committed to the repo** — rotate them and gitignore.
16. **Small defects**: `import crypto from 'crypto'` in `util.js` → build warning "externalized for browser compatibility" (unused); CSS typo `heigth 15px` (`ProfileView.vue:109`); 13 silent `catch(() => {})`; 899 KB/976 KB chunks (no code splitting).

**Suggested next steps:** fix #1 (one-line-class change, unblocks all overlays) → #3 → #2 → #9 → #4/#5, then P2/P3 cleanup.
