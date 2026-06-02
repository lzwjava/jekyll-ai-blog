---
audio: false
generated: true
lang: zh
layout: post
title: 使用PostCSS转换CSS
translated: true
type: note
---

我将解释如何在前端项目中使用 PostCSS。PostCSS 是一个通过 JavaScript 插件转换 CSS 的工具，提供自动添加前缀、压缩和未来 CSS 语法支持等功能。以下是详细步骤：

### 1. **项目初始化**
确保你有一个已安装 Node.js 的前端项目。如果没有，请初始化：
```bash
mkdir my-project
cd my-project
npm init -y
```

### 2. **安装 PostCSS 及相关工具**
安装 PostCSS、PostCSS CLI 以及所需插件（如用于厂商前缀的 `autoprefixer` 或用于压缩的 `cssnano`）：
```bash
npm install --save-dev postcss postcss-cli autoprefixer cssnano
```

### 3. **创建 CSS 文件**
创建源 CSS 文件，例如 `src/styles.css`：
```css
/* src/styles.css */
.container {
  display: flex;
  transition: all 0.3s ease;
}
```

### 4. **配置 PostCSS**
在项目根目录创建 `postcss.config.js` 文件来配置插件：
```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer'), // 添加厂商前缀
    require('cssnano')({ preset: 'default' }) // 压缩 CSS
  ]
};
```

### 5. **添加构建脚本**
在 `package.json` 中添加处理 CSS 的脚本：
```json
"scripts": {
  "build:css": "postcss src/styles.css -o dist/styles.css"
}
```
- `src/styles.css`：输入文件
- `dist/styles.css`：输出文件

### 6. **运行 PostCSS**
执行构建命令：
```bash
npm run build:css
```
这会处理 `src/styles.css` 并输出转换后的 CSS 到 `dist/styles.css`。例如，`autoprefixer` 会添加前缀，`cssnano` 会进行压缩：
```css
/* dist/styles.css */
.container{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-transition:all .3s ease;transition:all .3s ease}
```

### 7. **与构建工具集成（可选）**
如需更完善的配置，可将 PostCSS 与 Webpack、Vite 或 Gulp 等工具集成：

#### **在 Vite 中使用**
如果使用 Vite，安装 `postcss` 并在 `vite.config.js` 中配置：
```javascript
// vite.config.js
import postcss from 'postcss';
import autoprefixer from 'autoprefixer';

export default {
  css: {
    postcss: {
      plugins: [autoprefixer()]
    }
  }
};
```
Vite 会在导入 CSS 文件时自动处理 PostCSS。

#### **在 Webpack 中使用**
安装 `postcss-loader`：
```bash
npm install --save-dev postcss-loader
```
更新 `webpack.config.js`：
```javascript
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader']
      }
    ]
  }
};
```

### 8. **监听文件变更（可选）**
如需在开发时自动处理 CSS，修改 `package.json` 中的脚本：
```json
"scripts": {
  "watch:css": "postcss src/styles.css -o dist/styles.css --watch"
}
```
运行 `npm run watch:css` 即可监听文件变化。

### 9. **常用插件**
以下是常用的 PostCSS 插件：
- `autoprefixer`：根据浏览器支持度添加厂商前缀
- `cssnano`：压缩 CSS
- `postcss-preset-env`：让你提前使用未来 CSS 特性
- `postcss-import`：解析 `@import` 规则
按需安装插件：
```bash
npm install --save-dev postcss-preset-env postcss-import
```
在 `postcss.config.js` 中配置：
```javascript
module.exports = {
  plugins: [
    require('postcss-import'),
    require('postcss-preset-env'),
    require('autoprefixer'),
    require('cssnano')({ preset: 'default' })
  ]
};
```

### 完整工作流示例
1. 在 `src/styles.css` 中编写现代 CSS：
```css
@custom-media --viewport-medium (width >= 768px);

:root {
  --main-color: #1a73e8;
}

.container {
  color: var(--main-color);
  display: grid;
}

@media (--viewport-medium) {
  .container {
    grid-template-columns: 1fr 1fr;
  }
}
```
2. 运行 `npm run build:css`
3. 在 `dist/styles.css` 中获得已添加前缀、解析变量并压缩的 CSS

### 实用技巧
- 在 CLI 中使用 `--map` 参数（`postcss src/styles.css -o dist/styles.css --map`）可生成用于调试的 source map
- 查阅插件文档了解具体配置选项
- 通过将输出 CSS 链接到 HTML 或打包器，与 React、Vue 等前端框架结合使用

如有特定配置或插件需求，欢迎随时咨询！
