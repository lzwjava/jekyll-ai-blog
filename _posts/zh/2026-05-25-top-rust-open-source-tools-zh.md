---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶级Rust开源工具
translated: true
type: note
---

**问题：** 有哪些类似 Zed 和 Warp 的优秀 Rust 开源工具/软件值得了解？

**回答：**

以下是按类别整理的精选列表——均为生产级质量、积极维护的 Rust 项目：

---

## 终端与 Shell

| 项目 | 简介 |
|---------|-----------|
| [Warp](https://github.com/warpdotdev/Warp) | AI 原生终端（你已提及） |
| [Alacritty](https://github.com/alacritty/alacritty) | GPU 加速终端，极简，速度极快 |
| [WezTerm](https://github.com/wez/wezterm) | GPU 加速终端 + 多路复用器，Lua 可配置 |
| [Zellij](https://github.com/zellij-org/zellij) | 终端多路复用器（tmux 替代品），支持插件系统 |

---

## 编辑器与 IDE

| 项目 | 简介 |
|---------|-----------|
| [Zed](https://github.com/zed-industries/zed) | 快速协作编辑器（你已提及） |
| [Helix](https://github.com/helix-editor/helix) | 模式编辑器，内置 tree-sitter + LSP，无需插件 |

---

## CLI 替代工具（“现代 Unix 工具”级别）

| 项目 | 替代品 | 备注 |
|---------|----------|-------|
| [ripgrep (rg)](https://github.com/BurntSushi/ripgrep) | `grep` | 最快的 grep，尊重 `.gitignore` |
| [fd](https://github.com/sharkdp/fd) | `find` | 语法更简单，速度快 |
| [bat](https://github.com/sharkdp/bat) | `cat` | 语法高亮，集成 git |
| [eza](https://github.com/eza-community/eza) | `ls` | 彩色输出，图标，树形视图 |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | `cd` | 更智能的目录跳转 |
| [dust](https://github.com/bootandy/dust) | `du` | 可视化磁盘使用情况 |
| [procs](https://github.com/dalance/procs) | `ps` | 更好的进程查看器 |
| [bottom (btm)](https://github.com/ClementTsang/bottom) | `htop` | 完整的 TUI 系统监控 |
| [sd](https://github.com/chmln/sd) | `sed` | 更合理的替换语法 |
| [hyperfine](https://github.com/sharkdp/hyperfine) | 手动计时 | 命令行基准测试工具 |

---

## 构建、包管理与开发工具

| 项目 | 简介 |
|---------|-----------|
| [just](https://github.com/casey/just) | `make` 替代品，语法更合理——非常适合项目脚本 |
| [cargo-watch](https://github.com/watchexec/watchexec) | 文件变动时重新运行 cargo |
| [mise](https://github.com/jdx/mise) | `asdf`/`nvm`/`pyenv` 多合一版本管理器 |
| [pixi](https://github.com/prefix-dev/pixi) | 兼容 Conda 的包管理器，速度快 |
| [uv](https://github.com/astral-sh/uv) | Python 包管理器——替代 `pip` + `venv`，快 100 倍 |
| [ruff](https://github.com/astral-sh/ruff) | Python 代码检查器 + 格式化器，替代 flake8/black/isort |

---

## 网络与 HTTP

| 项目 | 简介 |
|---------|-----------|
| [xh](https://github.com/ducaale/xh) | 类似 `httpie` 但速度更快——对用户最友好的 curl 替代品 |
| [dog](https://github.com/ogham/dog) | DNS 查询工具，替代 `dig` |
| [bandwhich](https://github.com/imsnif/bandwhich) | 按进程查看终端带宽使用情况 |
| [miniserve](https://github.com/svenstaro/miniserve) | 即时 HTTP 文件服务器，单个二进制文件 |

---

## 数据与搜索

| 项目 | 简介 |
|---------|-----------|
| [Meilisearch](https://github.com/meilisearch/meilisearch) | 全文搜索引擎，Elasticsearch 替代品 |
| [Tantivy](https://github.com/quickwit-oss/tantivy) | Rust 实现的 Lucene 等效搜索库 |
| [Quickwit](https://github.com/quickwit-oss/quickwit) | 用于日志/追踪的分布式搜索引擎 |
| [Lancedb](https://github.com/lancedb/lancedb) | 嵌入式向量数据库（与你的 AI 工作相关） |

---

## AI / LLM 相关

| 项目 | 简介 |
|---------|-----------|
| [Candle](https://github.com/huggingface/candle) | HuggingFace 的 Rust ML 框架——无需 Python 即可运行 LLM |
| [llm](https://github.com/rustformers/llm) | 在 CLI 中本地运行 GGML 模型 |
| [Ratchet](https://github.com/FL33TW00D/ratchet) | Rust 中的 WebGPU ML 推理 |

---

## 特别为你推荐

鉴于你从事 AI 工程且偏好 CLI 工作流：

1. **`uv` + `ruff`**——你可能已经在用了，但若没有，它们能立即提升 Python 工作流效率
2. **`mise`**——单一工具替代 pyenv/nvm/rbenv
3. **`just`**——替代 Makefile，非常适合代理/CLI 项目脚本
4. **Candle**——值得研究其源码；HF 押注 Rust 推理，与你模型训练工作直接相关
5. **Tantivy / Quickwit**——如果你曾构建带自定义检索的 RAG 管道
6. **Helix**——如果你想要一个从第一天起就原生集成 LSP 的模式编辑器，无需折腾 vimrc
