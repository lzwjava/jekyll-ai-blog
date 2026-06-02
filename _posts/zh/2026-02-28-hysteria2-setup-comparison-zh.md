---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hysteria2 设置与对比指南
translated: true
type: note
---

**Hysteria** 是一种基于 QUIC 的快速代理协议，专为在丢包网络和高强度审查环境中提供高性能而设计。主要有两个版本：原始的 **Hysteria 1.x**（通常简称为“Hysteria”）和 **Hysteria 2**（现代推荐版本）。

截至 2026 年，**Hysteria 2** 是积极维护的版本，具有更好的协议设计、改进的伪装为 HTTP/3，以及整体更优的性能和抗性。**Hysteria 1** 被视为遗留版本。

### 在 Ubuntu 服务器上安装 Hysteria 2（推荐）

官方一键安装脚本是 Ubuntu（适用于 20.04、22.04、24.04 等）上最简单且最可靠的方法。

1. **运行安装脚本**（安装最新版本，设置 systemd 服务）：

   ```bash
   bash <(curl -fsSL https://get.hy2.sh/)
   ```

   - 这会下载二进制文件，创建 `/etc/hysteria/config.yaml`，并设置 `hysteria-server.service`。

2. **编辑配置文件**：

   ```bash
   nano /etc/hysteria/config.yaml
   ```

   最小工作示例（替换值）：

   ```yaml
   listen: :443   # UDP port (usually 443)

   acme:
     domains:
       - your-domain.com
     email: your@email.com

   auth:
     type: password
     password: your-strong-password-here

   masquerade:
     type: proxy
     proxy:
       url: https://news.ycombinator.com/
       rewriteHost: true
   ```

   - 对于自签名证书或手动证书，使用 `tls` 部分代替 `acme`。
   - 完整配置选项 → 官方文档。

3. **启动并启用服务**：

   ```bash
   systemctl daemon-reload
   systemctl enable --now hysteria-server
   ```

4. **检查状态和日志**：

   ```bash
   systemctl status hysteria-server
   journalctl -u hysteria-server -ef
   ```

5. **防火墙**（如果使用 ufw）：

   ```bash
   ufw allow 443/udp
   ```

6. **后续更新** → 只需重新运行相同的安装命令。

**注意**：如果 GitHub 被屏蔽，从 <https://github.com/apernet/hysteria/releases> 手动下载二进制文件，并使用：

```bash
bash <(curl -fsSL https://get.hy2.sh/) --local /path/to/hysteria-linux-amd64
```

### 安装原始 Hysteria 1.x（遗留版 – 不推荐）

如果特别需要与旧客户端兼容，使用旧仓库/脚本：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/apernet/hysteria/master/scripts/install_server.sh)
```

但在 2026 年强烈不推荐 — 请切换到 Hysteria 2。

### Hysteria 1 与 Hysteria 2 比较

| 特性 / 方面                    | Hysteria 1.x (遗留版)                  | Hysteria 2 (当前版)                              |
|-------------------------------|----------------------------------------|---------------------------------------------------|
| **协议**                      | 自定义 QUIC + 自有混淆                | 重新设计的基于 QUIC，伪装为真实的 **HTTP/3**     |
| **审查抗性**                  | 良好                                   | 显著更好（看起来像正常的 HTTP/3 流量）           |
| **拥塞控制**                  | 自定义（非常激进）                     | **Brutal**（自定义）+ BBR 支持，更稳定            |
| **性能**                      | 在丢包网络上出色                       | 通常更好/更快 + 更一致                           |
| **兼容性**                    | 仅与 Hysteria 1 客户端                 | 仅与 Hysteria 2 客户端（不向后兼容）              |
| **代码库**                    | 较旧，维护较少                         | 几乎完全重写，积极开发                           |
| **伪装**                      | 基本 HTTP 代理伪装                     | 更高级（proxy、files、string 等）                |
| **v2 中缺失**                 | —                                      | 无客户端侧 ACL（暂无）、无 FakeTCP（小众）        |
| **2026 年推荐**               | 新部署避免使用                         | **强烈推荐** 用于所有新部署                      |

**总结**：除非有特定原因留在 1.x（例如旧客户端兼容），否则使用 **Hysteria 2**。它提供更好的速度、更强的审查抗性，并且是面向未来的选择。

参考资料：

- [Hysteria 2 官方安装](https://v2.hysteria.network/docs/getting-started/Installation)
- [Hysteria 2 服务器安装脚本](https://v2.hysteria.network/docs/getting-started/Server-Installation-Script)
- [Hysteria 2 与 Hysteria 1 比较](https://v2.hysteria.network/docs/misc/2-vs-1)
