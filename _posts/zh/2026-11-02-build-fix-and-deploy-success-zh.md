---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建修复与部署成功
translated: true
type: note
---

构建已触发并成功部署。✅

**发生了什么：**

1. 我触发了 workflow，并发现**之前的构建已失败**——CI 的“Verify generated files are committed”步骤检测到 `portfolio.html` 与其生成器不同步。

2. **根本原因：** `scripts/build_cases.py` 从内部模板生成 `portfolio.html`（以及 `cases/*.html`）。我之前手动编辑 favicon 导致已提交的 `portfolio.html` 与生成器产出的内容不同——而生成器模板仍然使用旧的 emoji favicon。

3. **修复：** 更新了 `scripts/build_cases.py` 中的两个模板，使其输出新的 DeepCompute favicon 链接（`favicon.ico`、`deepcompute-icon.png`、`apple-touch-icon.png`），并使用正确的相对路径（portfolio 使用 `logo/…`，case 页面使用 `../logo/…`），然后重新生成了所有页面。

4. **已提交并推送**——由推送触发的运行已端到端通过：

   - ✓ **Build (regenerate static pages)** — 8s
   - ✓ **Deploy to Cloudflare Pages** — 30s

站点（带有 DeepCompute logo、philosophy band 以及所有重新生成的 case 页面）现已上线。之前的两次失败都只是同一个过时的验证检查，现已解决。
