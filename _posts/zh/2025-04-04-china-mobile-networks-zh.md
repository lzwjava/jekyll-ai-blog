---
audio: false
generated: true
lang: zh
layout: post
title: 中国移动网络环境下Git操作失败的原因
translated: true
type: note
---

这是在中国使用某些移动网络时的常见问题，特别是对于依赖特定端口和协议的 Git 服务。以下是问题原因及解决方法：

**中国移动网络导致 Git 操作失败的原因：**

* **端口阻塞/限流：**
  * 中国移动网络运营商有时会实施流量整形或端口阻塞，特别是针对 Git 使用的非标准端口（如 SSH 端口 22）。这通常是为了管理网络带宽或出于安全考虑。
  * 即使端口 22 未被完全阻塞，也可能被严重限流，导致连接极慢或超时，表现为 Git 操作"卡住"。
* **DNS 问题：**
  * 虽然您可以访问 GitHub 和 Google 等网站，但 Git 操作依赖通过 DNS 解析特定主机名（如 `github.com`）。如果 DNS 解析缓慢或不可靠，会导致 Git 挂起。
* **数据包丢失/延迟：**
  * 移动网络（特别是用作热点时）相比有线连接可能具有更高的延迟和数据包丢失率。这会干扰 Git 使用的 SSH 连接，导致操作失败。
* **防火墙干扰：**
  * 中国的"防火墙"可能会干扰 SSH 连接，即使这些连接未被明确阻塞。防火墙的深度包检测有时会导致连接不稳定。
* **MTU 问题：**
  * 最大传输单元（MTU）问题可能导致数据传输故障，移动网络的 MTU 值通常小于有线网络。

**在中国移动网络上修复 Git 推送/拉取问题的方法：**

1. **使用 HTTPS 替代 SSH：**
    * Git over HTTPS 使用 443 端口，该端口通常对网络流量开放。这是最可靠的解决方案。
    * 将 Git 远程仓库改为 HTTPS：
        * 打开终端
        * 进入 Git 仓库目录
        * 运行以下命令（将 `your_username` 和 `your_repository` 替换为您的 GitHub 信息）：

            ```bash
            git remote set-url origin https://github.com/your_username/your_repository.git
            ```

    * 如需提供用户名和密码，可使用 git 凭证助手或个人访问令牌。
2. **使用 VPN：**
    * 可靠的 VPN 可以绕过网络限制并提供更稳定的连接。
    * 在进行 Git 操作前连接至中国境外的 VPN 服务器。
    * 请注意 VPN 也可能出现不稳定和速度问题。
3. **配置 SSH 端口（如必须使用 SSH）：**
    * 如需使用 SSH，可尝试配置 Git 使用其他可能未被阻塞的端口（如 443）。
    * 编辑 `~/.ssh/config` 文件：

        ```
        Host github.com
            Hostname ssh.github.com
            Port 443
            User git
        ```

    * 然后将 git 远程 URL 改为使用 ssh.github.com：

        ```bash
        git remote set-url origin git@ssh.github.com:your_username/your_repository.git
        ```

4. **检查 MTU 设置：**
    * 如怀疑 MTU 问题，可尝试减小 MTU 大小。
    * 在 macOS 上可使用 `networksetup` 命令调整 MTU。
    * 但修改 MTU 属于较高级的故障排除步骤，需谨慎操作。
5. **检查 DNS 设置：**
    * 尝试使用公共 DNS 服务器，如 Google DNS（8.8.8.8 和 8.8.4.4）或 Cloudflare DNS（1.1.1.1 和 1.0.0.1）。
    * 可在 macOS 网络偏好设置中配置 DNS。
6. **使用 Git 代理：**
    * 如有代理服务器，可配置 Git 使用代理。
    * 设置 `http.proxy` 和 `https.proxy` Git 配置变量：

        ```bash
        git config --global http.proxy http://proxy_address:proxy_port
        git config --global https.proxy https://proxy_address:proxy_port
        ```

    * 若代理需要认证，可在代理 URL 中包含用户名和密码。
7. **尝试使用基于 Websockets 的 SSH：**
    * 某些工具和服务允许通过 websockets 隧道传输 SSH 流量，在标准 SSH 端口被阻塞时很有用。
    * 这是较高级的技术，需要设置支持 SSH over websockets 的服务器。

**重要注意事项：**

* 移动网络状况可能存在显著差异，在某个地点或时间有效的方法在其他场景可能无效。
* 请注意移动网络服务提供商的服务条款，以及使用 VPN 或其他解决方案可能存在的限制。
* 对大多数用户而言，HTTPS 通常是最佳解决方案。
