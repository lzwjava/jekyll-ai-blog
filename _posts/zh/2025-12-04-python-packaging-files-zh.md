---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Python打包文件详解
translated: true
type: note
---

问题：Python 中的 MANIFEST.in 和 setup.py 是什么，它们如何工作？

答案：

在 Python 中，当创建可分发包（例如，上传到 PyPI 或共享代码）时，通常会使用基于较旧的 **setup.py** 的打包系统（仍然广泛使用，尽管正在向 pyproject.toml 发展）的两个重要文件：

### 1. **setup.py**

- **目的**：这是你的 Python 包的构建脚本。它告诉 Python 的打包工具（如 `setuptools`）如何安装、构建或分发你的项目。
- **工作原理**：你运行如下命令：

  ```bash
  python setup.py sdist    # 创建一个源代码分发包 (tar.gz)
  python setup.py bdist_wheel  # 创建一个 wheel (.whl)
  python setup.py install   # 在本地安装包
  ```

- **常见内容**（示例）：

  ```python
  from setuptools import setup, find_packages

  setup(
      name="my-awesome-package",
      version="1.0.0",
      author="Your Name",
      author_email="you@example.com",
      description="A short description",
      packages=find_packages(),  # 自动查找包含 __init__.py 的包
      install_requires=[
          "requests>=2.25",
          "numpy",
      ],
      python_requires=">=3.8",
      entry_points={
          "console_scripts": [
              "mycommand=my_package.cli:main",
          ]
      },
  )
  ```

- 构建或安装包时，此文件作为一个 Python 脚本执行。

### 2. **MANIFEST.in**

- **目的**：控制在 `setup.py sdist` 创建的源代码分发包 (`sdist`) 中包含哪些**额外文件**（非 Python 代码）。
- 默认情况下，`setuptools` 会包含：
  - 所有 `.py` 文件
  - `setup.py`、`pyproject.toml` 等。
- 但它**不会自动包含**诸如：
  - README.md、LICENSE、数据文件、模板、文档、测试等。
- **MANIFEST.in** 解决了这个问题。

- **工作原理**：它是一个简单的文本文件，包含声明性命令（每行一个）。

- **常见示例** (`MANIFEST.in`)：

  ```text
  include README.md
  include LICENSE
  include requirements.txt
  recursive-include src *.txt *.json
  recursive-include docs *
  include tests/*
  graft data_files          # 包含整个目录
  global-exclude *.pyc      # 排除所有 .pyc 文件
  global-exclude __pycache__
  ```

- 当你运行 `python setup.py sdist` 时，`setuptools` 会：
  1. 读取 `MANIFEST.in`
  2. 生成一个 `MANIFEST` 文件，列出所有要包含的文件
  3. 创建包含这些文件的 `.tar.gz`

### 它们如何协同工作的总结

| 步骤 | 使用文件 | 结果 |
| ----------------------------- | ------------------- | -------- |
| 定义包元数据和依赖项 | `setup.py` | 安装/构建必需 |
| 指定要包含在源代码 tarball 中的非 Python 文件 | `MANIFEST.in` | 仅影响 `sdist`（源代码分发） |
| 构建源代码分发包 | `python setup.py sdist` | 同时使用这两个文件 |

### 现代替代方案（2020 年后推荐）

使用 `pyproject.toml` + `setuptools` 声明性配置，而不是 `setup.py` 和 `MANIFEST.in`：

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
# ... metadata ...

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"my_package" = ["*.txt", "data/*.json"]
```

这完全避免了 `MANIFEST.in`，使打包更清晰。

**简而言之**：

- `setup.py` → 包的大脑（元数据、依赖项、构建逻辑）
- `MANIFEST.in` → 源代码分发中额外文件的打包清单

这两个在旧项目中仍然很常见，但新项目应优先选择 `pyproject.toml`。
