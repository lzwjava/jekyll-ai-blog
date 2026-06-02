---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Python MagicMock 全面指南
translated: true
type: note
---

Question: Give a comprehensive guide about MagicMock in Python

Answer:

# Comprehensive Guide to MagicMock in Python

`MagicMock` 是 Python `unittest.mock` 模块中一个强大的类，专为在 unit tests 中创建 mock objects 而设计。它在模拟使用了 Python "magic" (dunder) methods（如 `__len__`、`__getitem__`、`__add__` 或 `__str__`）的对象时特别有用。

## Introduction to unittest.mock

`unittest.mock` 库（在 Python 3.3 中引入）允许你在测试期间用 mock objects 替换代码中的部分内容。这可以将 unit under test 与外部依赖项（如 databases、APIs、file systems）隔离开来。

核心类：
- `Mock`: 基础 mock object。
- `MagicMock`: `Mock` 的子类，预先实现了 magic methods。

## What is MagicMock?

`MagicMock` 是 `Mock` 的子类，它为大多数 Python magic methods 提供了默认实现。这使得它的行为更像真实的 Python objects（例如 lists、dicts 或具有特殊方法的自定义类），而无需手动配置。

```python
from unittest.mock import MagicMock

mock = MagicMock()
print(len(mock))  # Outputs: 0 (default behavior)
print(mock[0])    # Returns another MagicMock
print(mock + mock)  # Returns another MagicMock
```

官方文档建议将 `MagicMock` 作为默认选择，因为它的功能更全面。

## Mock vs. MagicMock

| Feature                  | Mock                          | MagicMock                                      |
|--------------------------|-------------------------------|------------------------------------------------|
| Base class               | Base mocking class            | Subclass of Mock                               |
| Magic methods            | Not pre-implemented (raises AttributeError by default) | Pre-implemented with sensible defaults        |
| When to use              | When you want minimal behavior and explicit control | Most cases, especially when mocking containers or objects with operators |
| Example: `len(mock)`     | Raises AttributeError         | Returns 0                                      |
| Example: `mock[0]`       | Raises AttributeError         | Returns a new MagicMock                        |
| Example: `mock + 1`      | Raises TypeError              | Returns a new MagicMock                        |

**建议**：除非你特别需要避免 magic method 的干扰，否则请使用 `MagicMock`。

## Creating a MagicMock

```python
from unittest.mock import MagicMock

# Basic creation
mock = MagicMock()

# With initial values
mock = MagicMock(name='my_mock', return_value='default_return')

# Specifying behavior for a method
mock.some_method.return_value = 42
mock.some_method.side_effect = [1, 2, 3]  # Returns sequentially
```

## Key Attributes and Methods

所有的 mocks（包括 `MagicMock`）都会追踪交互情况：

- `.called`: 如果 mock 至少被调用一次，则为 True。
- `.called_once`: 如果恰好被调用一次，则为 True。
- `.call_count`: 调用次数。
- `.call_args`: 最近一次调用的参数。
- `.call_args_list`: 所有调用参数的列表。
- `.method_calls`: 对子属性调用的列表。

Assertions（在测试中首选）：

```python
mock.some_method.assert_called()          # Called at least once
mock.some_method.assert_called_once()
mock.some_method.assert_called_with(1, 2, kw='value')
mock.some_method.assert_called_once_with(1, 2)
mock.some_method.assert_any_call(3, 4)    # Called with these args at least once
mock.some_method.assert_not_called()
```

## Configuring Behavior

- **return_value**: 调用时返回的固定值。

```python
mock = MagicMock(return_value=100)
print(mock())  # 100
```

- **side_effect**: 自定义行为。
  - Function: 使用参数调用并返回其结果。
  - Iterable: 按顺序返回元素。
  - Exception: 抛出异常。

```python
def my_effect(*args, **kwargs):
    return sum(args)

mock = MagicMock(side_effect=my_effect)
print(mock(1, 2, 3))  # 6

mock = MagicMock(side_effect=[10, 20, 30])
print(mock())  # 10
print(mock())  # 20

mock = MagicMock(side_effect=ValueError("Boom!"))
mock()  # Raises ValueError
```

## Magic Methods Examples

```python
mock = MagicMock()

# String representation
mock.__str__.return_value = 'Hello'
print(str(mock))  # Hello

# Length
mock.__len__.return_value = 5
print(len(mock))  # 5

# Iteration
mock.__iter__.return_value = iter([1, 2, 3])
print(list(mock))  # [1, 2, 3]

# Item access (behaves like a dict)
mock.__getitem__.side_effect = {'a': 1, 'b': 2}.__getitem__
print(mock['a'])  # 1
```

## Using with patch()

`patch()` 用于临时替换对象。它默认返回一个 `MagicMock`。

```python
from unittest.mock import patch

@patch('module.ClassUnderTest.method')
def test_something(mock_method):
    mock_method.return_value = 42
    # Call code that uses ClassUnderTest.method
    result = my_function()
    mock_method.assert_called_with(expected_args)
```

作为 context manager 使用：

```python
with patch('module.some_function') as mock_func:
    mock_func.return_value = True
    # Test code here
```

## Advanced Features

- **spec / spec_set**: 限制 mock 以匹配真实对象的 interface。

```python
class RealClass:
    def method(self, x): ...

mock = MagicMock(spec=RealClass)
mock.method(1)  # OK
mock.unknown()  # Raises AttributeError
```

- **create_autospec**: 更安全的 mocking 方式，带有 signature 检查。

```python
from unittest.mock import create_autospec

mock = create_autospec(RealClass)
```

- **attach_mock**: 手动构建嵌套的 mocks。
- **NonCallableMagicMock**: 用于不可调用的对象。

## Best Practices

- 通用场景下优先选择 `MagicMock`。
- 使用 `spec` 或 `create_autospec` 以避免拼写错误并保持测试的可维护性。
- 避免过度 mocking；专注于行为验证。
- 结合 `patch` 在测试中进行 dependency injection。

`MagicMock` 通过模拟真实的 object 行为，同时允许对交互进行详细的 assertions，使测试变得更加直观。

References:

- [unittest.mock — mock object library — Python 3.13 documentation](https://docs.python.org/3/library/unittest.mock.html)
- [unittest.mock — getting started — Python 3.13 documentation](https://docs.python.org/3/library/unittest.mock-examples.html)
- [Mock vs MagicMock - Stack Overflow](https://stackoverflow.com/questions/17181687/mock-vs-magicmock)
- [Mastering unittest.mock in Python | Better Stack Community](https://betterstack.com/community/guides/scaling-python/python-unittest-mock/)
