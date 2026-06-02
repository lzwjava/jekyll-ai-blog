---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 升级过时的Vue.js技术栈
translated: true
type: note
---

以下是图示：

**技术栈（约 2016–2020 年）：**
- **Vue 1.x** + Vue Router 0.7 + Vue Resource — *已过时*，当前版本为 Vue 3
- **Webpack 1** — 已停止维护，当前版本为 Webpack 5
- **Babel 6** + ES2015 预设 — 旧的转译方案
- **plupload** + **qiniu-js-sdk** 用于上传，**leancloud-realtime** 用于实时聊天
- **hls.js 0.7** 用于视频流传输

**核心架构：**
- 单页应用（SPA），Node 开发服务器（端口 9060）将 `/api/*` 代理至 `https://api.quzhiboapp.com`
- Vue 1 单文件组件（`.vue`），使用 stylus 编写样式
- 针对移动端网页开发的直播产品（quzhiboapp）

---

**如何升级 —— 两条路径：**

### 方案 A：渐进式升级（更安全）
1. 分两步升级 Vue 1 → Vue 2 → Vue 3
2. 升级 vue-router、vue-resource 至 Vue 3 对应版本（`vue-router@4`、`@vueuse/core` 或 `axios`）
3. 升级 Webpack 1 → 4 → 5（改动较大，加载器和插件生态已完全变化）
4. 将已弃用的 babel-runtime 替换为 `@babel/preset-env`

### 方案 B：现代化重写（如有时间建议采用）
1. 使用 **Vite** 新建项目（比 Webpack 更快，配置更简单）
2. 集成 **Vue 3** + Composition API
3. 将 `vue-resource` 替换为 **axios**
4. 更新 `hls.js` 至最新版本（原为 0.7，当前约为 1.x）
5. 弃用 plupload/qiniu —— 迁移至 **qiniu-js-sdk v2** 或直接使用最新 SDK
6. 保留视图/组件架构，但使用 Vue 3 单文件组件语法重写

**最大风险：** `leancloud-realtime` SDK 可能与新版 Node/打包工具不兼容。`vue-resource` 已停止维护 —— axios 可直接替代。

您希望选择哪个方向？
