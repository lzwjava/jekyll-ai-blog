---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM 安装行为修饰符指南
translated: true
type: note
---

以下是类似的 npm install 选项，它们可以修改行为而无需执行完整安装：

**Lock file 相关：**

- `--package-lock-only` - 仅更新 package-lock.json，不安装软件包
- `--no-package-lock` - 完全不读取或写入 package-lock.json
- `--lockfile-version <n>` - 设置 lockfile 格式版本（1、2 或 3）

**Dry run / 模拟：**

- `--dry-run` (或 `-n`) - 显示将要发生的情况，而不实际安装或修改任何内容

**安装范围：**

- `--global` (或 `-g`) - 全局安装软件包而不是本地安装
- `--production` - 仅安装 dependencies，跳过 devDependencies
- `--omit=dev` - 跳过 devDependencies（较新语法）
- `--omit=optional` - 跳过 optionalDependencies
- `--only=prod` - 仅安装 production dependencies（较旧语法）
- `--only=dev` - 仅安装 devDependencies

**Package resolution（包解析）：**

- `--legacy-peer-deps` - 忽略 peer dependency 冲突（使用旧版 npm 6 行为）
- `--strict-peer-deps` - 如果无法满足 peer dependency 要求，则安装失败
- `--force` - 即使存在冲突也强制安装

**Cache（缓存）相关：**

- `--prefer-offline` - 优先使用缓存的软件包，仅在需要时访问网络
- `--offline` - 仅使用缓存的软件包，绝不访问网络
- `--no-audit` - 安装期间跳过 security audit

**其他实用选项：**

- `--ignore-scripts` - 不运行 pre/post install 脚本
- `--no-save` - 安装软件包但不更新 package.json

这些选项让你能够精细控制 npm 在安装期间的执行行为。