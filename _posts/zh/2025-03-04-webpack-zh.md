---
audio: false
generated: true
lang: zh
layout: post
title: 使用Webpack作为模块打包工具
translated: true
type: note
---

### 核心要点

- 要使用 webpack 1.13.2 和 webpack-dev-server 1.14.0，可能需要搭建具有特定配置的 Node.js 项目。
- 研究表明需要通过 npm 安装这些版本，创建配置文件并运行开发服务器以实现实时更新。
- 关键证据表明需要确保存在 index.html 文件，且配置中包含正确的打包文件路径。

### 安装与设置

首先确保已从 [nodejs.org](https://nodejs.org) 安装 Node.js。创建项目目录，通过 npm 初始化并安装指定版本：

- 运行 `npm init -y` 创建 package.json 文件
- 执行 `npm install webpack@1.13.2` 和 `npm install webpack-dev-server@1.14.0` 进行安装

### 配置

创建 `webpack.config.js` 文件定义打包方式。基础配置包括：

- 入口文件（如 `./src/index.js`）
- 输出路径（如生成到 dist 目录的 `bundle.js`）
- 开发服务器设置，例如静态文件的 `contentBase` 配置

### 启动开发服务器

通过 `npx webpack-dev-server` 或 `./node_modules/.bin/webpack-dev-server`（若 npx 不可用）启动服务器。访问 [http://localhost:8080](http://localhost:8080) 查看应用，修改文件时将自动更新。

### 特别注意事项

这些旧版本需要特定配置（如使用 `contentBase` 而非现代的 `static`），且文件服务可能需要手动调整，这与具备更高自动化程度的新版本有所不同。

---

### 技术指南：使用 Webpack 1.13.2 和 Webpack-Dev-Server 1.14.0 详细说明

本指南详细讲解如何搭建并使用 webpack 1.13.2 及 webpack-dev-server 1.14.0，重点介绍适用于 JavaScript 项目的开发环境配置。鉴于这些版本年代久远，其配置和行为与现代标准存在差异，本文旨在通过清晰完整的步骤说明，帮助初学者顺利完成配置。

#### 背景说明

Webpack 是 JavaScript 模块打包工具，历史上用于编译和打包 Web 应用文件，管理依赖关系并优化生产部署。Webpack-dev-server 作为配套工具，提供具备实时重载功能的开发服务器，非常适合迭代式开发。指定版本 webpack 1.13.2 和 webpack-dev-server 1.14.0 发布于 2016 年，属于老旧但功能完整的配置方案，可能用于遗留项目维护。

#### 分步安装指南

首先确保安装 Node.js（这是使用 npm 包管理器的前提），可从 [nodejs.org](https://nodejs.org) 下载。当前时间（2025年3月3日星期一太平洋标准时间上午09:45）与配置无关，仅作背景记录。

1. **创建项目目录**：打开终端创建新目录，例如 "myproject"：
   - 命令：`mkdir myproject && cd myproject`

2. **初始化 npm 项目**：运行 `npm init -y` 创建包含默认设置的 `package.json` 文件，为管理 npm 依赖项做好准备

3. **安装指定版本**：使用 npm 安装所需版本：
   - 命令：`npm install webpack@1.13.2`
   - 命令：`npm install webpack-dev-server@1.14.0`
   - 这些命令将指定版本添加到 `node_modules` 并更新 `package.json` 中的 `dependencies`

#### 目录结构与文件创建

开发服务器需要基础目录结构：

- 创建静态文件目录 `public`：`mkdir public`
- 创建应用代码目录 `src`：`mkdir src`

在 `public` 目录中创建 `index.html` 文件（这是服务应用的必要文件）：

```html
<html>
<body>
<script src="/bundle.js"></script>
</body>
</html>
```

该文件引用了 webpack 将生成并提供服务的 `bundle.js`

在 `src` 目录中创建包含基础内容的 `index.js` 文件：

```javascript
console.log('Hello, World!');
```

这是 webpack 打包的入口文件

#### 配置文件设置

在根目录创建 `webpack.config.js` 文件配置 webpack：

```javascript
const path = require('path');
module.exports = {
    entry: './src/index.js',
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    devServer: {
        contentBase: path.join(__dirname, 'public')
    }
};
```

- `entry`：指定入口文件（`src/index.js`）
- `output`：定义打包文件输出位置（`dist/bundle.js`）
- `devServer.contentBase`：指向存放静态文件（如 `index.html`）的 `public` 目录

注意在 1.14.0 版本中使用的是 `contentBase` 而非现代的 `static`，这反映了旧版 API 的特点

#### 启动开发服务器

通过以下命令启动开发服务器：

- 首选：`npx webpack-dev-server`
- 备选（若 npx 不可用）：`./node_modules/.bin/webpack-dev-server`

该命令将启动服务器，通常可通过 [http://localhost:8080](http://localhost:8080) 访问。服务器在内存中运行，文件不会写入磁盘而是动态提供服务，并启用实时重载功能以方便开发

#### 操作细节与注意事项

- **访问应用**：在浏览器中打开 [http://localhost:8080](http://localhost:8080)，应该能看到加载 `bundle.js` 并执行 JavaScript 的 `index.html`，控制台将输出 "Hello, World!"
- **实时更新**：编辑 `src` 中的文件时，服务器将自动重新编译并刷新浏览器，这是 webpack-dev-server 支持迭代开发的关键特性
- **端口冲突**：若 8080 端口被占用，服务器可能启动失败。可在 `webpack.config.js` 的 `devServer.port` 中指定其他端口，例如 `port: 9000`

#### 文件服务与路径考量

鉴于版本特性，`devServer.contentBase` 从指定目录提供文件服务（未设置时默认为当前目录）。确保 `index.html` 位于 `public` 目录中以便在根路径提供服务。脚本标签 `<script src="/bundle.js"></script>` 能正常工作是因为 `output.publicPath` 默认为 '/'，且 `output.filename` 为 'bundle.js'，使其可通过 `/bundle.js` 访问

一个重要细节是 webpack-dev-server 1.14.0 需要 HTML 文件才能提供服务，且不会自动注入脚本，因此需要在 `index.html` 中手动引入。这与现代配置中使用 `html-webpack-plugin` 等插件自动处理的方式形成对比

#### 兼容性与限制

这些版本发布于 2016 年，虽然功能完整但缺乏现代特性和安全补丁。需要检查与当前 Node.js 版本（截至 2025 年 3 月）的兼容性，旧版本可能需要 Node.js 6 或 8（这些版本已停止支持）。建议在当前 Node.js 版本（如 20.x）测试，但需准备应对可能的弃用警告

#### 表格：版本详情与使用说明

下表汇总了关键版本信息和使用注意事项：

| 组件               | 版本    | 发布年份 | 关键使用说明                                      |
|-------------------|---------|----------|-------------------------------------------------|
| Webpack           | 1.13.2  | 2016     | 模块打包器，需要配置入口/输出设置                  |
| Webpack-Dev-Server| 1.14.0  | 2016     | 开发服务器，使用 `contentBase` 配置静态文件目录    |

#### 高级配置选项

如需更多功能，可考虑在 `devServer` 中添加 `hot: true` 启用热模块替换：

```javascript
devServer: {
    contentBase: path.join(__dirname, 'public'),
    hot: true
}
```

这允许在不完全刷新页面的情况下更新模块，提升开发效率

#### 总结

本配置使用 webpack 1.13.2 和 webpack-dev-server 1.14.0 提供了基础但功能完整的开发环境。鉴于版本较旧，需注意与现代工作流程的差异，例如手动文件服务和与当前工具的潜在兼容性问题。由于缺乏更新，不建议在生产环境使用这些版本，但对于遗留项目维护，本指南应能满足需求

#### 主要参考资料

- [Webpack 详细设置指南](https://webpack.js.org/)
- [Webpack-dev-server 配置选项](<https://webpack.js.org> configuration/dev-server/)
