---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决PyYAML安装错误
translated: true
type: note
---

### 理解错误信息

这段输出来自在 Linux 系统（Python 3.13 环境）执行 `python setup.py install` 或 `pip install pyyaml`（从源码安装）的结果。主要存在两个问题：

1. **C 扩展编译失败**：
   - 构建过程尝试编译 C 扩展（`yaml._yaml`）时找不到源文件 `yaml/_yaml.c`
   - 这是因为新版 PyYAML（约 4.x 起）会在构建时使用 Cython 动态生成 `_yaml.c` 文件。PyPI 上的源码分发包不包含预生成的 `.c` 文件，因此需要提前安装 Cython 来生成该文件
   - 最终系统回退到纯 Python 版本（功能正常但性能较低，且缺少 libyaml 支持等特性）

2. **安装过程中权限被拒绝**：
   - 安装程序尝试写入系统级 Python 目录（`/usr/local/lib/python3.13/dist-packages`），该操作需要 root 权限
   - 这种情况常见于未使用 `sudo` 或 `--user` 参数时

### 解决方案

#### 修复编译问题

先安装 Cython，然后重新尝试安装 PyYAML。这将生成缺失的 `_yaml.c` 文件并允许构建 C 扩展。

- **使用 pip（推荐）**：

  ```
  pip install cython
  pip install pyyaml
  ```

  - 如果需要启用更快的 libyaml C 扩展（需通过系统包管理器安装 libyaml-dev，如在 Ubuntu/Debian 上执行 `sudo apt install libyaml-dev`）：

    ```
    pip install cython libyaml
    pip install --upgrade --force-reinstall --no-cache-dir pyyaml
    ```

- **如果直接使用 setup.py**（不推荐，建议优先使用 pip）：

  ```
  pip install cython
  python setup.py build_ext --inplace
  python setup.py install
  ```

注意：Python 3.13 相对较新，请确保使用最新版 Cython（如 3.0.11 或更高版本）以保证兼容性。如果使用自由线程模式的 Python 构建版本，可能需要额外的编译调整——请查阅 PyYAML 的 GitHub issues 获取最新信息。

#### 修复权限问题

- **安装到用户目录**（最安全，无需 sudo）：

  ```
  pip install --user cython pyyaml
  ```

  - 这将安装到 `~/.local/lib/python3.13/site-packages`

- **使用 sudo 进行系统级安装**（请谨慎使用，可能与系统包管理器冲突）：

  ```
  sudo pip install cython pyyaml
  ```

- **最佳实践：使用虚拟环境**：
  彻底避免权限问题：

  ```
  python -m venv myenv
  source myenv/bin/activate  # Linux/Mac 系统
  pip install cython pyyaml
  ```

  这种方式可以保持环境隔离

安装完成后，可通过 `python -c "import yaml; print(yaml.__version__)"` 测试。如果无报错则说明安装成功。

如果以上方法仍无法解决问题（例如由于 Python 3.13 的特殊性），请提供更多详细信息，如具体执行的命令和操作系统版本。

[在 Mac 上构建 - 找不到 _yaml.c](https://github.com/yaml/pyyaml/issues/122)
[扩展 _yaml 未构建](https://github.com/yaml/pyyaml/issues/179)
[在 MacOS 上安装支持 libyaml 的 Pyyaml](https://akasurde.github.io/installing-pyyaml-with-libyaml-on-macos.html)
