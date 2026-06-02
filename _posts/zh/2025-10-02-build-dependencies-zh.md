---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 开发依赖与构建工具
translated: true
type: note
---

### 开发依赖
这些是开发过程中使用的包，不会包含在最终构建中。

- **babel-core** (6.13.0)：Babel 核心编译器，用于将现代 JavaScript (ES6+) 转译为 ES5 以实现更广泛的浏览器兼容性。
- **babel-loader** (6.2.5)：Webpack 加载器，在构建过程中集成 Babel 进行 JavaScript 转换。
- **babel-plugin-transform-runtime** (6.12.0)：Babel 插件，可重用运行时辅助函数以减少转译代码的打包体积。
- **babel-preset-es2015** (6.13.2)：Babel 预设，用于将 ES2015 (ES6) 特性编译为 ES5。
- **babel-runtime** (6.11.6)：运行时库，为 Babel 转译的代码提供 polyfill 和辅助函数。
- **cross-env** (^1.0.8)：跨平台设置环境变量（例如 NODE_ENV），不受 shell 差异影响。
- **css-loader** (^0.23.1)：加载并处理 CSS 文件，解析导入和依赖关系。
- **detect-indent** (4.0.0)：检测文件的缩进风格（空格/制表符）以保持格式一致。
- **exports-loader** (^0.6.3)：使模块导出在不同上下文中可用（例如用于非 AMD 模块）。
- **extract-text-webpack-plugin** (^1.0.1)：将 CSS 从 JavaScript 包中提取到单独的文件中，以提高性能。
- **file-loader** (0.9.0)：处理文件加载（例如图像），将其发送到输出目录并返回 URL。
- **html-webpack-plugin** (^2.22.0)：生成 HTML 文件并注入打包后的资源，简化单页应用设置。
- **rimraf** (^2.5.4)：跨平台递归文件删除（类似于 Unix 上的 rm -rf）。
- **style-loader** (^0.13.1)：通过 style 标签将 CSS 注入 DOM，实现动态加载。
- **stylus** (^0.54.5)：CSS 预处理器，具有富有表现力的语法，可编译为 CSS。
- **stylus-loader** (^2.1.1)：Webpack 加载器，用于将 Stylus 文件处理为 CSS。
- **url-loader** (0.5.7)：对小文件（例如图像）进行 Base64 编码内联或发送较大的文件；回退到 file-loader。
- **vue-hot-reload-api** (^1.2.0)：在开发过程中为 Vue.js 组件启用热模块替换。
- **vue-html-loader** (^1.0.0)：Webpack 加载器，用于解析 Vue 单文件组件中的 HTML 模板。
- **vue-loader** (8.5.3)：加载并处理 Vue 单文件组件（.vue 文件）为 JavaScript 和 CSS。
- **vue-style-loader** (^1.0.0)：处理来自 Vue 组件的 CSS，与 style-loader 集成。
- **webpack** (1.13.2)：模块打包器，用于构建和优化 Web 资源（如 JS、CSS 和图像）。
- **webpack-dev-server** (1.14.0)：开发服务器，支持实时重新加载和热模块替换。

### 运行依赖
这些是包含在最终应用程序构建中的运行时包。

- **debug** (^2.2.0)：调试工具，具有命名空间日志记录和条件输出（仅通过 DEBUG 环境变量启用）。
- **es6-promise** (^3.0.2)：在旧版浏览器/环境中为 ES6 Promise API 提供 polyfill。
- **font-awesome** (^4.6.3)：流行的图标库，通过 CSS 类提供可缩放矢量图标。
- **github-markdown-css** (^2.4.0)：用于样式化 GitHub 风格 Markdown 的 CSS。
- **highlight.js** (^9.6.0)：语法高亮器，支持多种语言的代码块。
- **hls.js** (^0.7.6)：JavaScript 库，用于通过 HTML5 视频播放 HTTP 直播流 (HLS) 视频。
- **inherit** (^2.2.6)：用于 JavaScript 对象中经典和原型继承的实用工具。
- **jquery** (^3.1.0)：快速、功能丰富的 JavaScript 库，用于 DOM 操作、AJAX 和事件处理。
- **json-loader** (^0.5.4)：将 JSON 文件作为 JavaScript 模块加载。
- **leancloud-realtime** (^3.2.3)：用于 LeanCloud 实时消息传递和数据同步服务的 SDK。
- **marked** (^0.3.6)：Markdown 解析器，可将 Markdown 转换为 HTML。
- **moment** (^2.14.1)：日期/时间操作库，用于解析、验证和格式化日期。
- **moment-timezone** (^0.5.7)：Moment.js 的扩展，用于处理时区和夏令时。
- **qiniu-js-sdk** (0.0.2)：用于与七牛云存储交互（上传/下载文件）的 JavaScript SDK。
- **raw-loader** (^0.5.1)：Webpack 加载器，将文件作为原始字符串加载（例如文本模板）。
- **rupture** (^0.6.1)：Stylus 的媒体查询扩展，为响应式设计提供断点。
- **sprintf-js** (^1.0.3)：JavaScript sprintf 实现，用于带占位符的字符串格式化。
- **vue** (^1.0.26)：用于构建用户界面的渐进式 MVVM 框架（v1.x，较旧版本）。
- **vue-resource** (^0.6.1)：Vue.js 的 HTTP 客户端，用于简化 AJAX/API 请求。
- **vue-router** (^0.7.13)：Vue.js 的官方路由器，支持单页应用导航。
- **vue-spinner** (^1.0.2)：Vue.js 的旋转加载器/加载组件库。
- **vue-weui** (^0.3.2)：WeUI 组件的 Vue.js 包装器（用于微信风格界面的 UI 库）。
- **weixin-js-sdk** (^1.2.0)：微信 JavaScript SDK，用于集成微信网页功能（例如分享、扫描）。
- **weui** (^0.4.3)：WeUI CSS 框架，用于构建受微信设计启发的移动界面。
- **word-color** (^1.2.0)：根据哈希或语言等因素为单词着色的库，可能用于热图类效果。
