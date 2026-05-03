---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复过期的OpenClaw插件条目
translated: true
type: note
---

两种解决方式：

**方案 1 —— 使用 doctor 自动清理（推荐）：**
```
openclaw doctor --fix
```
该命令会从配置中移除过时的 `brave` 条目（`plugins.entries.brave` + `plugins.installs.brave`）。此操作仅执行清理，不会重新安装。

**方案 2 —— 重新安装：**
```
openclaw plugins install @openclaw/brave-plugin
```
如果你确实需要重新启用 Brave 插件，请使用此方案。如果 npm 上已不存在该包，安装将失败 —— 此时方案 1 是正确选择。

**问题根源：** Brave 插件的包目录（`/home/lzw/.openclaw/npm/node_modules/@openclaw/brave-plugin`）在更新验证过程中缺失。OpenClaw 曾尝试自动恢复但失败（很可能是因为该包已不在 npm 上）。配置中仍保留着陈旧条目，因此反复出现警告。

运行 `doctor --fix` 后，请同时移除其警告中提示的冗余 `plugins.load.paths` 条目 —— 该操作可在同一次运行中完成。