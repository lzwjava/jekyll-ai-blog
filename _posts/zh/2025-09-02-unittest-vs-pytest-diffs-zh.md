---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Unittest与Pytest核心差异解析
translated: true
type: note
---

以下是一份简洁明了的对比，重点关注日常测试中实际发生的变化。

# 理念与风格

* **unittest**：xUnit 风格（类似 Java/JUnit）。基于类的测试，包含生命周期钩子如 `setUp/tearDown`，方法名必须以 `test_` 开头。
* **pytest**：Python 风格且极简。支持测试**函数**或类，提供丰富的 fixture，使用普通的 `assert` 并支持断言重写。

# 测试发现

* **unittest**：使用 `python -m unittest discover`（或加载测试套件）。查找 `test*.py` 文件和 `TestCase` 的子类。
* **pytest**：使用 `pytest` 自动发现 `test_*.py` 和 `*_test.py` 文件；查找 `test_*` 函数和 `Test*` 类中的方法。

# 断言

* **unittest**：提供多种特定方法（`assertEqual`、`assertTrue`、`assertRaises` 等）。
* **pytest**：使用普通的 `assert`，并输出详细的差异对比（“左侧 vs 右侧”），支持 `pytest.raises`。

# Fixture 与设置

* **unittest**：使用 `setUp()/tearDown()`、`setUpClass/tearDownClass`、`setUpModule/tearDownModule`。
* **pytest**：提供具有作用域的 **fixture**（函数/类/模块/会话），支持依赖注入、自动使用和终结器。鼓励使用小型、可重用的设置。

# 参数化

* **unittest**：无内置支持；需使用循环/subTest 或第三方库。
* **pytest**：`@pytest.mark.parametrize` 是一等公民（支持输入矩阵和清晰的报告）。

# 跳过、预期失败与标记

* **unittest**：提供 `@skip`、`@skipIf`、`@expectedFailure`。
* **pytest**：包含相同功能，外加强大的**标记**（`@pytest.mark.slow`、`xfail`、`filterwarnings`、自定义标记）和命令行选择（`-m slow`）。

# 插件与生态系统

* **unittest**：内置功能齐全但精简；依赖外部运行器/工具实现高级功能。
* **pytest**：拥有庞大的插件生态系统（`pytest-xdist` 用于并行测试、`pytest-randomly`、`pytest-cov`、`pytest-mock`、`pytest-asyncio`、`pytest-django` 等）。

# Mock

* **unittest**：`unittest.mock` 是标准库；可在任何地方使用。
* **pytest**：可使用 `unittest.mock` 或 `pytest-mock` 的 `mocker` fixture（更清晰的补丁和自动清理）。

# 异步测试

* **unittest**：自 3.8 版本起提供 `IsolatedAsyncioTestCase`（功能尚可但较冗长）。
* **pytest**：通过 `pytest-asyncio`（或 trio 的插件）提供 `@pytest.mark.asyncio` 和对事件循环的 fixture 支持。

# 性能与并行

* **unittest**：无内置并行支持；需使用 `unittest-parallel`/CI 技巧。
* **pytest**：`pytest-xdist -n auto` 是首选方案。

# IDE/CI/覆盖率

* 两者均与 IDE 和 CI 集成。通过 `coverage.py` 实现覆盖率：

  * **unittest**：`coverage run -m unittest` → `coverage report`。
  * **pytest**：使用 `pytest-cov` 时执行 `pytest --cov=your_pkg`。

# 如何选择

* **选择 unittest** 如果：

  * 你只需要标准库（无外部依赖）。
  * 你需要接入遗留/xUnit 代码库或严格的组织政策。
* **选择 pytest** 如果：

  * 你希望更快地编写测试、获得更清晰的失败信息和强大的 fixture/参数化功能。
  * 你能从其插件生态系统和并行化中受益。

# 互操作与迁移

你可以在 **pytest** 下运行 **unittest** 测试套件（pytest 能发现 `unittest.TestCase`）。这使你可以逐步迁移：

1. 开始使用 `pytest` 作为运行器。
2. 在现有测试旁添加 pytest 测试。
3. 在需要的地方引入 fixture/参数化。
4. 后续可选择将旧的 `TestCase` 重构为函数。

# 小型对比示例

## 相同的测试

**unittest**

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.data = [1, 2, 3]

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

if __name__ == "__main__":
    unittest.main()
```

**pytest**

```python
import pytest

@pytest.fixture
def data():
    return [1, 2, 3]

def test_sum(data):
    assert sum(data) == 6

def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## 参数化

**unittest (subTest)**

```python
import unittest

class TestParity(unittest.TestCase):
    def test_even(self):
        for n in [0, 2, 4]:
            with self.subTest(n=n):
                self.assertEqual(n % 2, 0)
```

**pytest**

```python
import pytest

@pytest.mark.parametrize("n", [0, 2, 4])
def test_even(n):
    assert n % 2 == 0
```

## Mocking

**unittest.mock**

```python
from unittest.mock import patch

@patch("pkg.api.fetch_user", return_value={"id": 1})
def test_uses_api(mock_fetch):
    from pkg.service import get_user
    assert get_user(1)["id"] == 1
    mock_fetch.assert_called_once_with(1)
```

**pytest-mock**

```python
def test_uses_api(mocker):
    mock_fetch = mocker.patch("pkg.api.fetch_user", return_value={"id": 1})
    from pkg.service import get_user
    assert get_user(1)["id"] == 1
    mock_fetch.assert_called_once_with(1)
```

# 实用建议

* 新项目：默认使用 **pytest**，以获得速度、可读性和生态系统优势。
* 遗留/仅限标准库的环境：坚持使用 **unittest**，但考虑通过 **pytest** 运行以在不重写测试的情况下获得更好的输出和插件支持。
* 早期添加 `pytest-xdist` 以加速 CI，添加 `pytest-cov` 以获取覆盖率。
* 使用 fixture 替代大型类设置；保持其小型化和可组合性。
* 使用标记来组织测试套件（`slow`、`integration`、`db`）并在 CI 阶段运行子集。

如果你愿意，告诉我你的项目结构和约束（仅限标准库？需要并行？异步？Django/Flask/FastAPI？），我可以为你设计一个最小化且实用的测试设置方案。
