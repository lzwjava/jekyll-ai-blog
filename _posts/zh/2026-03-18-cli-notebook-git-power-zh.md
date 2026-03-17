---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLI 笔记本：Git 强大功能
translated: true
type: note
---

**问题：** 提供对 https://github.com/xwmx/nb?tab=readme-ov-file#-revision-history 的全面介绍

**答案：**

`nb`（“notebook”的缩写）是一个强大、便携的 **command-line tool**（以及本地 web 界面），用于纯文本笔记记录、书签、归档和构建个人知识库。由 xwmx 开发，它是一个单一的 Bash 脚本，将一切存储在 Git 仓库中的普通纯文本文件（主要是 Markdown）中。这种设计使其轻量级、未来-proof、全文可搜索、有版本控制、可同步，并且独立于专有格式或云服务。

### 核心理念
- 使用标准格式（Markdown、Org 等）的纯文本文件存储数据
- Git 自动且透明地处理版本控制和同步
- 无数据库——只需普通目录和文件，可用任何工具管理
- 离线工作、本地优先，支持可选的远程 Git 同步（GitHub、GitLab、私有服务器等）
- 非常接近物理 Zettelkasten 系统的数字等价物

### 主要特性
- **Notes** — 创建、编辑、查看、删除带有标题、标签和内容的 Markdown 文件
- **Bookmarks** — 保存 URL 及其完整缓存内容、引述、评论、标签；支持全文搜索
- **Todos & Tasks** — 专用的 `.todo.md` 文件，支持复选框、到期日期、子任务和状态跟踪（`do` / `undo`）
- **Tagging** — `#hashtags`（包括嵌套的 `#parent/child`），强大的过滤功能
- **Linking** — Wiki 风格的 `[[notebook:folder/id|custom text]]` 内部链接，用于 Zettelkasten 风格的知识图谱
- **Pinning** — 将重要项目固定到列表顶部
- **Folders & Notebooks** — 分层组织；支持多个全局/本地 notebooks
- **Search** — 全文本搜索（支持 regex、AND/OR/NOT、标签/类型过滤），使用 `git grep`、`ripgrep` 或类似工具
- **Revision History** — 每个更改都是一个 Git commit；使用 `nb history` 查看（如果安装了则优先使用 `tig`）
- **Git Sync** — 自动 commit + push/pull 到远程；合理处理冲突
- **Encryption** — 每个项目使用 OpenSSL AES-256 或 GPG 进行密码保护
- **Browsing** — `nb browse` 启动本地 web 服务器，用于交互式浏览笔记（支持终端浏览器如 w3m 或 GUI 浏览器）
- **Import / Export** — 通过 Pandoc 支持多种格式的转换（HTML、DOCX、EPUB、PDF 等）
- **Images** — 支持内联图像、导入、终端查看
- **Plugins & Themes** — 可通过自定义子命令和颜色主题扩展
- **Interactive Shell** — `nb shell` 用于 REPL 风格的使用

### 版本历史如何工作
README 中的 **#-revision-history** 部分解释了基于 Git 的版本控制：

- 每个添加、编辑、移动、删除或其他修改都会在后台自动创建一个 Git commit。
- 使用 `nb history`（或 `nb history <selector>`）查看更改：
  - `nb history` — 当前 notebook
  - `nb history 42` — 特定 ID 的项目
  - `nb history example:7` — notebook “example” 中的项目 7
  - `nb history "My Note Title"` — 通过标题
- 显示 commit 日志（日期、消息、作者）；可用时使用 `tig` 进行交互式查看
- 作者名称/邮箱来自全局 Git 配置，或可通过 `nb notebooks author` 在每个 notebook 中覆盖
- 因为每个 notebook 都是独立的 Git 仓库，因此历史按 notebook 隔离

这为每个笔记、书签和 todo 提供了不可变的版本控制，类似于带有完整更改跟踪的轻量级个人 wiki。

### 安装（截至 2026 年）
- **Homebrew**（macOS/Linux）：`brew install xwmx/taps/nb`
- **npm**：`npm install -g nb.sh`
- **手动**（最便携）：  
  ```bash
  sudo wget https://raw.githubusercontent.com/xwmx/nb/master/nb -O /usr/local/bin/nb
  sudo chmod +x /usr/local/bin/nb
  nb completions install
  ```
- **更新**：`nb update`（非包管理器安装时使用）
- **必需**：Bash + Git
- **可选（强烈推荐）**：pandoc、ripgrep/rga、bat、tig、w3m/lynx、socat/ncat（用于 browse）

### 快速入门示例
```bash
# 创建一个笔记
nb add "Meeting notes 2026-03" --tags projectX meeting

# 添加一个书签
nb https://example.com/article --quote "Important insight" --tags research

# 创建一个 todo
nb todo add "Finish report" --due 2026-04-01 --task "Write summary" --task "Proofread"

# 搜索
nb q "quantum" --tag physics --type note

# 查看笔记历史
nb history 15

# 在浏览器中浏览
nb browse

# 同步一切
nb sync --all
```

### 优势与权衡
**优势**：
- 极度便携且长期可持续（纯文本 + Git）
- 强大的链接和搜索功能，适用于知识工作
- 零供应商锁定
- 活跃开发（2026 年 3 月最近 commit，版本 ~7.25.x）

**劣势 / 注意事项**：
- 需要熟悉终端和基本 Git
- 同步时的冲突解决需手动（Git 风格）
- 高级渲染（图像、复杂表格）依赖可选工具

总体而言，`nb` 是最成熟、功能丰富的 CLI 优先纯文本笔记本系统之一，特别是对于重视 Git、纯文本和 Zettelkasten 原则的用户。

**参考资料：**  

- [https://github.com/xwmx/nb](https://github.com/xwmx/nb)  
- [https://xwmx.github.io/nb/](https://xwmx.github.io/nb/)（演示 / 扩展文档）