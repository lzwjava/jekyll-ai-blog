---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 理解Pytest Fixture的用法
translated: true
type: note
---

## 什么是 `@pytest.fixture`？

`@pytest.fixture` 是一个装饰器，用于将函数标记为**fixture**——一种为测试提供测试数据、设置或清理功能的特殊函数。Fixture 是 pytest 最强大的功能之一，也是许多开发者偏爱 pytest 而非 Python 内置 `unittest` 模块的关键原因。

## Fixture 的工作原理

Fixture 遵循一个简单但强大的模式：

1. **设置**：`yield` 语句之前的代码在测试前运行
2. **测试执行**：测试在到达 `yield` 语句时运行
3. **清理**：`yield` 语句之后的代码在测试完成后运行

### 基础 Fixture 示例

```python
import pytest

@pytest.fixture
def sample_data():
    # 设置代码
    data = {"name": "John", "age": 30}
    yield data  # 测试在此处运行
    # 清理代码（测试后运行）
    print("Cleaning up sample data")
```

## 为什么需要 Fixture

Fixture 解决了几个常见的测试问题：

1. **测试隔离**：确保每个测试都使用新鲜、可预测的数据运行
2. **代码复用**：避免在多个测试中重复设置/清理代码
3. **资源管理**：正确处理数据库连接、文件或网络连接等资源
4. **测试清晰度**：让测试函数专注于测试内容，而不是设置工作
5. **依赖注入**：为每个测试提供其所需的内容

## Fixture 的主要特性

### 1. 依赖注入

Fixture 可以依赖于其他 fixture，创建依赖关系图：

```python
@pytest.fixture
def database_connection():
    # 设置数据库连接
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture
def user_table(database_connection):
    # 使用 database_connection fixture
    create_table(database_connection, "users")
    yield
    drop_table(database_connection, "users")
```

### 2. 作用域控制

Fixture 可以有不同的生命周期：

```python
@pytest.fixture(scope="function")  # 默认 - 每个测试运行一次
def per_test_fixture():
    pass

@pytest.fixture(scope="module")  # 每个模块运行一次
def per_module_fixture():
    pass

@pytest.fixture(scope="session")  # 每个测试会话运行一次
def per_session_fixture():
    pass
```

### 3. 自动使用 Fixture

Fixture 可以自动运行而无需显式请求：

```python
@pytest.fixture(autouse=True)
def always_run_this():
    # 这会在模块中的每个测试前运行
    yield
    # 这会在每个测试后运行
```

### 4. 参数化 Fixture

Fixture 可以生成多组数据：

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param  # 将使用 1、2 和 3 运行测试
```

## API 测试的实用示例

以下展示 fixture 如何帮助您的金融头测试场景：

```python
import pytest
import requests

@pytest.fixture
def financial_header():
    # 设置 - 创建头信息
    headers = create_financial_header()  # 您的创建逻辑
    yield headers  # 测试使用这些头信息运行

    # 清理 - 删除头信息
    delete_financial_header(headers)  # 您的清理逻辑

def test_submit_transaction(financial_header):
    # fixture 自动提供头信息
    response = requests.post(
        "https://api.example.com/transactions",
        headers=financial_header,
        json={"amount": 100}
    )
    assert response.status_code == 201

def test_validate_header(financial_header):
    # 相同的 fixture 在另一个测试中使用
    response = requests.get(
        "https://api.example.com/validate",
        headers=financial_header
    )
    assert response.json()["valid"] is True
```

## 与 unittest 的对比

| 特性               | pytest Fixtures                     | unittest setUp/tearDown          |
|-------------------|-------------------------------------|----------------------------------|
| 依赖注入           | ✅ 支持                             | ❌ 不支持                         |
| 作用域控制         | ✅ 函数、类、模块、会话级别         | ❌ 仅方法和类级别                 |
| 简洁语法           | ✅ 简单的装饰器                     | ❌ 需要继承                       |
| 测试隔离           | ✅ 每个测试获得新的 fixture         | ❌ 共享状态可能导致问题           |
| 参数化             | ✅ 内置支持                         | ❌ 需要手动实现                   |

## 何时使用 Fixture

在以下情况下使用 fixture：
- 设置测试数据或对象
- 管理外部资源（数据库连接、文件等）
- 在测试后执行清理
- 共享常见的测试依赖
- 创建不同的测试环境
- 实现复杂的设置/清理逻辑

在 API 测试中（如您的金融头测试案例），fixture 特别有价值，因为它们有助于以清晰和可预测的方式管理测试资源的生命周期。
