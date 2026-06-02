---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用requests.Session保持HTTP会话持久连接
translated: true
type: note
---

### requests.Session 的工作原理

在 Python 的 `requests` 库中，`requests.Session` 是一个允许跨多个 HTTP 请求维持持久会话的类。与单独调用 `requests.get()` 等方法相比，它具有以下优势：

- **Cookie 持久化**：默认自动存储并发送从服务器接收的 Cookie，支持基于会话的交互（如一次登录后保持认证状态）
- **连接池**：复用同主机的底层 TCP 连接，避免新建连接开销以提升性能
- **共享配置**：可设置默认请求头、认证参数、代理等，应用于会话内所有请求
- **底层机制**：使用 `urllib3` 库处理 HTTP 请求。创建 `Session` 时会初始化 `cookies`（RequestsCookieJar 实例）、`headers` 等属性。例如，来自某响应的 Cookie 会自动包含在后续同域请求中

基础使用示例：

```python
import requests

# 创建会话
session = requests.Session()

# 为会话中所有请求设置默认请求头
session.headers.update({'User-Agent': 'MyApp/1.0'})

# 使用同一会话发起多个请求
response1 = session.get('https://example.com/login')
response2 = session.post('https://example.com/data', data={'key': 'value'})

# 访问会话中存储的 Cookie
print(session.cookies)
```

这种方式可自动处理 Cookie（如会话 ID）而无需手动干预。

### 使用 Python 调用 Java/Spring 项目 API

与调用其他 HTTP API 类似，可通过 `requests.Session` 与基于 Java/Spring 构建的 API（通常通过 Spring MVC 或 Spring Boot 暴露的 RESTful 端点）进行交互。Spring 项目常通过 HTTP/HTTPS 暴露 API，`requests` 能够处理已实现的认证、CSRF 令牌或限流机制。

- **认证方式**：Spring 可能使用基于表单的 Spring Security、JWT 或 OAuth。对于基于会话的认证（如通过登录表单），`requests.Session` 在登录请求后会自动处理 Cookie
- **调用方法**：使用标准 HTTP 方法（GET、POST 等）。若 Spring API 需要 JSON 载荷，需传递 `json=数据参数`

登录 Spring 认证 API 并调用其他端点的示例：

```python
import requests

session = requests.Session()

# 登录（假设向 /login 发送用户名/密码的 POST 请求）
login_payload = {'username': 'user', 'password': 'pass'}
response = session.post('https://spring-api.example.com/login', data=login_payload)

if response.ok:
    # 此时会话 Cookie 已持久化，可调用其他 API 端点
    data_response = session.get('https://spring-api.example.com/api/data')
    print(data_response.json())
else:
    print("登录失败")
```

Spring API 默认无状态，但可通过服务端存储（如 Tomcat 或嵌入式服务器）管理会话。请确保 Python 客户端处理 Spring 要求的 CORS、CSRF 或自定义请求头。

### 与 Java/Spring 服务端 JSESSIONID 的关联

- **JSESSIONID 的作用**：在 Java Web 应用（包括运行于 Tomcat 等 Servlet 容器的 Spring）中，JSESSIONID 是容器用于追踪用户会话的标准 HTTP Cookie。它在会话创建时（如登录后）被设置，并通过响应返回。客户端（浏览器或 `requests` 等 HTTP 客户端）会在后续请求中携带该 Cookie 以维持状态（如用户认证或购物车数据）
- **与 requests.Session 的关联**：`requests.Session` 将 JSESSIONID 视为普通 Cookie——自动从服务器的 Set-Cookie 头获取，并在后续请求的 Cookie 头中包含。这使得与有状态 Spring API 的交互无需手动解析/提取 Cookie
- **服务端处理**：在 Java/Spring 端，ServletContext 管理会话。当 Python 客户端发送带 JSESSIONID 的请求时，Spring 的 HttpSession 会获取关联的服务端数据。若会话过期或无效，Spring 可能要求重新认证。为确保会话安全，建议使用 HTTPS，因为 JSESSIONID 在 HTTP 下存在被盗风险
- **潜在问题**：若 Spring 启用了 CSRF 令牌等保护机制，可能需要提取并包含这些令牌（如从隐藏表单字段获取）。对于无状态的 JWT 架构 Spring API，`requests.Session` 仍可通过持久化请求头中的认证令牌提供帮助，此时 JSESSIONID 的重要性会降低

若调用 Spring API 时遇到特定错误（如 401 未认证），可通过网络日志检查 Cookie 问题，或使用 `import logging; logging.basicConfig(level=logging.DEBUG)` 启用 `requests` 调试模式。更多 Spring Security 细节请参阅官方文档。
