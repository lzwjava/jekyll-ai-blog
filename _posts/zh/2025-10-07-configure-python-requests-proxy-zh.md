---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 通过.env文件配置Python请求代理
translated: true
type: note
---

### 使用 `.env` 文件为 Python Requests 设置 HTTP/HTTPS 代理

Python 中的 `requests` 库会自动遵循标准环境变量（如 `HTTP_PROXY` 和 `HTTPS_PROXY`）进行代理配置。为了安全地管理这些变量（例如，避免在代码中硬编码），你可以将它们存储在 `.env` 文件中，并使用 `python-dotenv` 库加载。这样可以将敏感的代理信息与代码分离。

#### 步骤 1：安装必要的包

你需要安装 `requests`（如果尚未安装）和 `python-dotenv` 来加载 `.env` 文件。

```bash
pip install requests python-dotenv
```

#### 步骤 2：创建 `.env` 文件

在项目根目录下创建一个名为 `.env`（无扩展名）的文件，并添加你的代理设置。代理 URL 使用 `http://` 或 `https://` 格式，如果需要，包含用户名和密码。

示例 `.env` 内容：

```
HTTP_PROXY=http://username:password@proxy-host:port
HTTPS_PROXY=https://username:password@proxy-host:port
NO_PROXY=localhost,127.0.0.1,example.com  # 可选：绕过代理的域名列表
```

- `HTTP_PROXY`：用于 HTTP 流量。
- `HTTPS_PROXY`：用于 HTTPS 流量（通常与 HTTP_PROXY 相同）。
- `NO_PROXY`：逗号分隔的主机/IP 列表，这些地址将绕过代理。
- 注意：环境变量不区分大小写，但通常使用大写形式。

将 `.env` 添加到 `.gitignore` 中，以避免提交敏感信息。

#### 步骤 3：在 Python 脚本中加载 `.env` 文件

在脚本的开头加载环境变量：

```python
from dotenv import load_dotenv
import requests

# 从 .env 文件加载变量
load_dotenv()  # 默认在当前目录中查找 .env 文件

# 现在发起请求 – 代理会自动应用
response = requests.get('https://httpbin.org/ip')
print(response.json())
```

- `load_dotenv()` 读取 `.env` 文件并将变量设置到 `os.environ` 中。
- `requests` 会自动检测 `HTTP_PROXY`/`HTTPS_PROXY`，无需传递 `proxies` 字典，除非需要覆盖。

#### 步骤 4：验证代理使用（可选）

为了确认代理正常工作，可以使用 httpbin.org 等服务进行测试：

```python
import requests
from dotenv import load_dotenv

load_dotenv()

proxies = requests.utils.get_environ_proxies('https://httpbin.org/ip')  # 检查加载的代理
print("已加载的代理:", proxies)

response = requests.get('https://httpbin.org/ip')
print("通过代理访问的 IP:", response.json())
```

如果配置正确，这里应该显示代理服务器的 IP。

#### 常见问题与技巧

- **代理认证**：如果代理需要认证，请在 URL 中包含 `username:password@`。
- **SOCKS 代理**：使用 `socks5://` 前缀（需要安装 `requests[socks]` 扩展：`pip install requests[socks]`）。
- **按请求覆盖**：如果某个特定调用需要使用不同的代理，可以传递一个字典：

  ```python:disable-run
  proxies = {'http': 'http://custom-proxy:port', 'https': 'https://custom-proxy:port'}
  response = requests.get('url', proxies=proxies)
  ```

- **环境兼容性**：适用于 Windows/Linux/macOS。在 Windows 上，可以在 cmd 或 PowerShell 中使用 `set` 命令设置环境变量。
- **安全性**：切勿将 `.env` 文件提交到版本控制系统中。

这种设置简单、安全，并遵循基于环境变量的配置最佳实践。

[Requests 文档：代理](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)
[python-dotenv 文档](https://github.com/theskumar/python-dotenv)
