---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺失构建系统导致入口点损坏
translated: true
type: note
---

## 摘要

### 发生了什么

你将项目从 `timesheet` 重命名为 `tt`（包括目录和 `pyproject.toml` 中的 `name` 字段）。之后，`uv run tt` 失败并报错：

```
error: Failed to spawn: `tt`
  Caused by: No such file or directory (os error 2)
```

### 根本原因

`pyproject.toml` 缺少 `[build-system]` 声明。当 `uv sync` 在没有此声明的情况下运行时，会发出以下警告（很容易被忽略）：

```
warning: Skipping installation of entry points (`project.scripts`) for package `tt`
because this project is not packaged; to install entry points, set `tool.uv.package = true`
or define a `build-system`
```

没有构建系统时，`uv` 会安装依赖，但**永远不会注册 CLI 入口点**（`tt = "tt.cli:main"`）。因此 `tt` 命令在虚拟环境的 `bin/` 目录中根本不存在，shell 无法找到它。

### 修改内容

**`pyproject.toml`** — 两处修改：

1. 添加了构建系统（hatchling）：
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

2. 将旧的 setuptools 包发现配置替换为 hatch 的等价配置：
```toml
# 之前（setuptools — 未将 setuptools 设为 build-backend 时无效）
[tool.setuptools.packages.find]
include = ["tt*"]
exclude = ["data*", "input*"]

# 之后（hatchling）
[tool.hatch.build.targets.wheel]
packages = ["tt"]
```

然后 `uv sync` 重新构建了包并注册了入口点。

### 为什么之前可能工作正常

旧项目位于 `/Users/lzwjava/projects/timesheet`，可能有一个缓存的虚拟环境，当时 `uv sync` 或 `uv pip install -e .` 是在可安装模式下运行的，或者设置了 `tool.uv.package = true`。当你重命名/移动项目后，`uv sync` 从头重新解析，从而遇到了缺少构建系统的问题。

### 备选方案（如果需要）

除了添加 `[build-system]`，你还可以在 `pyproject.toml` 中添加以下内容：

```toml
[tool.uv]
package = true
```

这告诉 `uv` 将项目视为一个包，并安装入口点，即使没有正式的构建后端。但使用 `hatchling` 是更标准的方法。