---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 黑色Python代码格式化工具指南
translated: true
type: note
---

PyPI 上的 `black` 包是一个 **Python 代码格式化工具**。它能自动将你的 Python 代码重新格式化为统一的风格规范（兼容 PEP 8，但具有更严格的规则）。以下是使用方法：

---

### 1. 安装 Black

```bash
pip install black
```

如需确保始终安装最新稳定版本：

```bash
pip install -U black
```

---

### 2. 格式化文件或目录

对单个文件运行 Black：

```bash
black my_script.py
```

对整个目录进行递归格式化：

```bash
black src/
```

默认情况下，它会直接覆盖原文件并生成格式化后的代码。

---

### 3. 检查格式而不修改

使用 `--check` 参数检查文件是否需要重新格式化：

```bash
black --check my_script.py
```

这在 CI 流水线中非常实用，可确保代码风格统一。

---

### 4. 常用选项

* `--line-length 88` → 调整行长度（默认值：88）
* `--diff` → 显示变更内容但不修改文件
* `--skip-string-normalization` → 保留字符串引号不变
* `--exclude` → 跳过指定文件/文件夹

示例：

```bash
black --line-length 100 --diff src/
```

---

### 5. 集成应用

* **IDE 支持**：Black 可作为插件在 PyCharm、VS Code、Vim、Emacs 等编辑器中使用
* **预提交钩子**：在 `.pre-commit-config.yaml` 中添加配置，实现提交前自动格式化：

  ```yaml
  repos:
    - repo: https://github.com/psf/black
      rev: stable
      hooks:
        - id: black
  ```

* **CI/CD**：在持续集成流程中加入 `black --check .` 命令

---

👉 需要我继续演示如何在 **VSCode 或 PyCharm 中配置自动格式化** 来避免手动运行 `black` 吗？
