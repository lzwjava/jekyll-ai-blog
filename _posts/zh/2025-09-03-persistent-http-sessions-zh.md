---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Python Requests实现持久HTTP会话
translated: true
type: note
---

Python `requests` 库中的 `Session` 是一种在多个 HTTP 请求间保持特定参数（如 cookies、headers 和认证信息）持久化的方式。它提供了一个便捷的接口，用于向同一服务器或相关端点发起重复请求，同时保持状态、提升效率并简化代码。下面我将解释 `requests.Session` 的工作原理、主要特性，并提供示例说明其用法。

## 什么是 `requests.Session`？

`requests` 库在 Python 中被广泛用于发起 HTTP 请求。虽然你可以使用独立函数如 `requests.get()` 或 `requests.post()`，但 `Session` 对象允许你创建一个持久化会话，在多个请求间保留配置（例如 cookies、headers 或认证凭证）。这对于需要状态交互的网站或 API 交互特别有用，例如保持登录状态或复用 TCP 连接。

`Session` 对象：

- 在请求间保持 cookies 持久化
- 复用底层 TCP 连接（通过连接池），在向同一主机发起多个请求时提升性能
- 允许设置默认参数（如 headers、超时时间），这些参数将应用于该会话的所有请求
- 支持认证和自定义配置

## `Session` 如何工作？

当你创建 `Session` 对象时，它充当 HTTP 请求的容器。以下是其功能分解：

1. **持久化 Cookies**：使用 `Session` 发起请求时，服务器设置的任何 cookies（例如登录后的会话 cookies）都会存储在会话中，并自动随后续请求发送。这对于保持状态（如保持登录）至关重要。

2. **连接池**：对于向同一主机的请求，`Session` 会复用相同的 TCP 连接，相比为每个请求创建新连接，减少了延迟和开销。

3. **默认参数**：你可以在 `Session` 对象上设置 headers、认证或超时等属性，这些设置将应用于该会话的所有请求，除非被覆盖。

4. **可定制性**：你可以配置代理、SSL 验证，甚至挂载自定义适配器（例如用于重试或自定义传输）来控制请求处理方式。

## 基本用法

以下是使用 `requests.Session` 的简单示例：

```python
import requests

# 创建会话
session = requests.Session()

# 为该会话的所有请求设置默认 headers
session.headers.update({'User-Agent': 'MyApp/1.0'})

# 发起 GET 请求
response1 = session.get('https://api.example.com/data')
print(response1.json())

# 发起另一个请求；cookies 和 headers 会被复用
response2 = session.post('https://api.example.com/submit', data={'key': 'value'})
print(response2.json())

# 关闭会话以释放资源
session.close()
```

在此示例中：

- 创建了 `Session`，并为所有请求设置了自定义 `User-Agent` header
- 会话自动处理 cookies，因此如果 `response1` 设置了 cookie，它会随 `response2` 发送
- 会话复用到 `api.example.com` 的连接，提升了性能

## 主要特性与示例

### 1. **保持 Cookies 持久化**

会话对于使用 cookies 保持状态的网站特别有用，例如登录会话。

```python
import requests

# 创建会话
session = requests.Session()

# 登录网站
login_data = {'username': 'user', 'password': 'pass'}
response = session.post('https://example.com/login', data=login_data)

# 访问受保护页面；会话自动发送登录 cookie
protected_page = session.get('https://example.com/protected')
print(protected_page.text)

# 关闭会话
session.close()
```

这里，会话存储了登录请求的认证 cookie，并在后续请求中将其发送到受保护页面。

### 2. **设置默认参数**

你可以为会话中的所有请求设置默认 headers、认证或其他参数。

```python
import requests

session = requests.Session()

# 设置默认 headers
session.headers.update({
    'Authorization': 'Bearer my_token',
    'Accept': 'application/json'
})

# 设置默认超时时间
session.request = functools.partial(session.request, timeout=5)

# 发起请求；headers 和超时设置会自动应用
response1 = session.get('https://api.example.com/endpoint1')
response2 = session.get('https://api.example.com/endpoint2')

session.close()
```

### 3. **连接池**

当向同一主机发起多个请求时，`Session` 会复用连接，这比独立请求更高效。

```python
import requests
import time

# 不使用会话
start = time.time()
for _ in range(5):
    requests.get('https://api.example.com/data')
print(f"Without session: {time.time() - start} seconds")

# 使用会话
session = requests.Session()
start = time.time()
for _ in range(5):
    session.get('https://api.example.com/data')
print(f"With session: {time.time() - start} seconds")
session.close()
```

基于会话的请求通常更快，因为它们复用了 TCP 连接。

### 4. **认证**

会话简化了认证处理，例如 HTTP 基本认证或自定义基于令牌的认证。

```python
import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth('user', 'pass')

# 所有请求都将包含基本认证
response = session.get('https://api.example.com/protected')
print(response.json())

session.close()
```

### 5. **自定义适配器**

你可以挂载自定义适配器来控制重试或连接池行为等。

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

# 配置重试策略
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# 发起带重试逻辑的请求
response = session.get('https://api.example.com/unstable_endpoint')
print(response.json())

session.close()
```

此示例为特定 HTTP 错误码设置了自动重试。

## 何时使用 `Session`

在以下情况下使用 `requests.Session`：

- 需要在多个请求间保持状态（例如 cookies），例如用于认证
- 向同一主机发起多个请求，并希望受益于连接池
- 希望在请求间应用一致的配置（headers、超时等）
- 与需要基于会话交互的 API 或网站交互

如果仅发起单个请求或不需要保持状态，使用独立的 `requests.get()` 或 `requests.post()` 即可。

## 关闭会话

完成后务必关闭会话以释放资源（例如连接）：

```python
session.close()
```

或者，将会话用作上下文管理器以确保自动关闭：

```python
with requests.Session() as session:
    session.headers.update({'User-Agent': 'MyApp/1.0'})
    response = session.get('https://api.example.com/data')
    print(response.json())
# 退出代码块时会话自动关闭
```

## 高级说明

- **线程安全**：`Session` 对象不是线程安全的。如果使用多线程，请为每个线程创建单独的 `Session`
- **代理**：可以通过 `session.proxies = {'http': 'http://proxy.com', 'https': 'https://proxy.com'}` 在会话上设置代理
- **SSL 验证**：默认情况下，`Session` 会验证 SSL 证书。要禁用（生产环境不推荐），使用 `session.verify = False`

## 参考资料

[Requests 文档](https://requests.readthedocs.io/en/latest/)
[Requests 会话对象](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects)
