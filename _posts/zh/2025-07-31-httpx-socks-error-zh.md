---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理方案不受支持
translated: true
type: note
---

错误信息表明，在您的 `gitmessageai.py` 脚本中，`openai` 客户端使用的 `httpx` 库正尝试配置一个代理，其 URL 为 `socks://127.0.0.1:7891/`，但该代理方案 `socks` 不被支持或识别，导致了 `ValueError: Unknown scheme for proxy URL`。这表明某个来自您的环境或代码的代理配置正在生效，并且它使用了一个不受支持的 SOCKS 代理方案。

让我们来分析代理可能来自哪里以及如何修复它。

### 代理配置来自何处？

代理配置 (`socks://127.0.0.1:7891/`) 很可能来自以下某个地方：

1. **环境变量**
    - `httpx` 库会自动检查环境变量中的代理设置，例如 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY` 或它们的小写形式 (`http_proxy`, `https_proxy`, `all_proxy`)。
    - 像 `socks://127.0.0.1:7891/` 这样的值表明一个 SOCKS 代理（常用于 Shadowsocks 或 VPN 等工具）被设置在了这些变量之一中。
    - 要检查这些变量是否已设置，请在您的终端中运行：

      ```bash
      env | grep -i proxy
      ```

      查找类似 `HTTP_PROXY=socks://127.0.0.1:7891` 或 `HTTPS_PROXY=socks://127.0.0.1:7891` 的变量。

2. **系统级代理设置**
    - 如果您使用的是 Linux 系统，代理设置可能是在全局配置的（例如，在 `/etc/environment`、`/etc/profile` 或您的 shell 配置文件如 `~/.bashrc`、`~/.zshrc` 或 `~/.profile` 中）。
    - 检查这些文件中是否有如下行：

      ```bash
      export HTTP_PROXY="socks://127.0.0.1:7891"
      export HTTPS_PROXY="socks://127.0.0.1:7891"
      ```

    - 您可以使用以下命令查看这些文件：

      ```bash
      cat ~/.bashrc | grep -i proxy
      cat ~/.zshrc | grep -i proxy
      cat /etc/environment | grep -i proxy
      ```

3. **代理工具中的代理配置**
    - 地址 `127.0.0.1:7891` 通常被代理或 VPN 工具使用，如 Shadowsocks、V2Ray 或 Clash，这些工具通常默认在 7890 或 7891 等端口上使用 SOCKS5 代理。
    - 如果您安装或配置了此类工具，它可能自动设置了环境变量或系统代理设置。

4. **代码中显式设置的代理**
    - 虽然可能性较小，但您的 `gitmessageai.py` 脚本或其使用的某个库可能显式地配置了代理。由于错误发生在 `httpx` 中，请检查您的脚本是否向 `OpenAI` 客户端或 `httpx` 客户端传递了代理。
    - 在您的脚本中搜索诸如 `proxy`、`proxies` 或 `httpx.Client` 等术语：

      ```bash
      grep -r -i proxy /home/lzwjava/bin/gitmessageai.py
      ```

5. **Python 库配置**
    - 一些 Python 库（例如 `requests` 或 `httpx`）可能会从配置文件或之前的设置中继承代理配置。然而，`httpx` 主要依赖于环境变量或显式代码。

### 为什么 `socks://` 会导致问题？

- `httpx` 库（被 `openai` 使用）本身不支持 `socks` 方案（SOCKS4/SOCKS5 代理），除非安装了额外的依赖项如 `httpx-socks`。
- 发生错误 `Unknown scheme for proxy URL` 是因为 `httpx` 期望的代理方案是 `http://` 或 `https://`，而不是 `socks://`。

### 如何修复此问题

您有两个选择：如果不需要代理，则**移除或绕过代理**；如果打算使用该代理，则**支持 SOCKS 代理**。

#### 选项 1：移除或绕过代理

如果您不需要为 DeepSeek API 使用代理，可以禁用或绕过代理配置。

1. **取消设置环境变量**
    - 如果代理是在环境变量中设置的，请为当前会话取消设置它们：

      ```bash
      unset HTTP_PROXY
      unset HTTPS_PROXY
      unset ALL_PROXY
      unset http_proxy
      unset https_proxy
      unset all_proxy
      ```

    - 要永久生效，请从 `~/.bashrc`、`~/.zshrc`、`/etc/environment` 或其他 shell 配置文件中移除相应的 `export` 行。

2. **在不使用代理的情况下运行脚本**
    - 临时在没有代理设置的情况下运行您的脚本：

      ```bash
      HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python3 /home/lzwjava/bin/gitmessageai.py
      ```

    - 如果这样能正常工作，那么问题就出在代理上。

3. **在代码中绕过代理**
    - 修改您的 `gitmessageai.py` 脚本，在 `OpenAI` 客户端中显式禁用代理：

      ```python
      from openai import OpenAI
      import httpx

      def call_deepseek_api(prompt):
          api_key = os.getenv("DEEPSEEK_API_KEY")
          if not api_key:
              raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
          client = OpenAI(
              api_key=api_key,
              base_url="https://api.deepseek.com",
              http_client=httpx.Client(proxies=None)  # 禁用代理
          )
          # 您的 API 调用逻辑在这里
          response = client.chat.completions.create(
              model="deepseek",  # 替换为正确的模型
              messages=[{"role": "user", "content": prompt}]
          )
          return response.choices[0].message.content
      ```

    - 设置 `proxies=None` 可确保 `httpx` 忽略任何环境代理设置。

#### 选项 2：支持 SOCKS 代理

如果您需要使用 SOCKS 代理（例如，为了通过 VPN 或代理服务器访问 DeepSeek API），则必须为 `httpx` 添加 SOCKS 支持。

1. **安装 `httpx-socks`**
    - 安装 `httpx-socks` 包以启用 SOCKS4/SOCKS5 代理支持：

      ```bash
      pip install httpx-socks
      ```

    - 这将扩展 `httpx` 以处理 `socks://` 和 `socks5://` 方案。

2. **更新您的代码**
    - 修改您的脚本以显式使用 SOCKS 代理：

      ```python
      from openai import OpenAI
      import httpx
      from httpx_socks import SyncProxyTransport

      def call_deepseek_api(prompt):
          api_key = os.getenv("DEEPSEEK_API_KEY")
          if not api_key:
              raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
          # 配置 SOCKS5 代理
          proxy_transport = SyncProxyTransport.from_url("socks5://127.0.0.1:7891")
          client = OpenAI(
              api_key=api_key,
              base_url="https://api.deepseek.com",
              http_client=httpx.Client(transport=proxy_transport)
          )
          # 您的 API 调用逻辑在这里
          response = client.chat.completions.create(
              model="deepseek",  # 替换为正确的模型
              messages=[{"role": "user", "content": prompt}]
          )
          return response.choices[0].message.content
      ```

    - 如果您的代理使用 SOCKS4，请将 `socks5://` 替换为 `socks4://`。

3. **验证代理服务器**
    - 确保 `127.0.0.1:7891` 上的代理服务器正在运行。如果您正在使用像 Clash 或 Shadowsocks 这样的工具，请检查其状态：

      ```bash
      netstat -tuln | grep 7891
      ```

    - 如果没有进程在监听 7891 端口，请启动您的代理工具或在代理 URL 中更正端口。

### 额外的调试步骤

- **检查代理工具配置**
  - 如果您正在使用像 Clash 或 Shadowsocks 这样的代理工具，请验证其配置文件（例如 `~/.config/clash/config.yaml`），确认它设置为对 SOCKS5 使用 `127.0.0.1:7891`。
  - 确保该工具正在运行且可访问。

- **测试代理连接性**
  - 使用像 `curl` 这样的工具测试代理（需要 `curl` 支持 SOCKS）：

      ```bash
      curl --socks5 127.0.0.1:7891 https://api.deepseek.com
      ```

  - 如果此操作失败，则代理服务器要么已关闭，要么配置错误。

- **记录代理使用情况**
  - 在您的脚本中添加日志记录以确认正在使用哪个代理：

      ```python
      import logging
      logging.basicConfig(level=logging.DEBUG)
      ```

### 推荐的修复方法

如果您不需要代理，最简单的修复方法是取消设置环境变量并运行：

```bash
HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python3 /home/lzwjava/bin/gitmessageai.py
```

如果您需要代理，请安装 `httpx-socks` 并按照上述方法更新您的代码以使用 `SyncProxyTransport`。

### 参考资料

- [httpx 文档](https://www.python-httpx.org/advanced/#proxy-support)
- [httpx-socks GitHub](https://github.com/romis2012/httpx-socks)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
