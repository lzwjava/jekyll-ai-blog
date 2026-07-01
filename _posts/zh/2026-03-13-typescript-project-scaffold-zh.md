---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TypeScript 项目脚手架工具
translated: true
type: note
---

Question: 对于像 `copilot-api` 这样的项目（一个基于 TypeScript/Bun 的 Node.js CLI/server 项目），是否有类似于 Spring Initializr 的简单 init/scaffold 工具？

Answer:

是 — npm/Node.js 生态系统有几个工具，功能类似于 Spring Initializr。由于 `copilot-api` 使用 **TypeScript + Bun + tsdown** 作为其技术栈，这里是最相关的选项：

---

## 1. `create-tsdown` — 本项目最相关

由于 `copilot-api` 使用 `tsdown` 作为其 bundler（您可以在 repo 中看到 `tsdown.config.ts`），对于此技术栈，最接近 Spring Initializr 的等价工具是：

```bash
npm create tsdown@latest my-project
```

`create-tsdown` CLI 提供了一系列 starter templates，用于构建纯 TypeScript 库，以及像 React 和 Vue 这样的前端库，并允许您快速 scaffold 一个新项目。

注意：`tsdown` 被认为是 `tsup` 的更好继任者，并带有 `create-tsdown` 作为其 scaffolding 工具。

---

## 2. `npm create vite@latest` — 用于前端/通用 TS 项目

`create-vite` 是一个工具，用于从基本模板快速启动流行框架的项目，您可以使用 `--no-interactive` 标志完全跳过提示。

```bash
npm create vite@latest my-app -- --template vanilla-ts
```

支持的模板包括：`vanilla`、`vanilla-ts`、`react`、`react-ts`、`vue`、`vue-ts`、`svelte`、`svelte-ts` 等。

---

## 3. `degit` — 克隆任何 GitHub 模板而不带 Git 历史

`degit` 允许您直接从任何 GitHub 模板 scaffold 项目，而不复制完整的 git 历史。

```bash
npx degit user/repo my-project
cd my-project
npm install
```

如果您想将像 `copilot-api` 本身这样的东西克隆作为起始模板，这很理想：

```bash
npx degit ericc-ch/copilot-api my-proxy-project
```

---

## 4. 带标志的 `npm init` — 快速基础设置

对于最简单的启动，您可以运行带内联标志的 `npm init`，以完全避免交互式提示，例如 `npm init --init-type="module" --init-license="MIT" --yes`，立即创建一个 ESM-ready 项目。

---

## 比较表格

| 工具 | 最适合 | 命令 |
| --- | --- | --- |
| `create-tsdown` | TypeScript library/CLI（与 copilot-api 相同的技术栈） | `npm create tsdown@latest` |
| `create-vite` | 前端 + TS 应用 | `npm create vite@latest` |
| `degit` | 克隆任何 GitHub 模板 | `npx degit user/repo` |
| `npm init` | 最基本的设置 | `npm init --yes` |

---

## 推荐用于 copilot-api 风格的项目

由于 `copilot-api` 本质上是一个使用 Bun 和 tsdown 构建的 **TypeScript CLI/server**，最佳工作流程是：

```bash
# 选项 A：使用 create-tsdown（最接近 Spring Initializr 体验）
npm create tsdown@latest my-project

# 选项 B：将 copilot-api 本身克隆为模板
npx degit ericc-ch/copilot-api my-project
cd my-project
bun install
```

然后自定义 `src/`、`package.json` 和 `tsdown.config.ts` 以满足您的需求。

参考资料：

- [tsdown Getting Started](https://tsdown.dev/guide/getting-started)
- [create-vite on npm](https://www.npmjs.com/package/create-vite)
- [degit usage via create-vite docs](https://www.npmjs.com/package/create-vite-init)
- [copilot-api GitHub repo](https://github.com/ericc-ch/copilot-api)
