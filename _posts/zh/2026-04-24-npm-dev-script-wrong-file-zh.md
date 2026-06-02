---
audio: false
generated: true
image: false
lang: zh
layout: post
title: npm开发脚本指向错误文件
translated: true
type: note
---

## 环境信息

| 工具 | 版本 |
|------|---------|
| Node.js | v25.3.0 |
| npm | 11.7.0 |
| npx | 11.7.0 |
| Node 路径 | `/opt/homebrew/bin/node` |
| 操作系统 | macOS Darwin 25.4.0 |

---

## 待提交的问题

**标题：** `npm run dev` 脚本指向了错误的入口文件 —— 服务器从未启动

**描述：**

`package.json` 中的 `dev` 脚本运行的是 `src/index.ts`，这是一个库导出文件，而非服务器文件。这导致 nodemon 启动后立即退出，没有服务器在运行。

**复现步骤：**
1. `npm install`
2. `npm run dev`
3. 服务器立即退出 —— 端口 3000 上没有任何监听

**预期：** 服务器在 `http://localhost:3000` 启动

**实际：** 进程干净利落地退出，服务器未启动

**修复方案：**
```json
// package.json
"dev": "nodemon --exec ts-node src/server.ts"
```

**临时解决方案：**
```bash
npx ts-node src/server.ts
```

**环境：** Node v25.3.0, npm 11.7.0, macOS Darwin 25.4.0

---

你可以在此提交此问题：https://github.com/sreekanthvaripalli/secure-captcha-plugin/issues
