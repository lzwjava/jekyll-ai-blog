---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开发脚本指向错误文件
translated: true
type: note
---

## 事件经过

### `npm run dev` 失败原因

`package.json` 中的 dev 脚本原配置为：
```json
"dev": "nodemon --exec ts-node src/index.ts"
```

`src/index.ts` 是一个**库的入口文件**——它仅导出类与类型，不包含服务器启动代码。直接运行该文件不会执行任何操作；nodemon 启动后会立即正常退出，没有服务器进入监听状态。

### 解决方案

实际的服务器代码位于 `src/server.ts` 中，该文件包含 `CaptchaServer` 类及其内部的 Express 应用，并通过 `.start()` 方法调用 `app.listen()` 启动服务。文件底部还包含一个启动保护逻辑：

```ts
if (require.main === module) {
  const server = new CaptchaServer(port, workers);
  server.start();
}
```

通过以下命令直接运行该文件：
```bash
npx ts-node src/server.ts
```

...即可在 3000 端口成功启动 Express 服务器，健康检查接口也能正常响应。

### 根本原因

`package.json` 中的 `dev` 脚本指向了错误的文件（应为 `server.ts` 而非 `index.ts`）。正确的配置应为：
```json
"dev": "nodemon --exec ts-node src/server.ts"
```