---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 精确的 Lockfile 安装
translated: true
type: note
---

**Question:** 解释 `npm ci` 的作用

**Answer:**

`npm ci` 是一个专门为 **clean and reproducible installations（清洁且可复现的依赖安装）** 设计的命令 —— 常用于 CI/CD pipelines、Docker builds、自动化测试以及 production-like 环境。

### 核心区别：`npm install` vs `npm ci`

| 特性 | `npm install` (或 `npm i`) | `npm ci` |
| ------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| 读取文件 | `package.json` | `package-lock.json` (必须) |
| 写入 / 更新 | `package-lock.json` (如果缺失或过时) | 永远不会修改 `package-lock.json` |
| 创建 / 删除 `node_modules` | 通常只添加缺失的 packages | **总是先删除** 现有的 `node_modules` |
| `package-lock.json` 缺失时允许？ | 是 | **否** — 会报错失败 |
| 安装精确版本 | 尝试安装 (如果 lockfile 存在)，但仍可能变动 | **总是** 根据 lockfile 安装精确版本 |
| 能否安装新 packages | 是 (`npm install lodash`) | **否** — 尝试安装会报错 |
| 速度 | 当 lockfile 过时时较慢 | 通常更快 (不需要 dependency resolution) |
| 主要使用场景 | 本地开发、添加/更新 packages | CI, CD, Docker, production builds, tests |

### `npm ci` 具体执行步骤

1. 删除现有的 `node_modules` 文件夹 (如果存在)
2. 检查 `package-lock.json` 是否存在 —— 如果不存在 → 失败
3. **仅**读取 `package-lock.json` (忽略 `package.json` 中的版本号)
4. **精确**安装 lockfile 中描述的 dependency tree
5. **不**更新或重新生成 lockfile
6. **不**运行依赖项的 `prepare` scripts (自 7.x 版本起 —— 速度更快)

### 典型的真实使用场景

```bash
# 在 CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI, Jenkins 等)
npm ci
npm test

# 在 Dockerfile 中 — 非常常见的模式
COPY package.json package-lock.json ./
RUN npm ci --omit=dev          # 在旧版本中使用 --production
COPY . .
```

```bash
# 本地开发 — 通常你仍然使用：
npm install

# 但有时你想完全复现 CI 环境：
rm -rf node_modules
npm ci
```

### 常见错误信息及其含义

```
npm ERR! ci can only install packages with an exact version number in package-lock.json
→ 你修改了 package.json 但没有运行 npm install 来更新 lockfile

npm ERR! Missing script: "ci"
→ 并非缺少 script，通常意味着 package-lock.json 缺失

npm ERR! cb() never called!
→ 现在非常罕见 — 通常意味着磁盘空间不足或 cache 问题
```

### 快速判断准则

- 正在开发 / 添加 / 更新 dependencies → `npm install`
- 想要与 lockfile 中完全一致的 dependency tree (CI, tests, Docker, production builds) → `npm ci`

**核心结论：**
`npm ci` = "完全按照 package-lock.json 安装，不进行任何改动，也不触碰 lockfile"

**References:**

- <https://docs.npmjs.com/cli/v10/commands/npm-ci>
- <https://blog.npmjs.org/post/178027064160/next-generation-package-management>
