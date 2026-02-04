---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: npm 中的 Install 与 Update
translated: true
type: note
---

`npm install` 和 `npm update` 之间的主要区别：

## **npm install**

- **安装** `package.json` 中列出但尚未在 `node_modules` 中的 packages
- 遵循 `package.json` 中指定的 **exact version ranges**（例如 `^1.2.3`）
- 创建或更新 `package-lock.json` 以锁定这些版本
- 如果在 packages 已安装的情况下运行，通常不会执行任何操作（除非 lock file 丢失）

## **npm update**

- 将 `node_modules` 中现有的 packages **更新**到仍符合 `package.json` 范围的最新版本
- 不会安装尚未存在的 packages
- 使用新版本更新 `package-lock.json`
- 例如，如果 `package.json` 中是 `^1.2.3` 且已安装版本为 1.2.3，`npm update` 可能会将其升级到 1.9.0（但不会升级到 2.0.0）

## **Quick example:**

```json
// package.json 显示: "lodash": "^4.17.0"
// 当前已安装: 4.17.0
// 最新可用版本: 4.17.21
```

- `npm install` → 保持 4.17.0（已满足要求）
- `npm update` → 升级到 4.17.21（`^` 范围内的最新版本）

**In practice：** 对于全新设置或添加新 packages，请使用 `npm install`。当你想在允许的范围内获取现有 dependencies 的更新版本时，请使用 `npm update`。