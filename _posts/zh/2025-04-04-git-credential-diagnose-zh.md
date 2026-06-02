---
audio: false
generated: true
lang: zh
layout: post
title: Git凭据管理器诊断
translated: true
type: note
---

`git credential-manager diagnose` 的输出现在明确显示存在**网络连接故障**，同时伴有 TLS 证书验证警告。让我们来解析这个错误并找到解决方法：

**关键发现：**

* **网络连接故障：**
  * 诊断测试失败并显示错误：`System.Net.Http.HttpRequestException: nodename nor servname provided, or not known (example.com:443)`。
  * 此错误意味着 Git 凭据管理器无法将主机名 `example.com` 解析为 IP 地址，或者无法连接到该主机的 443 端口。
  * 诊断日志显示，向 `https://example.com` 发起的 HEAD 请求失败。
* **代理干扰（可能原因）：**
  * 环境变量中存在的 `HTTP_PROXY: http://127.0.0.1:7890` 和 `HTTPS_PROXY: http://127.0.0.1:7890` 强烈表明代理是网络连接故障的根本原因。
  * 诊断可以访问 [http://httpforever.com](http://httpforever.com) 但无法访问 [https://example.com](https://example.com) 的事实，表明代理在处理 HTTPS 请求时出现问题。
* **TLS 证书验证已禁用（安全风险）：**
  * 如前所述，TLS 证书验证被禁用，这是一个重大的安全隐患。

**故障排除步骤：**

1. **代理验证：**
    * **测试代理：** 打开网页浏览器，尝试直接访问 `https://example.com`。如果遇到"无法连接"或"未找到主机名"错误，则您的代理很可能配置错误。
    * **代理软件问题：**
        * 重启您的代理软件（Shadowsocks、Clash 等）。
        * 检查代理软件的日志以查找错误信息。
        * 确保代理配置为能正确处理 HTTPS 流量。
        * 确保代理软件正在运行。
    * **代理配置：**
        * 仔细检查您操作系统网络首选项和任何 Git 配置文件中的代理设置。
        * 验证代理地址 (`127.0.0.1`) 和端口 (`7890`) 是否正确。
        * 在您的操作系统网络设置中临时禁用代理，然后重试 `git credential-manager diagnose` 命令。
2. **DNS 解析：**
    * 尽管错误信息提示了主机名解析问题，但代理是最可能的罪魁祸首。不过，检查您的 DNS 设置仍然是值得的。
    * 尝试使用公共 DNS 服务器（例如 8.8.8.8, 1.1.1.1）。
3. **TLS 证书验证：**
    * **重新启用证书验证：** 这对安全至关重要。请遵循 `https://aka.ms/gcm/tlsverify` 链接中提供的说明。
    * 如果您的代理软件旨在拦截 HTTPS 流量，请确保将代理的根证书安装到您操作系统的受信任根证书存储区。这是允许代理工作的安全方法。
4. **Git 配置：**
    * 运行 `git config --global --list` 来检查您的 Git 配置。
    * 临时从 Git 中移除代理设置以隔离问题：

        ```bash
        git config --global --unset http.proxy
        git config --global --unset https.proxy
        ```

    * 移除代理设置后，重新运行 `git credential-manager diagnose` 命令。
5. **防火墙：**
    * 临时禁用计算机上的任何防火墙，以排除防火墙干扰。
6. **网络连接：**
    * 使用其他网络应用程序测试您的网络连接，以确保网络本身稳定。
    * 如果使用移动热点，请移动到信号强度更好的位置。

**关键要点：** 代理几乎肯定导致了网络连接故障。正确配置代理并重新启用 TLS 证书验证是最重要的步骤。
