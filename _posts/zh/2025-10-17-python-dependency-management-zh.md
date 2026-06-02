---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用Poetry管理Python依赖
translated: true
type: note
---

### 什么是 Poetry？

Poetry 是 Python 中用于依赖管理和打包的工具。它允许您声明项目所依赖的库，并自动处理安装、更新和解析这些库，同时确保环境可重现。

### 主要用途

Poetry 通过单一配置文件（`pyproject.toml`）管理依赖关系，创建锁定文件以确保在不同机器上安装的一致性，并支持构建项目以进行分发（例如发布到 PyPI），从而简化了 Python 项目的工作流程。它旨在用统一、用户友好的方法取代零散的工具，如 `pip`、`pipenv` 和 `setuptools`。

### 主要特性

- **依赖解析**：自动安装和更新依赖项，智能解决冲突。
- **锁定文件**：生成 `poetry.lock` 文件以固定确切版本，实现可重复构建。
- **虚拟环境**：为每个项目创建隔离环境，避免全局污染。
- **打包功能**：构建 wheel 或 sdist 格式以方便分发。
- **多平台支持**：支持 Linux、macOS 和 Windows。
- **Shell 集成**：为 Bash、Fish 和 Zsh 提供 Tab 自动补全。
- **兼容 Python 3.9+**：需要现代 Python 版本。

### 安装方法

推荐使用 `pipx` 在隔离环境中安装 Poetry（避免冲突且全局可用）：

1. 如需安装 `pipx`（可通过系统包管理器或 `python -m pip install --user pipx` 安装）。
2. 运行：`pipx install poetry`。

更新方法：`pipx upgrade poetry`。
卸载方法：`pipx uninstall poetry`。

启用 Shell 自动补全（例如 Bash：`poetry completions bash >> ~/.bash_completion`）。

### 基本用法

初始化新项目：`poetry init`。
添加依赖项：`poetry add requests`。
根据锁定文件安装：`poetry install`。
运行脚本：`poetry run python script.py`。
构建包：`poetry build`。

完整命令请查阅文档。

[Poetry 文档](https://python-poetry.org/docs/)
