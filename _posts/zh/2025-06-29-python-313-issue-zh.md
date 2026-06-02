---
audio: false
generated: true
lang: zh
layout: post
title: Python 3.13 中的 CuPy 错误
translated: true
type: note
---

### 问题描述

在运行使用CuPy库进行GPU计算的Python脚本时，遇到`AttributeError`错误。该错误发生在`import cupy as cp`语句处，导致脚本无法执行。回溯信息指向CuPy内部代码的问题，具体位于`cupy/cuda/device.pyx`第105行，其中`memoize`装饰器试图修改内置函数或方法的`__name__`属性。错误信息如下：

```
AttributeError: attribute '__name__' of 'builtin_function_or_method' objects is not writable
```

这个问题似乎与您使用的Python 3.13有关，可能会导致与已安装CuPy版本的兼容性问题。

### 错误原因

该错误产生的原因是：

- **CuPy的`memoize`装饰器**：CuPy使用`memoize`装饰器来缓存函数结果以优化性能。该装饰器依赖Python的`functools.update_wrapper`来将原始函数的属性（如`__name__`）复制到包装函数。
- **内置函数**：在Python中，内置函数（用C实现）具有只读的`__name__`属性。当`update_wrapper`尝试设置此属性时，会因权限问题而失败。
- **Python 3.13兼容性**：CuPy的`device.pyx`中被记忆化的特定函数很可能是一个内置函数，而Python 3.13可能比先前版本执行更严格的规则或以不同方式处理内置函数，从而暴露了此问题。

由于错误发生在导入CuPy期间，这是一个与库初始化相关的系统性问题，而非脚本逻辑问题。

### 推荐解决方案

最简单实用的解决方法是使用已知与CuPy兼容的早期Python版本（如Python 3.11或3.12）运行脚本。这样可以避免Python 3.13的兼容性问题，无需修改CuPy源代码或实施复杂变通方案。

#### 方案优势

- **兼容性保障**：CuPy最新版本（如v11）已在Python 3.11和3.12环境中经过测试和验证，可避免此类错误。
- **零代码修改**：您的GPU排序基准测试脚本可在早期Python环境中直接运行，确保测试完整性。
- **快速部署**：通过虚拟环境或conda等工具可快速切换Python版本。

### 实施步骤

#### 方案一：使用`virtualenv`

1. **安装Python 3.11或3.12**
   - 通过系统包管理器或Python官网安装对应版本。

2. **创建虚拟环境**
   ```bash
   virtualenv -p python3.11 venv
   ```
   此命令创建名为`venv`的虚拟环境。如需使用Python 3.12，将`python3.11`替换为`python3.12`。

3. **激活虚拟环境**
   ```bash
   source venv/bin/activate
   ```

4. **安装CuPy**
   ```bash
   pip install cupy
   ```
   这将安装适用于Python 3.11的最新兼容版CuPy。

5. **运行脚本**
   ```bash
   python scripts/benchmark/cudamark.py
   ```
   此时脚本应能正常执行。

6. **退出环境（完成后）**
   ```bash
   deactivate
   ```

#### 方案二：使用`conda`

1. **创建Conda环境**
   ```bash
   conda create -n cudabench python=3.11
   ```
   创建名为`cudabench`的环境。如需Python 3.12，使用`python=3.12`。

2. **激活环境**
   ```bash
   conda activate cudabench
   ```

3. **安装CuPy**
   ```bash
   pip install cupy
   ```

4. **运行脚本**
   ```bash
   python scripts/benchmark/cudamark.py
   ```

5. **退出环境（完成后）**
   ```bash
   conda deactivate
   ```

### 验证结果

环境配置完成后运行脚本，应看到类似输出：

```
CPU核心数: <您的CPU核心数>
线程数: 1, 耗时: X.XXXX 秒
线程数: 2, 耗时: X.XXXX 秒
...
线程数,耗时(秒)
1,X.XXXXXX
2,X.XXXXXX
...
```

若脚本无`AttributeError`报错，即表明修复成功。

### 补充说明

- **脚本中的线程数设置**：您的脚本遍历线程数（`1, 2, 4, 8, 16, 32, 64, 128`），但`parallel_sort_gpu`函数使用CuPy的GPU排序（`cp.sort`），并不直接使用CPU线程。该循环可能不会如预期影响GPU排序性能。若为后续功能扩展（如添加CPU多线程）预留则无妨，否则可简化基准测试以专注GPU性能。
- **CuPy版本**：若怀疑CuPy版本过旧，可运行`pip install cupy --upgrade`更新。但核心问题在于Python 3.13兼容性，而非单纯版本问题。
- **长期解决方案**：如需坚持使用Python 3.13，建议关注CuPy的GitHub仓库或问题追踪器以获取对Python 3.13的支持更新（截至2025年6月可能尚未发布）。也可通过修改CuPy源码中`memoize`装饰器对内置函数的处理方式，但该方法较为复杂且对基准测试非必要。

通过使用Python 3.11或3.12，即可稳定运行GPU基准测试而避免此错误。
