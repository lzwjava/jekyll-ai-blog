---
audio: false
generated: true
lang: zh
layout: post
title: 使用ShellJS执行Shell命令
translated: true
type: note
---

ShellJS 是一个 JavaScript 库，为 Node.js 项目提供 Unix shell 命令（如 `cp`、`mkdir`、`exec` 等）。它允许直接在 JavaScript 中执行熟悉的 shell 命令，从而简化了跨平台脚本的编写。然而，在前端开发（通常指在浏览器中运行的代码）中，ShellJS 并不直接适用，因为它依赖的 Node.js API 在浏览器环境中不可用。下面我将解释其原因，以及如何在前端开发工作流中有效使用 ShellJS。

### 为什么 ShellJS 无法直接在浏览器中运行
- **Node.js 依赖**：ShellJS 构建于 Node.js 运行时之上，该运行时提供了文件系统访问、进程执行和其他系统级操作的 API。由于浏览器的沙盒安全模型，这些 API 在浏览器中不可用。
- **浏览器安全限制**：浏览器阻止 JavaScript 访问本地文件系统或执行任意命令，以保护用户免受恶意脚本的侵害。由于 ShellJS 的命令（如 `exec`（用于运行外部进程）或 `cp`（用于复制文件））依赖这些功能，它们无法在浏览器环境中运行。

因此，您无法在浏览器中运行的客户端 JavaScript 中直接使用 ShellJS。不过，通过将 ShellJS 集成到构建过程或开发工具中（这些工具通常在 Node.js 上运行），ShellJS 仍可以在前端开发中发挥重要作用。

### 如何在前端开发工作流中使用 ShellJS
虽然 ShellJS 不在浏览器中执行，但您可以在基于 Node.js 的脚本中利用它来自动化支持前端开发的任务。前端项目通常依赖 Webpack、Gulp 或 Grunt 等构建工具，这些工具在 Node.js 上运行，并可以集成 ShellJS 以简化工作流。具体方法如下：

#### 1. 安装 ShellJS
首先，确保系统已安装 Node.js。然后，使用 npm 或 yarn 将 ShellJS 添加到项目中：

```bash
npm install shelljs
```

或

```bash
yarn add shelljs
```

#### 2. 创建使用 ShellJS 的 Node.js 脚本
编写一个使用 ShellJS 执行与前端项目相关任务的脚本，例如复制文件、创建目录或运行命令行工具。将此脚本保存为 `.js` 文件（例如 `build.js`）。

以下是一个准备前端资源的示例脚本：

```javascript
const shell = require('shelljs');

// 如果构建目录不存在，则创建它
shell.mkdir('-p', 'build');

// 将 HTML 文件复制到构建目录
shell.cp('-R', 'src/*.html', 'build/');

// 编译 Sass 为 CSS
shell.exec('sass src/styles.scss build/styles.css');

// 复制 JavaScript 文件
shell.cp('-R', 'src/*.js', 'build/');
```

- **`shell.mkdir('-p', 'build')`**：创建一个 `build` 目录，`-p` 确保目录已存在时不会报错。
- **`shell.cp('-R', 'src/*.html', 'build/')`**：将所有 HTML 文件从 `src` 复制到 `build`，`-R` 表示递归复制。
- **`shell.exec('sass src/styles.scss build/styles.css')`**：运行 Sass 编译器生成 CSS。

#### 3. 将脚本集成到工作流中
您可以通过以下几种方式运行此脚本：
- **直接通过 Node.js**：
  ```bash
  node build.js
  ```
- **作为 npm 脚本**：将其添加到 `package.json`：
  ```json
  "scripts": {
    "build": "node build.js"
  }
  ```
  然后运行：
  ```bash
  npm run build
  ```
- **与构建工具结合**：将 ShellJS 集成到 Gulp 等工具中。例如：
  ```javascript
  const gulp = require('gulp');
  const shell = require('shelljs');

  gulp.task('build', function(done) {
    shell.exec('sass src/styles.scss build/styles.css');
    shell.cp('-R', 'src/*.js', 'build/');
    done();
  });
  ```

#### 4. 前端开发中的使用场景
ShellJS 可以在您的前端工作流中自动化各种任务：
- **资源管理**：将图片、字体或其他静态文件复制到构建目录。
- **CSS/JavaScript 处理**：通过 `shell.exec` 运行 Sass、PostCSS 或 UglifyJS 等工具。
- **测试和代码检查**：执行测试运行器或代码检查工具（例如 `shell.exec('eslint src/*.js')`）。
- **部署准备**：打包文件或清理目录（例如 `shell.rm('-rf', 'build/*')`）。

### 示例：自动化前端构建过程
假设您正在使用 HTML、Sass 和 JavaScript 构建一个简单的 Web 应用。以下是使用 ShellJS 自动化构建的方法：

**目录结构**：
```
project/
├── src/
│   ├── index.html
│   ├── styles.scss
│   └── app.js
├── build.js
└── package.json
```

**build.js**：
```javascript
const shell = require('shelljs');

// 清理构建目录
shell.rm('-rf', 'build/*');

// 创建构建目录
shell.mkdir('-p', 'build');

// 复制 HTML
shell.cp('src/index.html', 'build/');

// 编译 Sass
shell.exec('sass src/styles.scss build/styles.css');

// 复制 JavaScript
shell.cp('src/app.js', 'build/');
```

**package.json**：
```json
{
  "scripts": {
    "build": "node build.js"
  },
  "dependencies": {
    "shelljs": "^0.8.5"
  }
}
```

运行 `npm run build`，ShellJS 将准备您的 `build` 目录，其中包含编译和复制的文件，随时可以部署。

### 关键要点
- **不适用于浏览器**：由于 ShellJS 依赖 Node.js 和系统级操作，它无法在浏览器中运行。
- **适用于构建脚本**：在基于 Node.js 的脚本中使用它，可以自动化文件操作和命令执行等前端任务。
- **跨平台**：ShellJS 确保您的脚本在 Windows、Linux 和 macOS 上一致运行，非常适合多样化的开发环境。

通过将 ShellJS 集成到由 Node.js 驱动的构建过程中，您可以通过强大的自动化功能增强前端开发工作流，尽管它并不直接在浏览器中运行。
