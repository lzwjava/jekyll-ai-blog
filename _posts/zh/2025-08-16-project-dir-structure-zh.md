---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 项目目录结构最佳实践
translated: true
type: note
---

好问题。

通常的约定是：

* **`scripts/`** 用于存放应用程序代码（需要在生产环境运行或作为项目组成部分的内容）
* **`tests/`** 用于存放测试代码（用于验证脚本/模块正确性的内容）

因此如果你要添加新的测试文件，通常应该放在 **`tests/llm/`** 目录下，而不是 `scripts/` 目录。

例如：

```
scripts/
  llm/
    main.py
    utils.py
tests/
  llm/
    test_main.py
    test_utils.py
```

这样可以将测试代码与实现代码分离，方便像 `pytest` 这样的工具自动发现测试用例。

👉 你现在可以添加类似这样的代码：

```python
# tests/llm/test_basic.py
import pytest
from scripts.llm import utils

def test_addition():
    assert utils.add(2, 3) == 5
```

然后运行：

```bash
pytest tests/llm/
```

需要我同时展示如何设置 `conftest.py` 文件，以便在 `tests/llm/` 目录下的文件中共享测试夹具吗？
