---
audio: false
generated: true
lang: zh
layout: post
title: 使用Autoprefixer
translated: true
type: note
---

我将解释如何在前端开发中使用 Autoprefixer。Autoprefixer 是一个 PostCSS 插件，能自动为 CSS 添加浏览器厂商前缀，确保跨浏览器兼容性。

以下是集成 Autoprefixer 到前端工作流的主要方式：

1. 使用 npm（最常用方式）

```bash
# 安装 autoprefixer 和 postcss
npm install autoprefixer postcss --save-dev
```

2. 基于 PostCSS CLI 的基础配置

```bash
# 安装 postcss-cli
npm install postcss-cli --save-dev

# 创建 postcss.config.js 文件
module.exports = {
  plugins: [
    require('autoprefixer')
  ]
}

# 添加到 package.json 的 scripts 中
"scripts": {
  "build:css": "postcss src/styles.css -o dist/styles.css"
}
```

3. 与构建工具结合：

a) Webpack 配合 postcss-loader

```bash
npm install postcss-loader --save-dev
```

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['autoprefixer']
              }
            }
          }
        ]
      }
    ]
  }
}
```

b) Vite（内置支持）

```javascript
// vite.config.js
import autoprefixer from 'autoprefixer'

export default {
  css: {
    postcss: {
      plugins: [autoprefixer()]
    }
  }
}
```

4. 配置选项

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('autoprefixer')({
      overrideBrowserslist: ['> 1%', 'last 2 versions'], // 目标浏览器
      grid: true, // 启用网格布局前缀
      flexbox: 'no-2009' // Flexbox 支持选项
    })
  ]
}
```

5. CSS 使用示例

```css
/* 输入 */
.container {
  display: flex;
  justify-content: space-between;
}

/* 输出（经 Autoprefixer 处理后） */
.container {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
```

核心特性与使用技巧：

- 基于 Can I Use 数据自动添加前缀
- 通过 browserslist 配置控制（通常位于 package.json）
- 自动移除旧版 CSS 中的过时前缀
- 支持现代 CSS 特性如自定义属性

package.json 中的基础 browserslist 配置示例：

```json
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead"
  ]
}
```

运行方式：

```bash
# 使用 PostCSS CLI
npx postcss src/*.css --dir dist

# 或使用 npm 脚本
npm run build:css
```

请根据项目现有构建体系（Webpack、Vite 等）选择合适的集成方案。在现代前端开发中，Webpack 或 Vite 方案最为常见，因其能很好地与现有构建流程集成。
