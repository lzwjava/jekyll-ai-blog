---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wrangler自动配置导致Hugo错误
translated: true
type: note
---

Question: 为什么我的 Cloudflare Worker 部署会运行 `npx hugo` 然后失败，而 sec-edgar-gpt 是一个 Worker，不是 Hugo 站点？

Answer:

Wrangler 的自动配置检测了你的仓库，误判为静态站点，并注入了 `npx hugo` 作为构建步骤。这个步骤不在你的构建命令中（显示为 "None"）——它来自 trace 中的 `runAutoConfig` / `maybeRunAutoConfig`。随后 `npx hugo` 失败，报错 `could not determine executable to run`，因为 Hugo 不是一个 npm 包（它是 Go 二进制文件），所以 npx 找不到可执行文件。

有两个问题：(1) 自动配置不应该对 Worker 触发；(2) 即使触发了，Hugo 也无法通过 npx 安装。

修复方法——显式固定所有配置，让 Wrangler 停止猜测。

确保 `wrangler.toml` 清晰声明 Worker：

```toml
name = "sec-edgar-gpt"
main = "src/index.js"   # 你的实际入口
compatibility_date = "2026-06-27"

# 禁止自动构建推断
[build]
command = ""
```

空的 `[build]` 命令告诉 Wrangler 没有需要构建的内容，从而抑制了注入 `hugo` 的框架检测路径。

同时检查 Cloudflare 控制面板的构建设置——部署命令是 `npx wrangler deploy`，这没问题，但如果较新版本的 Wrangler 执行了自动配置，请锁定版本：

```bash
npm i -D wrangler@latest   # 或一个已知稳定的版本
npx wrangler deploy
```

如果单独的 `[build]` 块无法阻止，则显式禁用自动配置：

```bash
WRANGLER_DISABLE_AUTOCONFIG=1 npx wrangler deploy
```

或在控制面板中将其设置为构建变量。根本原因是自动配置启发式错误分类了仓库；空构建命令加上禁用自动配置是彻底的解决方案。

如果你提供 `wrangler.toml` 和仓库结构，我会准确指出是哪一行触发了 Hugo 猜测。