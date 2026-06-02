---
audio: false
generated: true
lang: zh
layout: post
title: 使用Chokidar实现文件监听
translated: true
type: note
---

Chokidar 是一个主要设计用于服务端文件监听的 Node.js 库，因此直接在前端（即浏览器环境）使用并非其典型应用场景。浏览器不像 Node.js 那样直接访问文件系统，这就是为什么 Chokidar 更适用于后端或构建时环境。不过，如果您在开发环境中使用 Webpack、Vite 或 Parcel 等打包工具，或是开发 Electron 应用（结合了 Node.js 与前端），则可以间接利用 Chokidar。以下根据具体场景说明实现方式。

### 为什么 Chokidar 不能直接在浏览器运行
- Chokidar 依赖 Node.js 的 `fs`（文件系统）等 API 来监听文件，这些 API 在浏览器环境中不可用
- 前端代码运行在沙箱化的浏览器环境中，出于安全考虑，文件系统访问受到限制

### 在"前端"上下文中使用 Chokidar 的可能场景
以下是与前端开发相关的 Chokidar 使用方式：

#### 1. **配合构建工具进行开发**
若想在前端开发过程中使用 Chokidar 监听文件（例如实现热重载或实时更新），需要将其集成到构建流程而非浏览器运行时。

自定义 Node.js 脚本示例：
```javascript
const chokidar = require('chokidar');

// 监听前端源文件变化
chokidar.watch('./src/**/*.{html,js,css}').on('all', (event, path) => {
  console.log(event, path);
  // 在此触发重建或通知前端开发服务器
});
```
- **应用场景**：可结合 WebSocket 连接向浏览器推送开发时的更新
- **工具搭配**：与 `esbuild` 或开发服务器（如 Vite 已内置文件监听，但可通过 Chokidar 定制）配合使用

#### 2. **在 Electron 应用中**
如果"前端"是 Electron 应用的一部分，可在主进程（Node.js）中使用 Chokidar，并将变更通知渲染进程（前端）。

示例：
```javascript
// main.js (Electron 主进程)
const { ipcMain } = require('electron');
const chokidar = require('chokidar');

chokidar.watch('./files').on('change', (path) => {
  ipcMain.send('file-changed', path); // 向渲染进程发送事件
});
```
```javascript
// renderer.js (前端)
const { ipcRenderer } = require('electron');

ipcRenderer.on('file-changed', (event, path) => {
  console.log(`文件已变更: ${path}`);
  // 相应更新用户界面
});
```

#### 3. **通过后端代理服务的前端应用**
若要为网页应用实现文件监听功能，需在 Node.js 后端运行 Chokidar，并通过 WebSocket 或服务器推送事件向前端发送更新。

Express 与 WebSocket 后端示例：
```javascript
const express = require('express');
const WebSocket = require('ws');
const chokidar = require('chokidar');

const app = express();
const server = app.listen(3000);
const wss = new WebSocket.Server({ server });

chokidar.watch('./public').on('change', (path) => {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(`文件已变更: ${path}`);
    }
  });
});
```
前端 React 示例：
```javascript
const socket = new WebSocket('ws://localhost:3000');
socket.onmessage = (event) => {
  console.log(event.data); // "文件已变更: ..."
  // 更新状态或用户界面
};
```

### 安装方法
在任意上述方案中使用 Chokidar 前，需先安装到 Node.js 项目：
```bash
npm install chokidar
```

### 核心 Chokidar 方法
- `chokidar.watch(path, [options])`: 开始监听文件或目录
- 事件监听：`.on('add', callback)`, `.on('change', callback)`, `.on('unlink', callback)`, `.on('all', (event, path) => {})`
- 配置选项：`{ ignored: /node_modules/, persistent: true }`（按需定制）

### 其他可能性
如果完全不需要 Node.js 环境，仅需在浏览器中实现类文件监听功能（例如监听 `<input type="file">` 变更），这需要用到 `File` API 和事件监听器而非 Chokidar。

请告知您的具体配置或目标，我可以提供更针对性的建议！
