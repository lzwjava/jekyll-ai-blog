---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proxy Scheme Not Supported
translated: false
type: note
---

The error indicates that the `httpx` library, used by the `openai` client in your `gitmessageai.py` script, is attempting to configure a proxy with the URL `socks://127.0.0.1:7891/`, but the scheme `socks` is not supported or recognized, resulting in a `ValueError: Unknown scheme for proxy URL`. This suggests that a proxy configuration is being picked up from your environment or code, and it’s using an unsupported SOCKS proxy scheme.

Let’s break down where the proxy might come from and how to fix it.

### Where Is the Proxy Coming From?

The proxy configuration (`socks://127.0.0.1:7891/`) is likely being sourced from one of the following places:

1. **Environment Variables**
   - The `httpx` library automatically checks for proxy settings in environment variables like `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, or their lowercase equivalents (`http_proxy`, `https_proxy`, `all_proxy`).
   - A value like `socks://127.0.0.1:7891/` suggests a SOCKS proxy (common for tools like Shadowsocks or VPNs) was set in one of these variables.
   - To check if these variables are set, run the following in your terminal:
     ```bash
     env | grep -i proxy
     ```
     Look for variables like `HTTP_PROXY=socks://127.0.0.1:7891` or `HTTPS_PROXY=socks://127.0.0.1:7891`.

2. **System-Wide Proxy Settings**
   - If you’re using a Linux system, proxy settings might be configured globally (e.g., in `/etc/environment`, `/etc/profile`, or your shell configuration like `~/.bashrc`, `~/.zshrc`, or `~/.profile`).
   - Check these files for lines like:
     ```bash
     export HTTP_PROXY="socks://127.0.0.1:7891"
     export HTTPS_PROXY="socks://127.0.0.1:7891"
     ```
   - You can view these files with:
     ```bash
     cat ~/.bashrc | grep -i proxy
     cat ~/.zshrc | grep -i proxy
     cat /etc/environment | grep -i proxy
     ```

3. **Proxy Configuration in a Proxy Tool**
   - The address `127.0.0.1:7891` is commonly used by proxy or VPN tools like Shadowsocks, V2Ray, or Clash, which often default to SOCKS5 proxies on ports like 7890 or 7891.
   - If you’ve installed or configured such a tool, it might have automatically set environment variables or system proxy settings.

4. **Explicit Proxy in Code**
   - Though less likely, your `gitmessageai.py` script or a library it uses might be explicitly configuring a proxy. Since the error occurs in `httpx`, check if your script passes a proxy to the `OpenAI` client or `httpx` client.
   - Search your script for terms like `proxy`, `proxies`, or `httpx.Client`:
     ```bash
     grep -r -i proxy /home/lzwjava/bin/gitmessageai.py
     ```

5. **Python Library Configuration**
   - Some Python libraries (e.g., `requests` or `httpx`) might inherit proxy settings from a configuration file or a previous setup. However, `httpx` primarily relies on environment variables or explicit code.

### Why Is `socks://` Causing an Issue?

- The `httpx` library (used by `openai`) does not natively support the `socks` scheme (SOCKS4/SOCKS5 proxies) unless additional dependencies like `httpx-socks` are installed.
- The error `Unknown scheme for proxy URL` occurs because `httpx` expects proxies with schemes like `http://` or `https://`, not `socks://`.

### How to Fix the Issue

You have two options: **remove or bypass the proxy** if it’s not needed, or **support the SOCKS proxy** if you intend to use it.

#### Option 1: Remove or Bypass the Proxy

If you don’t need a proxy for the DeepSeek API, you can disable or bypass the proxy configuration.

1. **Unset Environment Variables**
   - If the proxy is set in environment variables, unset them for your session:
     ```bash
     unset HTTP_PROXY
     unset HTTPS_PROXY
     unset ALL_PROXY
     unset http_proxy
     unset https_proxy
     unset all_proxy
     ```
   - To make this permanent, remove the corresponding `export` lines from `~/.bashrc`, `~/.zshrc`, `/etc/environment`, or other shell configuration files.

2. **Run Script Without Proxy**
   - Temporarily run your script without proxy settings:
     ```bash
     HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python3 /home/lzwjava/bin/gitmessageai.py
     ```
   - If this works, the proxy was the issue.

3. **Bypass Proxy in Code**
   - Modify your `gitmessageai.py` script to explicitly disable proxies in the `OpenAI` client:
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
             http_client=httpx.Client(proxies=None)  # Disable proxies
         )
         # Your API call logic here
         response = client.chat.completions.create(
             model="deepseek",  # Replace with correct model
             messages=[{"role": "user", "content": prompt}]
         )
         return response.choices[0].message.content
     ```
   - Setting `proxies=None` ensures `httpx` ignores any environment proxy settings.

#### Option 2: Support the SOCKS Proxy

If you need to use the SOCKS proxy (e.g., for accessing the DeepSeek API through a VPN or proxy server), you must add SOCKS support to `httpx`.

1. **Install `httpx-socks`**
   - Install the `httpx-socks` package to enable SOCKS4/SOCKS5 proxy support:
     ```bash
     pip install httpx-socks
     ```
   - This extends `httpx` to handle `socks://` and `socks5://` schemes.

2. **Update Your Code**
   - Modify your script to use the SOCKS proxy explicitly:
     ```python
     from openai import OpenAI
     import httpx
     from httpx_socks import SyncProxyTransport

     def call_deepseek_api(prompt):
         api_key = os.getenv("DEEPSEEK_API_KEY")
         if not api_key:
             raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
         # Configure SOCKS5 proxy
         proxy_transport = SyncProxyTransport.from_url("socks5://127.0.0.1:7891")
         client = OpenAI(
             api_key=api_key,
             base_url="https://api.deepseek.com",
             http_client=httpx.Client(transport=proxy_transport)
         )
         # Your API call logic here
         response = client.chat.completions.create(
             model="deepseek",  # Replace with correct model
             messages=[{"role": "user", "content": prompt}]
         )
         return response.choices[0].message.content
     ```
   - Replace `socks5://` with `socks4://` if your proxy uses SOCKS4.

3. **Verify Proxy Server**
   - Ensure the proxy server at `127.0.0.1:7891` is running. If you’re using a tool like Clash or Shadowsocks, check its status:
     ```bash
     netstat -tuln | grep 7891
     ```
   - If no process is listening on port 7891, start your proxy tool or correct the port in the proxy URL.

### Additional Debugging Steps

- **Check Proxy Tool Configuration**
  - If you’re using a proxy tool like Clash or Shadowsocks, verify its configuration file (e.g., `~/.config/clash/config.yaml`) to confirm it’s set to use `127.0.0.1:7891` for SOCKS5.
  - Ensure the tool is running and accessible.

- **Test Proxy Connectivity**
  - Test the proxy with a tool like `curl` (requires `curl` built with SOCKS support):
    ```bash
    curl --socks5 127.0.0.1:7891 https://api.deepseek.com
    ```
  - If this fails, the proxy server is either down or misconfigured.

- **Log Proxy Usage**
  - Add logging to your script to confirm which proxy is being used:
    ```python
    import logging
    logging.basicConfig(level=logging.DEBUG)
    ```

### Recommended Fix

If you don’t need the proxy, the simplest fix is to disable it by unsetting environment variables and running:
```bash
HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= python3 /home/lzwjava/bin/gitmessageai.py
```

If you need the proxy, install `httpx-socks` and update your code to use `SyncProxyTransport` as shown above.

### References
- [httpx Documentation](https://www.python-httpx.org/advanced/#proxy-support)
- [httpx-socks GitHub](https://github.com/romis2012/httpx-socks)
- [DeepSeek API Documentation](https://platform.deepseek.com/docs)
