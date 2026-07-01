---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular tsconfig.json 指南精要
translated: true
type: note
---

**问题：** `tsconfig.json` 在 Angular 项目中如何工作？

**答案：**

## 概述

Angular 项目中的 `tsconfig.json` 文件在 TypeScript 编译过程中扮演着关键角色。它是一个配置文件，向 TypeScript 编译器提供将 TypeScript 代码编译成 JavaScript 的指示。

目录中存在 `tsconfig.json` 文件表明该目录是 TypeScript 项目的根目录。它指定了根文件以及编译项目所需的编译器选项。

---

## Angular 中的多个 tsconfig 文件

使用 CLI 生成新 Angular 项目时，通常会得到 **三个 tsconfig 文件**：

| File | Purpose |
| --- | --- |
| `tsconfig.json` | 整个项目的根/基础配置 |
| `tsconfig.app.json` | 构建应用程序时使用的配置 |
| `tsconfig.spec.json` | 运行单元测试时使用的配置 |

`tsconfig.json` 文件可以使用 `extends` 属性继承另一个文件的配置。`extends` 是一个顶级属性（与 `compilerOptions`、`files`、`include` 和 `exclude` 并列）。其值是一个字符串，包含要继承的另一个配置文件路径。基础文件的配置首先加载，然后被继承配置文件中的配置覆盖。

例如，`tsconfig.app.json` 通常如下所示：

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "./out-tsc/app",
    "types": []
  },
  "files": ["src/main.ts"],
  "include": ["src/**/*.ts"],
  "exclude": ["src/test.ts", "src/**/*.spec.ts"]
}
```

---

## tsconfig.json 的顶级结构

它允许开发者指定编译器选项、包含/排除文件，并定义项目的结构。主要部分包括：

```json
{
  "compilerOptions": { },
  "include": [ ],
  "exclude": [ ],
  "angularCompilerOptions": { }
}
```

---

## 部分 1：`compilerOptions`

`compilerOptions` 属性是一个对象，用于指定 TypeScript 编译器选项。该属性在每个 `tsconfig.json` 文件中都是必需的，并为编译器提供有关需要编译的代码的重要信息。

关键选项说明：

| Option | Description |
| --- | --- |
| `target` | 编译成的 JavaScript 版本（例如 `es2020`） |
| `module` | 模块格式；Angular 通过 `esnext` 受益于 tree-shaking |
| `moduleResolution` | 模块解析方式；使用 `node` 以匹配 Node.js 行为 |
| `lib` | 可用内置 API（例如 `es2020`、`dom`） |
| `strict` | 启用所有严格类型检查选项 |
| `noImplicitAny` | 禁止隐式 `any` 类型的变量 |
| `sourceMap` | 为调试生成 source map 文件 |
| `skipLibCheck` | 跳过 `.d.ts` 声明文件的类型检查，从而加速构建 |
| `esModuleInterop` | 允许从 CommonJS 模块进行默认导入 |
| `resolveJsonModule` | 允许在 TypeScript 中导入 `.json` 文件 |
| `baseUrl` | 设置解析非相对模块名称的基础目录 |
| `paths` | 将自定义导入别名映射到实际文件夹路径 |

---

## 部分 2：`include` 和 `exclude`

`include` 属性是一个文件 glob 数组，指定应包含在编译过程中的文件。默认情况下，编译器将包含项目中所有未被 `exclude` 属性排除的文件。

`exclude` 选项仅更改由于 `include` 设置而包含的文件。它不会防止文件被包含——它只是更改 `include` 设置找到的内容。如果代码中有 import 语句，`exclude` 中指定的文件仍可能成为代码库的一部分。

示例：

```json
"include": ["src/**/*.ts"],
"exclude": ["node_modules", "dist", "e2e"]
```

---

## 部分 3：`angularCompilerOptions`

此部分是 **Angular 专属** 的，用于控制 Angular 模板编译器（Ivy）。重要选项包括：

| Option | Description |
| --- | --- |
| `strictInjectionParameters` | 强制执行正确的注入参数类型 |
| `strictInputAccessModifiers` | 验证输入绑定访问修饰符 |
| `fullTemplateTypeCheck` | 在 HTML 模板中启用类型检查（在 Angular 13+ 中已弃用） |
| `strictTemplates` | `fullTemplateTypeCheck` 的现代替代品 |

---

## 部分 4：路径别名（奖励最佳实践）

路径映射对于简化导入并避免长相对路径非常有用。`baseUrl` 设置解析非相对模块名称的基础目录，而 `paths` 将自定义路径映射到特定文件夹，使导入更简洁。

```json
"compilerOptions": {
  "baseUrl": "./",
  "paths": {
    "@app/*": ["src/app/*"],
    "@assets/*": ["src/assets/*"]
  }
}
```

这允许您使用 `import { MyService } from '@app/services/my.service'` 而不是 `../../services/my.service`。

---

## 部分 5：错误处理选项

`noEmitOnError` 防止编译器在存在任何错误时发出输出。这确保只生成干净、无错误的构建——在 CI/CD 管道中很有用。

---

## 优化的 Angular tsconfig.json 完整示例

```json
{
  "compileOnSave": false,
  "compilerOptions": {
    "target": "es2020",
    "module": "esnext",
    "moduleResolution": "node",
    "lib": ["es2020"],
    "skipLibCheck": true,
    "strict": true,
    "noImplicitAny": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "sourceMap": true,
    "noEmitOnError": true,
    "baseUrl": "./",
    "paths": {
      "@app/*": ["src/app/*"],
      "@assets/*": ["src/assets/*"]
    }
  },
  "angularCompilerOptions": {
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "e2e"]
}
```

---

**参考资料：**

- [Almost Perfect tsconfig.json Options for Angular Projects – Medium](https://medium.com/@sehban.alam/almost-perfect-tsconfig-json-options-for-your-angular-projects-5bec056f23d8)
- [Angular Compiler Options – angular.dev](https://angular.dev/reference/configs/angular-compiler-options)
- [What is a tsconfig.json – TypeScript Official Docs](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
- [TSConfig Reference – TypeScript](https://www.typescriptlang.org/tsconfig/)
- [Angular tsconfig.json file decoded – LinkedIn](https://www.linkedin.com/pulse/angular-tsconfigjson-file-decoded-guru-samrudh)
