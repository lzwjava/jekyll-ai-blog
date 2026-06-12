---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes 更新在 Web UI 构建时挂起
translated: true
type: note
---

**问题：** 为什么在执行 `hermes update`（Hermes Agent）时，在安装了 repo 根目录 + ui-tui 和 web 工作区包之后，会卡在 "→ Building web UI..." 这一步？

**回答：**

几乎可以确定它没有卡住——只是没有输出。“Building web UI...” 这一步会运行 web 工作区的构建脚本，内容是：

```
tsc -b && vite build
```

`hermes update` 的旋转动画会吞掉子进程的标准输出，直到该步骤完成，而 `tsc -b`（TypeScript 项目引用构建）在进行类型检查时**不会输出任何内容**。在冷缓存（全新的 `node_modules`、没有 `.tsbuildinfo`）下，`tsc -b` 处理约 2200+ 个模块可能需要几分钟——尤其是在你的 16 GB M2 Air 上，tsc 加上 npm 残留的内存压力可能会让你进入交换状态。一旦 tsc 完成，vite 部分本身只需要约 3 秒，正如仓库中最近一份相同的报告所显示的那样：在 macOS 上执行相同的更新序列，显示“added 769 packages in 7s ✓ repo root + ui-tui, web workspaces (desktop skipped) → Building web UI...” 旋转动画会停留一段时间，然后最终完成并显示“vite v7.3.2 ... ✓ 2257 modules transformed ... ✓ built in 2.92s ✓ Web UI built”。

与其猜测，不如花 30 秒调试一下：

```bash
# 1. 真的在工作吗？查看 tsc/vite 是否在消耗 CPU
ps aux | grep -E 'tsc|vite|esbuild' | grep -v grep
# tsc 占用 ~100% CPU = 正在构建，没有挂起

# 2. 如果你想看到真实输出，终止 update 并手动构建
cd ~/.hermes/hermes-agent/web
npx tsc -b --verbose   # 显示每个项目的进度
npm run build          # 完整的 vite 输出

# 3. 然后继续
hermes update
```

趁此机会可以修复两件事：

1. **Node 版本。** 同样的日志显示 npm EBADENGINE 警告：`@icons-pack/react-simple-icons@13.13.0` 需要 node >=24，而系统当前是 v22.x。这只是警告而非失败，但离静默运行时崩溃只差一个传递依赖。执行 `nvm install 24 && nvm use 24`（或 `mise use node@24`）。

2. **检查 Air 上的交换情况。** 如果 `ps` 显示 tsc 存活但运行缓慢，请检查 `vm_stat | grep -E 'Pageouts|swap'`。在安装了大量 npm 包且内存为 16 GB 的情况下，tsc 可能会发生颠簸。在运行 `hermes update` 之前关闭浏览器/Electron 应用确实有帮助。

如果 `tsc -b` 报错（而非挂起），旋转动画 UI 也可能掩盖非零退出状态——第 2 步中的手动 `npm run build` 会立即显示实际的 TypeScript 错误。如果 web 前端从未构建成功（例如 npm 不可用或 PATH 被缩减），文档中记录的手动降级方法是 `cd ~/.hermes/hermes-agent/web && npm install && npm run build`，然后重新启动——仪表盘会提供 `web_dist` 中存在的任何内容。生产构建输出到 `hermes_cli/web_dist/`，FastAPI 服务器将其作为静态 SPA 提供；`hermes update` 仅在 npm 可用时自动重建前端。

再多一个数据点：在关联的问题中，*真正的*挂起出现在后一步——“→ Building desktop packaged app...” 在 electron-builder 打包期间停滞。你的运行显示 `(desktop skipped)`，所以你避开了那个问题；你的问题只是 tsc 在静默运行。

**参考资料：**

- [Issue #38974 — 在 macOS 上执行 `hermes update` 时卡住](https://github.com/NousResearch/hermes-agent/issues/38974)
- [Hermes Agent 文档 — Web Dashboard 构建管道](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard)
- [手动构建 Web UI 的降级方案](https://hermes-agent.ai/how-to/use-hermes-web-ui)
