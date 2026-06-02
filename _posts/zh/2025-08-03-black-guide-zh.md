---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 黑色：Python代码格式化工具指南
translated: true
type: note
---

Black 是由 Python 软件基金会（PSF）开发的一款固执己见、毫不妥协的 Python 代码格式化工具。它能自动将 Python 代码重新格式化为一致的风格，主要基于 PEP 8 的严格子集，同时强调可读性、一致性以及在版本控制中保持最小的差异。通过使用 Black，开发者同意放弃对次要格式细节的控制，以换取代码审查期间的速度、确定性和减少关于风格的争论。Black 确保格式化后的代码在项目中看起来统一，从而为开发中更关键的方面节省时间和精力。它支持 Python 3.8 及更高版本，最新的稳定版本是 25.1.0（于 2025 年 1 月 29 日发布），该版本引入了 2025 稳定风格，包含诸如规范化的 Unicode 转义字符大小写和改进尾随逗号处理等增强功能。

Black 的哲学优先考虑：

- **一致性**：相似的构造会被格式化为相同的形式。
- **通用性**：规则广泛适用，没有特殊情况。
- **可读性**：专注于易于阅读的代码。
- **差异最小化**：减少 Git 差异中的变更，以加速审查。

由于其可靠性和集成能力，它被广泛用于开源和专业项目中。

## 安装

Black 可在 PyPI 上获取，可以使用 pip 安装。建议在虚拟环境中安装以实现项目隔离。

- 基本安装：

  ```
  pip install black
  ```

- 如需额外功能，如 Jupyter Notebook 支持或彩色差异显示：

  ```
  pip install 'black[jupyter,colorama]'
  ```

  （`d` 额外项用于 blackd，一个用于编辑器集成的守护进程。）

在 Arch Linux 上，您可以通过包管理器安装：`pacman -S python-black`。

Black 也可以通过 conda 或其他包管理器安装。安装后，使用 `black --version` 进行验证。

对于开发或测试，您可以克隆 GitHub 仓库并以可编辑模式安装：

```
git clone https://github.com/psf/black.git
cd black
pip install -e .
```

## 用法

Black 主要是一个命令行工具。基本命令会原地格式化文件或目录：

```
black {源文件或目录}
```

如果以脚本方式运行 Black 不工作（例如，由于环境问题），请使用：

```
python -m black {源文件或目录}
```

### 主要命令行选项

Black 提供了各种标志用于自定义和控制。以下是主要选项的摘要：

- `-h, --help`：显示帮助信息并退出。
- `-c, --code <代码>`：格式化一串代码（例如，`black --code "print ( 'hello, world' )"` 输出格式化后的版本）。
- `-l, --line-length <整数>`：设置行长度（默认值：88）。
- `-t, --target-version <版本>`：指定 Python 版本以保持兼容性（例如，`py38`，可以指定多个，如 `-t py311 -t py312`）。
- `--pyi`：将文件视为类型存根（`.pyi` 风格）。
- `--ipynb`：将文件视为 Jupyter Notebooks。
- `--python-cell-magics <magic>`：识别自定义的 Jupyter magics。
- `-x, --skip-source-first-line`：跳过格式化第一行（适用于 shebangs）。
- `-S, --skip-string-normalization`：不将字符串规范化为双引号或特定前缀。
- `-C, --skip-magic-trailing-comma`：忽略尾随逗号以进行换行。
- `--preview`：启用下一个版本的实验性样式更改。
- `--unstable`：启用所有预览更改以及不稳定功能（需要 `--preview`）。
- `--enable-unstable-feature <功能>`：启用特定的不稳定功能。
- `--check`：检查文件是否需要重新格式化而不更改它们（如果需要更改，则退出码为 1）。
- `--diff`：显示更改的差异而不写入文件。
- `--color / --no-color`：对差异输出进行着色。
- `--line-ranges <范围>`：格式化特定的行范围（例如，`--line-ranges=1-10`）。
- `--fast / --safe`：跳过（`--fast`）或强制执行（`--safe`）AST 安全检查（默认：safe）。
- `--required-version <版本>`：要求特定的 Black 版本。
- `--exclude <正则表达式>`：通过正则表达式排除文件/目录。
- `--extend-exclude <正则表达式>`：添加到默认排除项。
- `--force-exclude <正则表达式>`：即使显式传递也排除。
- `--include <正则表达式>`：通过正则表达式包含文件/目录。
- `-W, --workers <整数>`：设置并行工作进程数（默认值：CPU 数量）。
- `-q, --quiet`：抑制非错误消息。
- `-v, --verbose`：显示详细输出。
- `--version`：显示 Black 版本。
- `--config <文件>`：从文件加载配置。

### 示例

- 格式化单个文件：`black example.py`
- 检查而不格式化：`black --check .`
- 显示差异：`black --diff example.py`
- 格式化标准输入：`echo "print('hello')" | black -`
- 使用自定义行长度格式化：`black -l 79 example.py`
- 格式化 Jupyter Notebook：`black notebook.ipynb`

### 提示和注意事项

- Black 格式化整个文件；使用 `# fmt: off` / `# fmt: on` 来跳过代码块，或使用 `# fmt: skip` 跳过单行。
- 对于标准输入，使用 `--stdin-filename` 以尊重排除规则。
- Black 是确定性的：相同的输入总是产生相同的输出。
- 使用 `--preview` 来测试即将到来的样式，但请注意它们可能会更改。

## 配置

Black 可以通过命令行标志或 `pyproject.toml` 文件（项目首选）进行配置。在 `pyproject.toml` 中的配置放在 `[tool.black]` 部分下。

### 使用 pyproject.toml

示例：

```
[tool.black]
line-length = 79
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
skip-string-normalization = true
```

支持的选项与 CLI 标志相对应（例如，`line-length`，`skip-string-normalization`）。多值选项如 `target-version` 使用数组。

### 优先级

- 命令行标志覆盖配置文件设置。
- 如果未找到 `pyproject.toml`，Black 使用默认值并搜索父目录。
- 使用 `--config` 指定自定义配置文件。

### 文件发现与忽略

Black 自动发现目录中的 Python 文件，默认情况下遵循 `.gitignore`。使用 `--include`/`--exclude` 来自定义。它会忽略常见目录，如 `.git`、`.venv` 等，除非被覆盖。

对于版本控制，可以与 pre-commit 等工具集成以强制执行格式化。

## Black 代码风格

Black 强制执行一种特定的风格，配置选项有限。关键规则：

### 行长度

- 默认值：88 个字符。如果无法断开（例如，长字符串），可能会超出。

### 字符串

- 首选双引号；将前缀规范化为小写（例如，`r` 在 `f` 之前）。
- 将转义序列转换为小写（除了 `\N` 名称）。
- 处理文档字符串：修复缩进，移除多余的空白/换行，在文本中保留制表符。

### 数字字面量

- 语法部分小写（例如，`0xAB`），数字大写。

### 换行与运算符

- 在二元运算符之前换行。
- 大多数运算符周围使用单个空格；对于一元运算符或幂运算符且操作数简单时无空格。

### 尾随逗号

- 添加到多行集合/函数参数中（如果使用 Python 3.6+）。
- "魔法"尾随逗号：如果存在，则会将列表展开。

### 注释

- 内联注释前两个空格；文本前一个空格。
- 保留 shebangs、文档注释等的特殊间距。

### 缩进

- 4 个空格；与缩进减少的闭括号匹配。

### 空行

- 最小化空白：函数内单个空行，模块级别双空行。
- 文档字符串、类和函数的特定规则。

### 导入

- 拆分长导入；与 isort 的 `black` 配置文件兼容。

### 其他规则

- 优先使用括号而非反斜杠。
- 基于文件规范化行结尾。
- `.pyi` 文件使用简洁风格（例如，方法之间没有额外的空行）。
- 在预览模式下，折叠导入后的空行。

Black 旨在减少差异并提高可读性，更改主要是为了错误修复或新语法支持。

## 集成

Black 与编辑器和版本控制系统无缝集成，实现自动化格式化。

### 编辑器

- **VS Code**：使用 Python 扩展并将 Black 设置为格式化程序。在 settings.json 中设置 `"python.formatting.provider": "black"`。对于 LSP，安装 python-lsp-server 和 python-lsp-black。
- **PyCharm/IntelliJ**：
  - 内置（2023.2+）：设置 > 工具 > Black，配置路径。
  - 外部工具：设置 > 工具 > 外部工具，添加 Black，参数为 `$FilePath$`。
  - 文件监视器：用于保存时自动格式化。
  - BlackConnect 插件用于基于守护进程的格式化。
- **Vim**：使用官方插件（通过 vim-plug：`Plug 'psf/black', { 'branch': 'stable' }`）。命令：`:Black` 进行格式化。自动保存：将 autocmd 添加到 vimrc。配置变量如 `g:black_linelength`。
- **Emacs**：使用 reformatter.el 或 python-black 包进行保存时格式化。
- **其他**：通过插件或扩展支持 Sublime Text、JupyterLab、Spyder 等。

### 版本控制

- **Pre-commit Hooks**：添加到 `.pre-commit-config.yaml`：

  ```
  repos:
    - repo: https://github.com/psf/black-pre-commit-mirror
      rev: 25.1.0
      hooks:
        - id: black
          language_version: python3.11
  ```

  对于 Jupyter：使用 `id: black-jupyter`。
- **GitHub Actions**：在工作流中使用诸如 `psf/black-action` 之类的 actions 进行 CI 检查。
- **Git**：在 pre-commit 脚本或 husky 中运行 Black 以强制执行。

## 高级主题

- **预览和不稳定样式**：使用 `--preview` 获取未来的更改（例如，更好的括号拥抱）。`--unstable` 用于实验性功能。
- **Blackd**：用于集成的 HTTP 服务器（`blackd --bind-host 127.0.0.1 --bind-port 45484`）。
- **Jupyter 支持**：格式化 Notebook，保留 magics。
- **类型存根**：对 `.pyi` 文件使用特殊的简洁格式化。
- **兼容性**：目标为 Python 3.8+；对旧代码使用 `--target-version`。
- **替代方案**：与 autopep8（更灵活但不太固执己见）或 Ruff（更快，包含 linting）进行比较。

对于故障排除，请查阅官方文档或 GitHub issues 上的 FAQ。

## 参考资料

- [Black 25.1.0 文档](https://black.readthedocs.io/en/stable/)
- [psf/black GitHub 仓库](https://github.com/psf/black)
- [Black 代码风格](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
- [用法与配置](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
- [编辑器集成](https://black.readthedocs.io/en/stable/integrations/editors.html)
- [版本控制集成](https://black.readthedocs.io/en/stable/integrations/source_version_control.html)
- [使用 Black 进行 Python 代码格式化 - GeeksforGeeks](https://www.geeksforgeeks.org/python/python-code-formatting-using-black/)
- [如何使用 Black 自动格式化 Python 代码 - freeCodeCamp](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/)
- [Black - PyPI](https://pypi.org/project/black/)
- [Python Black 模块介绍 - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-to-python-black-module/)
- [Python 自动格式化工具：Autopep8 vs. Black - Built In](https://builtin.com/data-science/autopep8-vs-black)
