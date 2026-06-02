---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Requests Setup.py 文件解析
translated: true
type: note
---

### 概述
这是一个 `setup.py` 文件，它是与 `setuptools` 配合使用的标准 Python 脚本，用于定义和构建 Python 包。具体来说，这个文件是为 **Requests** 库准备的——这是一个流行的 Python HTTP 客户端。它处理诸如包名称、版本、依赖项和分类器（用于 PyPI 分发）等元数据。当你运行 `pip install requests` 时，这个脚本（或其构建产物）会在后台执行以安装该包。

该脚本结构上是一个单独的 `setup()` 函数调用，但它包含了一些防护措施、辅助功能以及从其他文件动态读取的内容。我将逐节进行解析。

### 1. 导入和 Python 版本检查
```python
#!/usr/bin/env python
import os
import sys
from codecs import open

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    # 错误消息并退出
    sys.exit(1)
```
- **Shebang (`#!/usr/bin/env python`)**：使文件在类 Unix 系统上可执行，使用系统的 Python 解释器运行。
- **导入**：引入 `os` 和 `sys` 用于系统交互，`codecs.open` 用于 UTF-8 文件读取（安全处理非 ASCII 字符），以及从 `setuptools` 导入 `setup` 用于构建包。
- **版本检查**：确保用户运行的是 Python 3.9 或更高版本。如果不是，它会打印一条有用的错误消息，建议升级或固定到旧版本的 Requests（<2.32.0），然后以代码 1（失败）退出。这强制执行了兼容性，因为 Requests 放弃了对旧版本 Python 的支持。

### 2. 发布快捷方式
```python
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()
```
- 为维护者提供的便利：如果你运行 `python setup.py publish`，它会：
  - 在 `dist/` 文件夹中构建源码分发版（`sdist`）和 wheel 包（`bdist_wheel`）。
  - 使用 `twine`（一个安全的上传工具）将它们上传到 PyPI。
- 这是一种无需手动命令即可发布新版本的快速方法。运行后退出。

### 3. 依赖项
```python
requires = [
    "charset_normalizer>=2,<4",
    "idna>=2.5,<4",
    "urllib3>=1.21.1,<3",
    "certifi>=2017.4.17",
]
test_requirements = [
    "pytest-httpbin==2.1.0",
    "pytest-cov",
    "pytest-mock",
    "pytest-xdist",
    "PySocks>=1.5.6, !=1.5.7",
    "pytest>=3",
]
```
- **`requires`**：当你运行 `pip install requests` 时安装的核心依赖项。这些依赖项处理编码（`charset_normalizer`）、国际化域名（`idna`）、HTTP 传输（`urllib3`）和 SSL 证书（`certifi`）。
- **`test_requirements`**：仅在运行测试时安装（例如，通过 `pip install -e '.[tests]'`）。包括测试工具，如用于 HTTP 模拟、覆盖率测试和并行测试的 `pytest` 变体。`PySocks` 用于测试中的 SOCKS 代理支持。

### 4. 动态元数据加载
```python
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "src", "requests", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()
```
- **`about` 字典**：使用 `exec()` 从 `src/requests/__version__.py` 读取元数据（例如 `__title__`、`__version__`、`__description__` 等）。这使得版本信息集中管理——只需更新一次，`setup.py` 就会自动拉取。
- **`readme`**：将整个 `README.md` 文件作为字符串加载，用作 PyPI 上包的详细描述。

### 5. 主要的 `setup()` 调用
这是文件的核心。它配置包以进行构建/安装：
```python
setup(
    name=about["__title__"],  # 例如 "requests"
    version=about["__version__"],  # 例如 "2.32.3"
    description=about["__description__"],  # 简短摘要
    long_description=readme,  # 完整的 README
    long_description_content_type="text/markdown",  # 在 PyPI 上以 Markdown 格式渲染
    author=about["__author__"],  # 例如 "Kenneth Reitz"
    author_email=about["__author_email__"],
    url=about["__url__"],  # 例如 GitHub 仓库
    packages=["requests"],  # 安装 'requests' 包
    package_data={"": ["LICENSE", "NOTICE"]},  # 包含非 Python 文件
    package_dir={"": "src"},  # 源代码位于 'src/'
    include_package_data=True,  # 拉取所有数据文件
    python_requires=">=3.9",  # 与版本检查保持一致
    install_requires=requires,  # 来自前面的定义
    license=about["__license__"],  # 例如 "Apache 2.0"
    zip_safe=False,  # 允许编辑已安装的文件（库的常见做法）
    classifiers=[  # PyPI 分类，便于发现
        "Development Status :: 5 - Production/Stable",
        # ... (完整列表包括 Python 版本、操作系统、主题等)
    ],
    tests_require=test_requirements,  # 用于 `pip install -e '.[tests]'`
    extras_require={  # 可选依赖项
        "security": [],  # 为空——可能供将来使用
        "socks": ["PySocks>=1.5.6, !=1.5.7"],  # SOCKS 代理支持
        "use_chardet_on_py3": ["chardet>=3.0.2,<6"],  # 遗留字符集回退
    },
    project_urls={  # PyPI 页面上的链接
        "Documentation": "https://requests.readthedocs.io",
        "Source": "https://github.com/psf/requests",
    },
)
```
- **关键参数**：
  - **名称/版本/描述**：从 `__version__.py` 拉取，便于维护。
  - **包/包目录**：告诉 setuptools 包位于 `src/requests/` 下，并将其安装为 `import requests`。
  - **分类器**：一个字符串列表，用于对包进行分类（例如，稳定版、Python 3.9+、Apache 许可证、Web/HTTP 主题）。这有助于用户在 PyPI 上找到它。
  - **额外依赖项**：允许用户安装可选功能，例如 `pip install requests[socks]` 用于代理支持。
  - **项目 URL**：在 PyPI 页面上添加可点击的文档和源代码链接。

### 实际工作原理
- **安装**：`pip install .`（从仓库）或 `pip install requests`（从 PyPI）运行此脚本来复制文件、安装依赖项并设置包。
- **构建**：`python setup.py sdist` 创建可分发的归档文件。
- **为何采用这种结构？** 这是一种“src 布局”（代码在 `src/` 中），这是现代最佳实践，可以避免开发期间意外导入。该文件是自包含的，但将细节委托给其他文件，如 `__version__.py`。

这个 setup.py 来自官方的 Requests 仓库，并且多年来变化不大——它经过了实战测试，非常可靠。

### 参考资料
- [Requests 文档](https://requests.readthedocs.io/en/latest/)
- [Requests GitHub 仓库](https://github.com/psf/requests)
- [Python 打包用户指南](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
