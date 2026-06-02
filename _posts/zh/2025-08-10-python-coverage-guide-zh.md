---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python覆盖率指南核心要点
translated: true
type: note
---

这是一份实用且面向开发者的 **coverage**（coverage.py）工具包入门指南——涵盖其测量内容、最佳使用方式以及你真正需要关注的核心配置。

# coverage.py 是什么

* 一款用于**测量测试或任何代码执行过程中运行到的代码行和分支**的 Python 工具
* 可生成**文本、HTML、XML 和 JSON** 格式报告，便于发现测试盲点并集成到 CI 质量门禁
* 兼容 unittest、pytest、nose 或普通脚本

# 核心概念（通俗解释）

* **行覆盖**：某行代码是否至少执行过一次？
* **分支覆盖**：决策点的每个可能分支是否都执行过？（if/else、布尔短路、异常、推导式等）
* **源码选择**：仅测量自身代码，避免虚拟环境/site-packages 的干扰
* **数据存储**：运行会生成 `.coverage`（SQLite）数据文件，支持多轮运行数据合并
* **上下文**：为执行过程添加标签（例如按测试用例），支持按测试名称、命令等维度查看报告

# 快速开始

```bash
# 1) 安装
pip install coverage

# 2) 在覆盖率监控下运行测试（以 pytest 为例）
coverage run -m pytest

# 3) 查看终端报告（含未覆盖行号）
coverage report -m

# 4) 生成 HTML 报告（在浏览器中打开 htmlcov/index.html）
coverage html

# 可选：生成机器可读报告
coverage xml        # 适用于 Sonar、Jenkins、Azure DevOps 等 CI 工具
coverage json       # 用于脚本分析
```

# 推荐的 .coveragerc 配置

在代码库根目录创建配置文件，确保本地与 CI 环境结果一致。

```ini
[run]
# 仅测量指定代码包避免干扰
source = src, your_package
branch = True
parallel = True                 # 允许多进程/多轮运行写入独立数据
relative_files = True           # 报告中的路径更清晰（兼容 CI）
concurrency = thread, multiprocessing

# 可完全排除某些文件或模式
omit =
    */tests/*
    */.venv/*
    */site-packages/*
    */migrations/*

[report]
show_missing = True
skip_covered = False            # 设为 True 可生成更简洁的报告
fail_under = 90                 # 覆盖率低于 90% 时使 CI 失败
exclude_lines =
    pragma: no cover            # 忽略代码行的标准指令
    if TYPE_CHECKING:
    raise NotImplementedError

[html]
directory = htmlcov
title = Coverage Report

[xml]
output = coverage.xml

[json]
output = coverage.json

[paths]
# 合并不同机器/容器数据时特别有用
source =
    src
    */workspace/src
    */checkouts/your_repo/src
```

# 测量子进程与并行运行

若代码涉及子进程（多进程、CLI 工具），需设置**子进程覆盖率**：

1. 在 `[run]` 中保持 `parallel = True`
2. 设置环境变量使子进程自动加载相同配置：

```bash
export COVERAGE_PROCESS_START=$(pwd)/.coveragerc
```

3. 正常运行程序/测试（或仍通过 `coverage run -m ...`）
4. 所有运行结束后合并数据并生成报告：

```bash
coverage combine
coverage report -m
```

> 提示：`concurrency = multiprocessing, thread, gevent, eventlet, greenlet` 可让 coverage 适配不同异步模型

# 分支覆盖与编译指示

* 在 `[run]` 中启用 `branch = True`，可捕获遗漏的 `else` 分支、短路逻辑、异常路径等
* 通过行尾注释忽略不可测试代码：
  * `# pragma: no cover` — 将该行排除在覆盖率外
  * 对于复杂分支，应优先考虑重构而非过度使用编译指示

# 上下文（按测试或任务切片）

上下文功能为执行代码添加标签，可解答“哪些测试覆盖了这段代码？”

* 最简单的 pytest 集成方式：
  * 在 `.coveragerc` 中添加 `dynamic_context = test_function`
  * 通过 `coverage html --show-contexts` 或检查上下文数据查看具体测试覆盖情况
* 也可设置 `dynamic_context = test`（测试节点ID）或通过环境变量在自定义运行器中设置 `dynacontext`

# Pytest 集成

两种常用模式：

**A. 原生 coverage CLI（简单高效）**

```bash
coverage run -m pytest -q
coverage report -m
```

**B. pytest-cov 插件（增强 CLI 体验）**

```bash
pip install pytest-cov
pytest --cov=your_package --cov-branch --cov-report=term-missing --cov-report=html
```

两种方式底层均使用 coverage.py，根据团队习惯选择即可

# 典型 CI 集成示例（GitHub Actions 提纲）

```yaml
- name: Install
  run: pip install -U pip coverage pytest

- name: Test with coverage
  run: |
    coverage run -m pytest -q
    coverage report -m
    coverage xml
- name: Enforce threshold
  run: coverage report --fail-under=90
- name: Upload HTML
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: htmlcov
    path: htmlcov/
```

# 常见问题与解决方案

* **报告过大/过慢**：限制 `source=` 范围并使用 `omit=` 排除虚拟环境、测试代码、生成代码
* **CI 与本地路径差异**：配置 `[paths]` 章节使 `coverage combine` 能正确合并数据集
* **子进程未测量**：设置 `COVERAGE_PROCESS_START` 并保持 `parallel = True`，最后执行 `coverage combine`
* **异步框架**：在 `concurrency = ...` 中添加对应条目
* **C 扩展**：coverage.py 仅测量 Python 代码而非原生代码——应在 Python 边界编写框架测试
* **不可达代码误报**：使用 `# pragma: no cover` 标记，但建议通过重构使行为可测试

# 实际常用命令

```bash
coverage erase                       # 清理历史数据
coverage run -m pytest               # 收集数据
coverage report -m                   # 带未覆盖行号的文本摘要
coverage html                        # 生成 HTML 报告
coverage xml                         # CI 解析格式
coverage json                        # 脚本/自动化处理格式
coverage combine                     # 合并并行/子进程数据
coverage annotate                    # 生成带执行标记的源码文件
```

# 何时停止调优

设定**有意义的阈值**（如 80-95%），通过 `fail_under` 强制执行，并聚焦于**差异覆盖率**审查（新增/修改的代码是否被测试？）。不要强求难以测试的代码（功能开关、防御性检查）达到 100%——谨慎使用编译指示，优先采用更简洁可测试的设计。

如果需要，我可以提供一个包含即用型 `.coveragerc`、pytest 配置和失败阈值检查的最小示例项目结构，方便你直接接入现有项目。
