---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: GitHub Actions 矩阵构建指南
translated: true
type: note
---

听起来您是在询问如何使用 **GitHub Actions 矩阵构建**来并行运行测试，以及如何在矩阵策略中使用 `fail-fast` 选项。我来为您详细解释一下。

---

### GitHub Actions 中的矩阵构建

**矩阵策略**允许您使用不同参数并行运行相同任务——例如跨多个 Python 或 Node 版本进行测试，或在不同操作系统上进行测试。

一个最小化示例：

{% raw %}

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
        os: [ubuntu-latest, windows-latest]
      fail-fast: false
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

{% endraw %}

---

### 关键要点

- **`matrix`:** 定义用于创建任务组合的变量。
  上述示例会运行所有（`python-version`，`os`）组合的测试。

- **并行执行:** 矩阵生成的每个任务默认**并行运行**。

- **`fail-fast`:**
  - 默认值为 `true`。这意味着如果一个任务失败，其余矩阵任务将被取消。
  - 如果您希望所有矩阵任务继续运行（即使其中一个失败），请设置 `fail-fast: false`。

  示例：

  ```yaml
  strategy:
    matrix:
      node: [14, 16, 18]
    fail-fast: false
  ```

- **限制总任务数:** 您可以排除某些组合：

  ```yaml
  strategy:
    matrix:
      python-version: [3.8, 3.9, 3.10]
      os: [ubuntu-latest, windows-latest]
    exclude:
      - python-version: 3.8
        os: windows-latest
  ```

---

### 并行运行测试

- 每个**矩阵任务都在独立的运行器上并行运行**，因此您无需特殊处理。
- 在每个任务内部，如果您想要**并行测试执行**（例如 pytest 的 `-n auto`），可以在测试命令级别添加。

示例：

```yaml
- name: Run pytest in parallel
  run: pytest -n auto
```

---

✅ **总结:**

- 使用 `strategy.matrix` 定义不同的参数组合。
- 如果您希望所有矩阵任务即使有一个失败也能继续运行，请设置 `fail-fast: false`。
- 矩阵任务会自动并行运行。
- 为了加快每个任务内的运行速度，请使用测试框架的并行化功能（例如 pytest-xdist）。

---

需要我为您展示一个**运行 Node/JavaScript 测试**的真实矩阵示例吗（包含多个 Node 版本、`fail-fast: false` 设置，以及使用 `npm test` 进行并行测试）？
