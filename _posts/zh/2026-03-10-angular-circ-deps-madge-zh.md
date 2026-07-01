---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Madge 检测 Angular 循环依赖
translated: true
type: note
---

## 什么是 Madge？

Madge 是一个开发者工具，用于生成模块依赖关系的视觉图表、查找循环依赖，并提供其他有用信息。它支持 JavaScript（AMD、CommonJS 和 ES6 模块），也支持 CSS 预处理器（Sass、Stylus 和 Less）。

---

## 步骤 1：安装 Madge

全局安装 Madge（或作为 dev dependency）：

```bash
# 全局安装
npm install -g madge

# 或作为 dev dependency
npm install --save-dev madge
```

如果要**生成视觉图表图像**，还需要安装 Graphviz：

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz
```

---

## 步骤 2：基本用法 — 检测循环依赖

在 Angular 项目**根目录**下运行：

```bash
# 扫描整个 src/ 文件夹的循环依赖
npx madge --circular src/
```

或者，为了更好地支持 TypeScript，指向 `main.ts` 并使用 `tsconfig.json`：

```bash
npx madge --circular src/main.ts --ts-config tsconfig.json
```

通过运行 `npx madge --circular --extensions ts ./` 可以快速获取当前目录及其子目录中所有 `.ts` 文件的循环依赖列表。

---

## 步骤 3：生成视觉依赖图

运行 `npx madge src/main.ts --ts-config tsconfig.json --image ./deps.png`，遍历整个应用程序并创建依赖图图像。这可用于识别循环依赖、可视化不同组件和服务之间的关系，并识别“意大利面条代码”场景。

要生成仅显示**循环**依赖的图表：

```bash
npx madge --circular --extensions ts --image circular-graph.png src/
```

**图表颜色说明：**

- **蓝色** — 有依赖的文件
- **绿色** — 没有依赖的文件
- **红色** — 有循环依赖的文件

---

## 步骤 4：有用命令总结

| 用途 | 命令 |
| --- | --- |
| 检测循环依赖 | `npx madge --circular src/` |
| 支持 TypeScript | `npx madge --circular --extensions ts src/` |
| 使用 tsconfig | `npx madge --circular src/main.ts --ts-config tsconfig.json` |
| 生成完整图表图像 | `npx madge --image deps.png src/main.ts --ts-config tsconfig.json` |
| 查找孤儿/死代码 | `npx madge --orphans src/main.ts --ts-config tsconfig.json` |

---

## 步骤 5：添加到 `package.json` Scripts

在 Angular 项目中，打开 `package.json` 并添加自定义脚本：

```json
"scripts": {
  "check:circles": "madge --circular src/",
  "check:graph": "madge --image dependency-graph.png src/"
}
```

然后随时运行：

```bash
npm run check:circles
```

---

## 步骤 6：跳过仅类型导入（推荐用于 Angular/TypeScript）

TypeScript 的 `import type` 语句可能导致假阳性。要跳过它们，请在 `package.json` 中添加此配置：

```json
"madge": {
  "detectiveOptions": {
    "ts": {
      "skipTypeImports": true,
      "skipAsyncImports": true
    },
    "tsx": {
      "skipTypeImports": true,
      "skipAsyncImports": true
    }
  }
}
```

---

## 步骤 7：添加到 CI/CD 流水线

将 Madge 添加到 CI/CD 流水线中，以防止循环依赖重新进入 Angular 项目。

GitLab CI 示例：

```yaml
stages:
  - test

circular-dependency-check:
  stage: test
  image: node:18
  script:
    - npm install madge -g
    - npm install
    - npm run check:circles
  allow_failure: false
```

---

## 示例输出

```
✖ 发现 3 个循环依赖！

1) src/app/services/service-a.ts → src/app/services/service-b.ts → src/app/services/service-a.ts
2) src/app/module-a.module.ts → src/app/module-b.module.ts → src/app/module-a.module.ts
```

---

## 如何修复循环依赖

要修复循环引用问题，请创建一个新文件来打破关系，确保文件之间的依赖是单向的，将公共依赖提取到单独的共享文件中。常见策略：

- **提取共享接口/类型**到单独的 `models/` 或 `shared/` 文件
- **创建共享模块**用于公共功能
- **重组模块**以分离关注点并确保单向依赖流

参考资料：

- [https://www.angulartraining.com/daily-newsletter/visualizing-internal-dependencies-with-madge/](https://www.angulartraining.com/daily-newsletter/visualizing-internal-dependencies-with-madge/)
- [https://www.npmjs.com/package/madge](https://www.npmjs.com/package/madge)
- [https://www.danywalls.com/how-to-detect-and-fix-circular-dependencies-in-typescript](https://www.danywalls.com/how-to-detect-and-fix-circular-dependencies-in-typescript)
- [https://angular.dev/errors/NG0919](https://angular.dev/errors/NG0919)
- [https://dev.to/greenroach/detecting-circular-dependencies-in-a-reacttypescript-app-using-madge-229](https://dev.to/greenroach/detecting-circular-dependencies-in-a-reacttypescript-app-using-madge-229)
