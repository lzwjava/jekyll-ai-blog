---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Vue 3 迁移：核心流程损坏
translated: true
type: note
---

工作树是干净的（探针已移除，开发服务器已停止）。以下是完整评估。

## 当前进度

**已完成（已提交，`6fc4b76`）：**

- **Vite + Vue 3 迁移脚手架已完成**：`src/main.js`（`createApp`）、`src/router/index.js`（vue-router 4，hash 历史，全部 21 条路由 + catch-all 重定向）、根 `index.html`、`public/` 资源、`vite.config.js`（别名 `@`、stylus 导入、开发代理）、`.env.production`。
- **所有约 50 个 SFC 已转换为 `<script setup>`**：零 Vue 2 遗留（`new Vue`、`filters:`、`.sync`、`slot-scope`、`this.$set`、`beforeDestroy`——无命中）。
- **构建和开发模式均可用**：`npm run build` 成功（1.7 秒，输出 → `static/`），`npm run dev` 在 :5173 上提供服务。
- **`api.js` 已用 axios 重写**（X-Session 头、统一 reject）、路由懒加载、部署链（fabfile rsync + nginx `website.conf`）已更新。
- **跨 22 条路由的浏览器冒烟测试**：全部渲染，无页面错误。

## 剩余工作（已通过代码检查 + 无头浏览器探针验证）

**P0 – 核心流程损坏**

1. **动态 `<component :is="'string'">` 永远不会解析。** 已在浏览器中证实：覆盖层渲染了 `<login-options-form>…</login-options-form>`（未知元素），而不是该组件。影响 `src/App.vue:30`（登录/注册）、`src/views/IntroView.vue:48`（报名选项/分享/订阅/QR-pay）、`src/views/LiveView.vue:54`（打赏/控制）。修复方法：在 refs 中保留导入的组件对象，而不是字符串名称。
2. **报名/加入流程缺失**：任何地方都没有 `attendances/create` 调用；旧的 `pay()`/`createAttend()`/`wxPay`/`payFinish` 都被丢弃了（`wechat.wxPay` 未使用，`QrcodePayForm` 的 `payFinish` 和 `SubscribeForm` 的 `close` 没有被监听）。
3. **App.vue 事件管道失效**：`provide(...)` 没有 `inject` 消费者；`defineExpose({$dispatch})` 只能通过根代理访问；`@hide="hideForm"` 忽略了类型参数，因此 `handleHideLoginOptionsForm`（登录↔注册切换）无法触达；`Tip` 已导入但从未渲染。

**P1 – LiveView（核心页面）回归**（1011 → 328 行）

4. **聊天不可用**：没有 LeanCloud 实时客户端（`leancloud-realtime` 依赖未使用），`msgs` 从未填充，`sendMsg` 只清空输入框，`membersCount` 从未设置。
5. **播放**：只有 `videoEl.src = webHlsUrl`（原生 HLS = 仅 Safari/iOS/微信）；`hls.js` 未使用 → Android Chrome 无法播放；切换线路是 `location.reload()`，而不是切换 `hlsUrls`。
6. **打赏损坏**：`RewardForm` 发出 `reward`，LiveView 只监听 `@close`；没有 `rewards` API 调用。
7. **`null` 组件崩溃**：`ControlForm.vue` 调用 `show(null, …)` → 在开始/结束直播时出现 `null.$dispatch` TypeError；`configWeixin(null)`/`shareLive(null,…)` 同理 → `wechat.js` 回调中的 `show(comp,…)`/`comp.$emit`。

**P2 – 上传 / 编辑**

8. **`src/common/qiniu.js` 是一个 15 行的占位桩** → markdown 图片上传（按钮根本没有处理程序）、EditLiveView 封面 + 课件上传、EditUserView 头像（`// Implement avatar change`）都是死的；`files/uptoken` 从未被调用。`plupload` 子模块为空，`qiniu-js` 依赖未使用。
9. **`markdown-area.vue` 的 `v-model` 不匹配**：属性是 `content` + `update:content`，但父组件传入 `v-model` → 详情/公告编辑永远不会绑定（写入空内容）。`date_picker` 是正确的（`modelValue`）。
10. **EditLiveView 丢失的功能**：封面、付费/门票、shareIcon、分类、主播介绍、公告链接、课件、提交审核——只剩下 subject/planTs/detail。
11. **需要与后端验证的端点漂移**：`lives/my`（旧的 `lives/attended` + `lives/me`）、`self/bindPhone`（旧的 `users/bindPhone`）、`lives/user/:id`（旧的 `lives/userLives` + `lives/attended`）。

**P3 – 渲染与整理**

12. **Markdown**：marked v12 忽略了已移除的 `sanitize`/`highlight` 选项（hljs 永远不会运行），并且 `github-markdown-css` + `highlight.js/styles/solarized-light.css` 的引入被删除 → 表格/代码没有样式；`sanitize` 丢失也是一个 XSS 回归。
13. **无效配置**：`.env.production` 从未被应用——`vite.config.js` 读取 `process.env.VITE_BASE_URL`（未定义；构建后的 HTML 确认 base `/`），没有任何地方读取 `VITE_API_BASE_URL`。使用 `loadEnv` 或删除。
14. **需要删除的遗留文件**：`webpack.config.js`、`server.js`（webpack-dev-server）、`yarn.lock`、`plupload` 子模块 + `.gitmodules`、未使用的依赖（`weui`、`rupture`、`dayjs`、`font-awesome`——尽管 ProfileView 使用了 `fa fa-pencil-square-o`，但没有链接 FA CSS，所以图标不可见）、未使用的组件（`nav.vue`、`loading.vue`、`logo.vue`、`dropdown.vue`、`InputTextForm`、`RecommendLiveList`、`tip.vue`）。
15. **安全**：`uploadqn.json` 中有 **硬编码的七牛 access/secret 密钥并已提交到仓库**——请轮换它们并加入 gitignore。
16. **小缺陷**：`util.js` 中的 `import crypto from 'crypto'` → 构建警告 “externalized for browser compatibility”（未使用）；CSS 拼写错误 `heigth 15px`（`ProfileView.vue:109`）；13 个静默的 `catch(() => {})`；899 KB/976 KB 的块（没有代码分割）。

**建议的后续步骤：** 修复 #1（一行类更改，解锁所有覆盖层）→ #3 → #2 → #9 → #4/#5，然后进行 P2/P3 清理。
