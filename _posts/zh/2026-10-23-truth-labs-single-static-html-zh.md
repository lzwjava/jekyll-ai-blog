---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 真理实验室：单个静态HTML
translated: true
type: note
---

完成。**Truth Labs 现在是一个单一且自包含的 `index.html`** — 无需 Jekyll、无需 bundle、无需构建步骤。只需在浏览器中打开该文件，或将其放到任何静态托管上（GitHub Pages、Cloudflare、nginx、`python3 -m http.server`）。

## 文件内容

一个页面、一个内联 `<style>` 块，总计约 52 KB。所有部分均为页内锚点：

| 部分 | 内容 |
|---|---|
| **Hero** | “Truth through compute — nothing but truth” + 4 项统计条（52 GB VRAM、13 个模型、约 5B tokens、12 年） |
| **Focus areas** | 训练 · 推理与服务 · GPU 与硬件 · 咨询 |
| **Experiments** | 6 张公开工作卡（SEC-EDGAR-GPT、nanoGPT fork、52 GB 集群、MoE、zz、FluxReel） |
| **Manifesto** | 单人实验室语录 |
| **Research** | 完整实验室笔记：13 次训练表、硬件规格列表、SEC-EDGAR-GPT、nanoGPT fork、推理基准（nano-vLLM 506 tok/s、SGLang、llama.cpp、MoE）、M40/P100 集群 + BIOS 突破、token 使用量表 |
| **Services** | 4 条可雇佣服务 + 合作模式 + 可验证的参考 |
| **About** | 时间线 2008 → 2026、快速事实、论文、“为什么是单人实验室” |
| **Contact** | 电子邮件/GitHub/博客渠道 + 每种服务需要发送的内容 |

## 已验证

- 本地服务返回 `200`，0 个 Jekyll/liquid 语法残留
- 所有导航锚点（`#research`、`#services`、`#about`、`#contact` 等）都能解析到目标
- 没有未闭合/不匹配的 HTML 标签，没有损坏的内部链接
- 完全响应式 + 移动端导航处理

预览：
```bash
cd /Users/lzwjava/projects/truth-labs && python3 -m http.server 8080
```

该目录现在只有 `index.html`、`.gitignore`，没有其他文件——最简洁的静态站点。