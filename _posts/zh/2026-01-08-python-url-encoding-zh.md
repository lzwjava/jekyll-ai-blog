---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Python URL 中进行特殊字符编码
translated: true
type: note
---

Question: 有时我们需要在 URL 中使用像 http://username:password@someproxy 这样的 endpoint，对吧？如果使用 password 包含 # 或 . 等字符，Python 可能会报 parse failure 错误。

Answer:

是的，在构建包含身份验证凭据（username:password@host）的 URL 时，用户名或密码中的特殊字符必须经过 percent-encoded（URL-encoded），以避免解析问题。

### 为什么会发生这种情况

Python 的 `urllib.parse.urlparse`（或 `requests` 等库中的类似解析器）会将 URL 拆分为多个组件。分隔符如 `:`、`@`、`/`、`?` 和 `#` 具有特殊含义：

- `:` 分隔用户名和密码。
- `@` 分隔凭据和 host。
- `#` 标志着 fragment 的开始。
- `?` 标志着 query 的开始。
- `.` 在密码中通常没问题，但其他字符可能导致误判。

如果密码包含 `#`，解析器可能会将 `#` 之后的所有内容视为 fragment，从而导致错误的 netloc（网络位置）以及解析错误或失败（例如，因无效的 port 或 host 导致 ValueError）。

这是 Python `urllib` 中的已知行为（参见相关 bug，例如除非经过编码，否则会将 `#` 或 `?` 视为分隔符）。

### 正确的解决方案

使用 `urllib.parse.quote`（或者在某些情况下使用 `quote_plus`，但此处 `quote` 更安全，因为它不会将空格替换为 `+`）对用户名和/或密码进行 percent-encode。

**推荐方法：通过编码手动构建 URL**

```python
from urllib.parse import quote

username = "myuser"
password = "pass#word.with.dots"  # 包含 # 和 .

encoded_username = quote(username, safe='')
encoded_password = quote(password, safe='')

proxy_url = f"http://{encoded_username}:{encoded_password}@proxyhost:port/"

# 示例输出: http://myuser:pass%23word.with.dots@proxyhost:port/
```

- 使用 `safe=''` 来编码甚至包括 `/` 在内的字符（尽管在凭据中很少见）。
- **不要**对 `:` 或 `@` 分隔符本身进行编码。

### 在 `requests` 库中使用 Proxies

如果使用 proxies：

```python
import requests
from urllib.parse import quote

password = "pass#word.with.dots"
encoded_password = quote(password, safe='')

proxies = {
    "http": f"http://username:{encoded_password}@proxyhost:port/",
    "https": f"http://username:{encoded_password}@proxyhost:port/",
}

response = requests.get("https://example.com", proxies=proxies)
```

许多报告确认，将 `#` 编码为 `%23`，将 `@` 编码为 `%40` 等，可以解决 `requests` proxies 中的解析错误。

### 替代方案：避免在 URL 中嵌入凭据

出于安全和简洁的考虑：

- 如果支持，请为 proxies 使用独立的 auth（例如，`requests` 允许为某些 proxies 提供 `auth` 参数，但对于 HTTP proxies，URL 形式很常见）。
- 或者使用带有编码凭据的环境变量，如 `HTTP_PROXY`。

编码确保了在 host 部分之前，整个凭据字符串被正确处理。

References:

- [https://bugs.python.org/issue18140](https://bugs.python.org/issue18140)
- [https://github.com/python/cpython/issues/62340](https://github.com/python/cpython/issues/62340)
- [https://docs.python.org/3/library/urllib.parse.html](https://docs.python.org/3/library/urllib.parse.html)
- [https://stackoverflow.com/questions/30299973/http-request-through-proxy-in-python-having-in-password](https://stackoverflow.com/questions/30299973/http-request-through-proxy-in-python-having-in-password)
- [https://stackoverflow.com/questions/73034574/how-to-use-password-with-special-character-in-basic-auth](https://stackoverflow.com/questions/73034574/how-to-use-password-with-special-character-in-basic-auth)
