---
audio: false
generated: true
lang: zh
layout: post
title: 使用并发
translated: true
type: note
---

看起来您是在询问在前端开发中使用 "concurrently" 的问题。不过，"concurrently" 通常是一个 Node.js 包，用于同时运行多个命令或脚本，常见于后端或开发工作流中，而非直接用于前端代码。您是指在前端项目设置中使用它（例如运行脚本），还是指前端 JavaScript 中的并发操作（例如 Promise、async/await）？我暂时假设是前者，但您可以进一步说明！

### 在前端项目中使用 `concurrently`

如果您正在开发前端项目（例如使用 React、Vue 或 Angular），`concurrently` 通常用于在开发过程中同时运行多个进程，比如启动开发服务器和构建监听器。以下是使用方法：

#### 1. 安装 `concurrently`

首先，将其作为开发依赖安装到项目中：

```bash
npm install --save-dev concurrently
```

#### 2. 在 `package.json` 中添加脚本

在 `package.json` 中定义要同时运行的脚本。例如，同时运行前端开发服务器和 CSS 预处理器（如 Sass）：

```json
{
  "scripts": {
    "start:frontend": "react-scripts start", // 或您的前端开发命令
    "watch:css": "sass --watch src/styles:dist/styles",
    "dev": "concurrently \"npm run start:frontend\" \"npm run watch:css\""
  }
}
```

- `start:frontend`：运行前端开发服务器（例如 React、Vite 等）。
- `watch:css`：监听并编译 CSS 文件。
- `dev`：使用 `concurrently` 同时运行上述两个命令。

#### 3. 运行并发脚本

在终端中运行：

```bash
npm run dev
```

这将同时启动前端服务器和 CSS 监听器。您可以在同一终端中看到两个进程的输出，`concurrently` 会保持它们同时运行。

#### 4. 可选配置

您可以使用以下选项自定义 `concurrently`：

- `--kill-others`：如果某个进程失败，停止所有进程。
- `--names`：为每个进程添加标签，使输出更清晰。

在 `package.json` 中使用选项的示例：

```json
"dev": "concurrently --names \"前端,CSS\" --kill-others \"npm run start:frontend\" \"npm run watch:css\""
```

输出可能如下：

```
[前端] 正在启动前端服务器...
[CSS] 正在监听 CSS 文件...
```

#### 在前端工作流中的使用场景

假设您正在构建一个带有独立 API 服务器的 React 应用：

- 前端：`npm run start`（React 开发服务器，端口 3000）。
- API：`npm run start:api`（例如 Node.js 服务器，端口 5000）。
使用 `concurrently` 可以同时运行两者：

```json
"dev": "concurrently \"npm run start\" \"npm run start:api\""
```

### 如果您指的是前端中的并发 JavaScript

如果您是在询问前端代码中的并发操作处理（例如同时调用多个 API），以下是使用 `Promise.all` 的简单示例：

```javascript
async function fetchData() {
  const [userData, postsData] = await Promise.all([
    fetch('https://api.example.com/user').then(res => res.json()),
    fetch('https://api.example.com/posts').then(res => res.json())
  ]);
  console.log(userData, postsData);
}
fetchData();
```

这会并发运行 API 调用，并等待两者完成。

### 如需进一步说明请告知

如果您所说的 "前端中的并发" 是指其他内容（例如特定的库、框架或使用场景），请告诉我，我会进一步调整回答！
