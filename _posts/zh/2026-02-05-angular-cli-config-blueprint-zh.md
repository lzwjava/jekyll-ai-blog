---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular CLI 配置蓝图指南
translated: true
type: note
---

**angular.json** 是 Angular CLI 项目的主要配置文件。它定义了项目的结构，以及 CLI 如何进行 build、serve 和 test 你的应用程序。

**它包含的关键内容：**

**Project configuration** - 如果在一个 workspace 中有多个 apps 或 libraries，每个项目都会在这里定义其专属设置。

**Build options** - 指定 source files 的位置、built files 的输出目录、需要复制的 assets、包含的 style 文件、polyfills 等。

**Architect targets** - 针对不同 CLI 命令的配置，例如：

- `build` - 如何编译你的 app
- `serve` - dev server 设置（port、proxy config 等）
- `test` - testing 配置
- `lint` - linting 规则

**Different environments** - 你可以为 development、production、staging 等环境定义不同的配置（例如是否启用 source maps、optimization 级别、base URLs）。

**示例结构：**

```json
{
  "projects": {
    "my-app": {
      "architect": {
        "build": {
          "options": {
            "outputPath": "dist/my-app",
            "index": "src/index.html",
            "main": "src/main.ts",
            "styles": ["src/styles.css"]
          },
          "configurations": {
            "production": {
              "optimization": true,
              "sourceMap": false
            }
          }
        }
      }
    }
  }
}
```

当你运行类似 `ng build --configuration=production` 的命令时，CLI 会读取 angular.json 以了解执行该 build 的具体方式。它基本上是 CLI 在执行所有项目操作时遵循的蓝图。
