---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 调试 Angular Stack Overflow 解决方案
translated: true
type: note
---

**问题：** 我们能否更新 ivy/index.js 源代码，在那里输出堆栈（以调试 Angular 迁移期间的 "Maximum call stack size exceeded" 错误）？

**回答：**

是的——技术上是可能的，但这**通常不是一个好或实用的解决方案**。以下是原因，以及你可以做什么。

### 为什么修补 @ngtools/webpack/src/ivy/index.js 很困难 / 不推荐

- 该文件位于 `node_modules/@ngtools/webpack/src/ivy/index.js` 内
- 它是编译/转译包的一部分——真正的逻辑位于 Angular 仓库中的 TypeScript 源代码中
- node_modules 通常在每次 `npm install` / `npm ci` 时被覆盖
- 即使你修补它，大多数团队都认为这是一个维护噩梦（在下次 `@angular-devkit/build-angular` 更新时会中断）

### 获取更好堆栈跟踪的实际方法

1. **最佳且最干净的选项：使用 NODE_OPTIONS --stack-trace-limit**

   大多数现代 node 版本都尊重此标志：

   ```bash
   # 先尝试 200–500，然后如果需要再提高
   NODE_OPTIONS="--stack-trace-limit=300" ng build

   # 或者更高
   NODE_OPTIONS="--stack-trace-limit=1000" ng build --verbose
   ```

   这通常会显示额外 5–15 个帧，并通常告诉你**哪个文件 / 符号 / 装饰器 / 导入**导致了递归。

2. **使用 patch-package 临时修补（最可控的方式）**

   步骤：

   ```bash
   npm install --save-dev patch-package
   ```

   - 打开 `node_modules/@ngtools/webpack/src/ivy/index.js`
   - 找到抛出 RangeError 的地方（搜索 "Maximum call stack size exceeded"）
   - 像这样替换 / 包装它：

     ```js
     // 原始代码大致如下：
     throw new Error("Maximum call stack size exceeded");

     // 改为：
     const err = new Error("Maximum call stack size exceeded");
     err.stack = new Error().stack;           // 捕获更完整的堆栈
     console.error("[IVY PATCH] Deep recursion detected");
     console.error(err.stack);
     throw err;
     ```

   - 然后运行：

     ```bash
     npx patch-package @ngtools/webpack
     ```

   - 提交生成的 `patches/@ngtools+webpack+...patch` 文件
   - 在 package.json 的 scripts 中添加 `"postinstall": "patch-package"`

   → 现在每次 `npm install` 时，修补都会自动应用。

3. **使用调试器而不是修补**

   - 在你的 `package.json` scripts 中添加：

     ```json
     "build:debug": "node --inspect-brk ./node_modules/@angular-devkit/build-angular/src/dev-server/index.js"
     ```

   - 或者更简单——仅以 inspect 模式运行构建器：

     ```bash
     node --inspect-brk ./node_modules/.bin/ng build
     ```

   - 打开 chrome://inspect → 连接 → 在抛出 "Maximum call stack size exceeded" 的行上设置断点
   - 当它暂停时，在 Chrome DevTools 中查看调用堆栈

4. **快速且粗糙的方法 – 运行时 monkey-patch**

   创建一个文件 `debug-ivy.js`：

   ```js
   const originalError = Error;

   Error = function (...args) {
     const err = new originalError(...args);
     if (args[0]?.includes?.("Maximum call stack size exceeded")) {
       console.error("[DEBUG] Ivy recursion crash");
       console.error(new originalError().stack); // 捕获外部堆栈
       console.error(err.stack);
     }
     return err;
   };
   Error.prototype = originalError.prototype;
   ```

   然后运行：

   ```bash
   node -r ./debug-ivy.js ./node_modules/.bin/ng build
   ```

### 总结 – 推荐顺序

1. 首先尝试 → `NODE_OPTIONS="--stack-trace-limit=500" ng build --verbose`
2. 如果仍不足 → 使用 `patch-package` 修补 ivy/index.js（最易维护）
3. 如果真的需要深度调试 → 使用 `--inspect-brk` + Chrome 调试器
4. 避免直接编辑 node_modules 而不用 patch-package

在 95% 的真实案例中，人们在通过 `--stack-trace-limit` 查看额外 30–50 个堆栈帧后，就能解决底层循环导入问题。

修补源代码是可能的——但应该是你的最后手段，而不是首选。

**参考：**

- <https://github.com/angular/angular-cli/issues?q=is%3Aissue+label%3A%22type%3A+bug%22+%22Maximum+call+stack%22>
- <https://stackoverflow.com/questions/73197135/angular-14-ng-serve-error-ngtools-webpack-src-ivy-index-js-error-maximum>
