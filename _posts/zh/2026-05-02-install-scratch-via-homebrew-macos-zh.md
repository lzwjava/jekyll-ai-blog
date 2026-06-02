---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上通过Homebrew安装Scratch
translated: true
type: note
---

以下是我具体执行的操作：

**1. 预检阶段 —— Homebrew 是否可用？**
```bash
which brew && brew --version
```
在 `/opt/homebrew/bin/brew` 找到 Homebrew 5.1.1。

**2. 检查 Scratch 是否已安装**
```bash
brew list --cask | grep -i scratch
ls /Applications/ | grep -i scratch
```
两条命令均无返回结果 —— 属于全新安装环境。

**3. 通过 Homebrew Cask 安装**
```bash
brew install --cask scratch
```
Homebrew 下载了 Scratch 3.31.1 并将 `Scratch 3.app` 移至 `/Applications/`。

**4. 安装验证**
```bash
ls /Applications/ | grep -i scratch
```
确认 `/Applications/Scratch 3.app` 存在。

---

**为何选择 Homebrew Cask？**
在 macOS 中，`brew install --cask` 是安装 GUI 应用程序的标准方式 —— 它能自动处理下载、`.dmg` 挂载以及移动至 `/Applications` 目录的完整流程。无需使用 flatpak，也无需手动下载。虽然也可从 `scratch.mit.edu/download` 手动下载 `.dmg` 文件安装，但 Homebrew 方案更为简洁，且便于后续更新（通过 `brew upgrade --cask scratch`）。
