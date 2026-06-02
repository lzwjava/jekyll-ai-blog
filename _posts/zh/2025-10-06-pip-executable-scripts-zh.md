---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 为Pip包添加可执行脚本
translated: true
type: note
---

### 在 Python Pip 包中创建可执行脚本

若要在通过 `pip` 安装的 Python 包中包含可执行脚本（即命令行工具），您需要在包的配置文件中定义 **入口点**。这使得用户在安装后可以直接运行您的脚本（例如在终端中输入 `my-script`）。

我们将使用一个简单示例：名为 `mytools` 的包，其中包含一个用于打印问候语的 `greet` 脚本。

#### 步骤 1：设置包结构
创建如下目录结构：

```
mytools/
├── pyproject.toml          # 现代配置文件（推荐替代 setup.py）
├── README.md
└── src/
    └── mytools/
        ├── __init__.py     # 使其成为包
        └── greet.py        # 脚本逻辑
```

在 `src/mytools/__init__.py` 中（可为空或包含版本信息）：
```python
__version__ = "0.1.0"
```

在 `src/mytools/greet.py` 中（脚本将调用的函数）：
```python
import sys

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

#### 步骤 2：在 `pyproject.toml` 中配置入口点
使用 `[project.scripts]` 部分定义控制台脚本。这会指示 pip 创建可执行包装器。

```toml
[build-system]
requires = ["hatchling"]  # 或 "setuptools", "flit" 等
build-backend = "hatchling.build"

[project]
name = "mytools"
version = "0.1.0"
description = "一个简单的工具包"
readme = "README.md"
requires-python = ">=3.8"
dependencies = []  # 在此添加依赖项，例如 "requests"

[project.scripts]
greet = "mytools.greet:main"  # 格式：脚本名称 = 包.模块:函数
```

- `greet` 是用户将运行的命令（例如 `greet Alice`）
- `mytools.greet:main` 指向 `greet.py` 中的 `main()` 函数

如果您偏好使用较旧的 `setup.py`（仍可使用但不推荐）：
```python
from setuptools import setup, find_packages

setup(
    name="mytools",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "greet = mytools.greet:main"
        ]
    },
    # ... 其他字段如 description, install_requires
)
```

#### 步骤 3：构建和安装包
1. 安装构建工具：`pip install build twine`（如果使用 hatchling 后端则安装 `hatchling`）

2. 构建包：
   ```
   python -m build
   ```
   这将在 `dist/` 目录中创建 `.tar.gz` 和 `.whl` 文件

3. 本地安装测试：
   ```
   pip install -e .  # 可编辑模式（更改立即生效）
   ```
   或进行干净安装：`pip install dist/mytools-0.1.0-py3-none-any.whl`

4. 测试：在终端中运行 `greet Alice`，应输出 "Hello, Alice!"

#### 步骤 4：分发（可选）
- 上传到 PyPI：`twine upload dist/*`（需要 PyPI 账户）
- 用户随后可通过 `pip install mytools` 安装并运行 `greet`

#### 提示
- **多个脚本**：在 `[project.scripts]` 中添加更多行，例如 `another-script = mytools.other:main`
- **参数处理**：在 `main()` 中使用 `argparse` 以获得更好的 CLI 处理
- **依赖项**：在 `[project.dependencies]` 中列出（例如 CLI 框架 `click`）
- **虚拟环境**：始终使用虚拟环境（`python -m venv env; source env/bin/activate`）以避免冲突
- **遇到错误？** 使用 `pip install --verbose` 查看详细信息，确保函数不接受参数（或正确处理 `sys.argv`）

有关更高级的设置（例如使用 Poetry 或 Flit），请查阅官方文档。

#### 参考文档
- [Python 打包用户指南：入口点](https://packaging.python.org/en/latest/guides/writing-entry-points/)
- [PyPI：构建与发布](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
