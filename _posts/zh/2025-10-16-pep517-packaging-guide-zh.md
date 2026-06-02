---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: PEP 517 Python打包指南
translated: true
type: note
---

PEP 517 于 2016 年被采纳，它为构建 Python 包定义了一个标准化接口，将构建后端（创建分发包的逻辑）与前端（如 pip 这类编排流程的工具）解耦。这使得开发者能够使用现代构建工具，而无需受限于像 setuptools 的 `setup.py` 这样的遗留系统。结合 PEP 518（指定构建依赖），它支持从源码树或源码分发包（sdists）进行可靠、隔离的构建。截至 2025 年，PEP 517 已成为现代 Python 打包的基础，得到了 pip（自版本 10 起支持 PEP 518，自版本 19 起完全支持 PEP 517）以及 Poetry、Flit 和 PDM 等工具的支持。

本指南涵盖了其动机、关键概念、规范、工作流程、实现及最佳实践。

## 动机与背景

Python 打包从 `distutils`（Python 1.6 引入，2000 年）发展到 `setuptools`（2004 年），后者增加了依赖管理但也带来了问题：
- **命令式且脆弱**：构建依赖于执行 `python setup.py`，这是一个可能因环境假设（例如，缺少用于扩展的 Cython）而失败的任意脚本。
- **无构建依赖声明**：构建所需的工具（例如编译器、Cython）未被声明，导致手动安装和版本冲突。
- **紧密耦合**：Pip 硬编码了 `setup.py` 的调用，阻碍了如 Flit 或 Bento 等替代构建系统。
- **主机环境污染**：构建使用用户的全局 Python 环境，存在副作用风险。

这些问题抑制了创新，并在源码安装（例如从 Git）时导致错误。PEP 517 通过标准化一个最小接口解决了这个问题：前端在隔离环境中调用后端钩子。Wheels（预构建的二进制文件，2014 年引入）简化了分发——后端只需生成符合规范的 wheels/sdists。PEP 518 通过 `pyproject.toml` 声明构建需求来补充，实现了隔离。

结果是：一个声明式、可扩展的生态系统，其中 `setup.py` 是可选的，并且像 pip 这样的工具可以在没有遗留回退的情况下构建任何兼容的项目。

## 关键概念

### 源码树与分发包
- **源码树**：包含包代码和 `pyproject.toml` 的目录（例如 VCS 检出）。像 `pip install .` 这样的工具从中构建。
- **源码分发包 (Sdist)**：一个 gzip 压缩的 tar 包（`.tar.gz`），如 `package-1.0.tar.gz`，解压到一个包含 `pyproject.toml` 和元数据（PKG-INFO）的 `{name}-{version}` 目录。用于发布和下游打包（例如 Debian）。
- **Wheel**：一个 `.whl` 二进制分发包——预构建、平台特定，无需编译即可安装。PEP 517 要求使用 wheels 以保证可重现性。

遗留的 sdists（PEP 517 之前）解压到可执行树，但现在必须包含 `pyproject.toml` 以符合规范。

### pyproject.toml
这个 TOML 文件集中了配置。`[build-system]` 部分（来自 PEP 518/517）指定：
- `requires`：构建所需的 PEP 508 依赖列表（例如 `["setuptools>=40.8.0", "wheel"]`）。
- `build-backend`：后端的入口点（例如 `"setuptools.build_meta"` 或 `"poetry.masonry.api"`）。
- `backend-path`（可选）：用于自托管后端的、添加到 `sys.path` 的树内路径（例如 `["src/backend"]`）。

最小配置示例：
```
[build-system]
requires = ["setuptools>=40.8.0", "wheel"]
build-backend = "setuptools.build_meta"
```

需求形成一个有向无环图（无环；前端检测到环则失败）。其他部分如 `[project]`（PEP 621）或 `[tool.poetry]` 保存元数据/依赖。

### 构建后端与前端
- **后端**：通过钩子（可调用函数）实现构建逻辑。在子进程中运行以实现隔离。
- **前端**：编排流程（例如 pip）。设置隔离环境，安装需求，调用钩子。
- **解耦**：前端调用标准化的钩子，而非 `setup.py`。这支持多样化的后端而无需更改 pip。

钩子使用 `config_settings`（用于标志的字典，例如 `{"--debug": true}`）并可能输出到 stdout/stderr（UTF-8 编码）。

## 规范详情

### [build-system] 详情
- `requires`：PEP 508 字符串（例如 `">=1.0; sys_platform == 'win32'"`）。
- `build-backend`：`module:object`（例如 `flit_core.buildapi` 导入 `flit_core`；`backend = flit_core.buildapi`）。
- 无 `sys.path` 污染——后端通过隔离导入。

### 钩子
后端将这些作为属性暴露：

**必需：**
- `build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str`：在 `wheel_directory` 中构建 wheel，返回基本文件名（例如 `"myproj-1.0-py3-none-any.whl"`）。如果提供了先前元数据则使用它。通过临时文件处理只读源。
- `build_sdist(sdist_directory, config_settings=None) -> str`：在 `sdist_directory` 中构建 sdist（pax 格式，UTF-8 编码）。如果不可能（例如无 VCS）则抛出 `UnsupportedOperation`。

**可选（默认为 `[]` 或回退）：**
- `get_requires_for_build_wheel(config_settings=None) -> list[str]`：额外的 wheel 依赖（例如 `["cython"]`）。
- `prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str`：写入 `{pkg}-{ver}.dist-info` 元数据（遵循 wheel 规范，无 RECORD）。返回基本文件名；如果缺失，前端从 wheel 中提取。
- `get_requires_for_build_sdist(config_settings=None) -> list[str]`：额外的 sdist 依赖。

钩子在出错时抛出异常。前端在隔离环境中调用钩子（例如，仅包含标准库 + 需求的 venv）。

### 构建环境
- 隔离的 venv：用于 `get_requires_*` 的引导环境，用于构建的完整环境。
- PATH 中的 CLI 工具（例如 `flit`）。
- 无标准输入；每个钩子使用子进程。

## 构建流程详解

### 逐步工作流程
对于 `pip install .`（源码树）或 sdist 安装：

1. **发现**：前端读取 `pyproject.toml`。
2. **隔离设置**：创建 venv；安装 `requires`。
3. **需求查询**：调用 `get_requires_for_build_wheel`（安装额外依赖）。
4. **元数据准备**：调用 `prepare_metadata_for_build_wheel`（或构建 wheel 并提取）。
5. **Wheel 构建**：在隔离环境中调用 `build_wheel`；安装生成的 wheel。
6. **回退**：如果不支持 sdist，则构建 wheel；如果无钩子，则使用遗留 `setup.py`。

对于 sdists：解包，视为源码树。开发者工作流程（例如 `pip wheel .`）：
1. 隔离环境。
2. 调用后端钩子以构建 wheel/sdist。

### 构建隔离（PEP 518）
为构建创建临时 venv，避免污染主机环境。Pip 的 `--no-build-isolation` 禁用此功能（谨慎使用）。像 tox 这样的工具默认使用隔离。

新旧对比：
- **旧**：在主机环境中执行 `python setup.py install`——存在冲突风险。
- **新**：隔离的钩子——可重现、安全。

## 实现一个构建后端

创建后端：
1. 定义一个包含钩子的模块（例如 `mybackend.py`）。
2. 将 `build-backend` 指向它。

最小示例（纯 Python 包）：
```python
# mybackend.py
from zipfile import ZipFile
import os
from pathlib import Path

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    # 复制源码到 wheel 目录，压缩为 .whl
    dist = Path(wheel_directory) / "myproj-1.0-py3-none-any.whl"
    with ZipFile(dist, 'w') as z:
        for src in Path('.').rglob('*'):
            z.write(src, src.relative_to('.'))
    return str(dist.relative_to(wheel_directory))

# 可选钩子
def get_requires_for_build_wheel(config_settings=None):
    return []

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    # 写入 METADATA 等
    return "myproj-1.0.dist-info"
```

在 `pyproject.toml` 中：
```
[build-system]
requires = []
build-backend = "mybackend:build_wheel"  # 实际指向模块对象
```

使用像 `pyproject-hooks` 这样的库来处理样板代码。对于扩展，通过 `config_settings` 集成 C 编译器。

## 与工具一起使用 PEP 517

- **pip**：自动检测 `pyproject.toml`；使用 `--use-pep517`（自 19.1 起默认）。对于可编辑安装：`pip install -e .` 调用钩子。
- **Poetry**：声明式工具。生成：
  ```
  [build-system]
  requires = ["poetry-core>=1.0.0"]
  build-backend = "poetry.core.masonry.api"
  ```
  通过 `poetry build` 安装；与 pip 兼容。
- **Flit**：适用于纯 Python 的简单工具。使用：
  ```
  [build-system]
  requires = ["flit_core >=3.2,<4"]
  build-backend = "flit_core.buildapi"
  ```
  `flit publish` 构建/上传。
- **Setuptools**：遗留桥接：
  ```
  [build-system]
  requires = ["setuptools>=40.8.0", "wheel"]
  build-backend = "setuptools.build_meta"
  ```
  支持 `setup.cfg` 用于声明式元数据。

迁移遗留项目：添加 `[build-system]`；移除 `setup.py` 调用。

## 错误处理与最佳实践

- **错误**：钩子抛出异常（例如，`ValueError` 表示无效配置）。循环依赖：前端失败并显示消息。不支持的 sdist：回退到 wheel。
- **最佳实践**：
  - 优先使用声明式（`setup.cfg` 或 `[project]`）。
  - 声明精确的构建依赖（例如 `cython==0.29`）。
  - 测试隔离：使用 `pip wheel . --no-build-isolation` 进行调试。
  - 对于树内后端：使用 `backend-path`；避免循环。
  - 安全性：钩子在子进程中运行；无任意代码。
  - 兼容性：为旧工具包含 `setup.py`。

截至 2025 年，setuptools 仍占主导地位（根据调查），但 Poetry/Flit 因其简洁性而采用率增长。

## 参考资料
- [PEP 517 – 源码树的构建系统无关格式](https://peps.python.org/pep-0517/)
- [PEP 517 和 518 通俗解释](https://chadsmith-software.medium.com/pep-517-and-518-in-plain-english-47208ca8b7a6)
- [Python 打包 - 过去、现在、未来](https://bernat.tech/posts/pep-517-518/)
- [什么是 PEP 517/518 兼容性？](https://pydevtools.com/handbook/explanation/what-is-pep-517/)
- [现代 pip 构建流程（–use-pep517）](https://fromkk.com/posts/modern-pip-build-process-use-pep517/)
- [什么是构建后端？](https://pydevtools.com/handbook/explanation/what-is-a-build-backend/)
