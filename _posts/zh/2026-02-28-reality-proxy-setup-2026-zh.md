---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 现实代理设置指南 2026
translated: true
type: note
---

仓库 **flq367/reality** 提供了一个简单的“一键安装”脚本，用于设置 **Reality**（通常指 Xray-core 中的 VLESS + XTLS-Reality 协议），常用于创建抗审查代理。

### 安装步骤

1. **连接到您的服务器**  
   使用 SSH 访问您的 Linux 服务器（Ubuntu/Debian、CentOS 或 Alpine 是此类脚本的常见选择）。

2. **运行一键安装命令**  
   以 root 用户身份执行此命令（或使用 `sudo`）：

   ```bash
   bash <(curl -sL https://raw.githubusercontent.com/flq367/reality/main/r.sh)
   ```

   - 这会下载并立即运行脚本 `r.sh`。
   - 该脚本通常处理：
     - 安装所需依赖
     - 下载预构建的 Xray-core 二进制文件（带 Reality 支持）
     - 生成密钥和证书
     - 创建基本的服务器配置
     - 设置 systemd 服务（或等效服务）以自动运行

3. **安装过程中**  
   该脚本在大多数类似 Reality 安装程序中是交互式的。您可能会被要求：
   - 选择端口（默认通常为 443）
   - 输入域名 / SNI / serverName（用于 Reality 伪装）
   - 选择回退目标网站（例如 www.microsoft.com:443）
   - 生成或输入 Reality 的公钥/私钥
   - 选择是否启用 uTLS 指纹等。

   仔细遵循屏幕提示。

4. **安装完成后**  
   - 脚本通常会显示：
     - 服务器配置摘要
     - VLESS Reality URL / 分享链接（用于 v2rayN、Nekobox、Hiddify 等客户端）
     - 如果安装了面板，可能还有登录信息
   - 立即保存 VLESS 链接——它通常类似于：  
     `vless://uuid@your-server-ip:443?security=reality&...`

5. **安装后的常见位置**  
   - 配置文件：通常为 `/usr/local/etc/xray/config.json` 或 `/etc/xray/config.json`
   - 二进制文件：`/usr/local/bin/xray`
   - 服务：`systemctl status xray`（或类似名称）

6. **测试与管理**  
   - 检查状态：`systemctl status xray`（或显示的服务名称）
   - 重启：`systemctl restart xray`
   - 查看日志：`journalctl -u xray -ef` 或检查 `/var/log/xray/`

### 重要说明与要求
- 使用 **clean IP**（之前未用于代理的 IP）—— Reality 在未污染的 IP 上效果最佳。
- 强烈推荐使用端口 443（模拟 HTTPS 流量）。
- 通常需要一个指向服务器 IP 的域名以获得最佳效果（但短域名 Reality 设置也是可能的）。
- 该脚本最近一次显著更新大约在 2025 年初——验证它在 2026 年是否仍有效。
- 如果脚本失败 → 请尝试在全新的 Ubuntu 22.04 / 24.04 或 Debian 12 服务器上运行。

### 如果脚本无效或您想要替代方案
2026 年的热门维护选项包括：
- Hiddify-Manager（面板 + Reality 支持）
- 3X-UI 面板
- AmneziaVPN 自托管安装程序
- 各种一键 Xray-Reality 脚本（搜索 "xray reality one key install 2026"）

References:  

- [https://github.com/flq367/reality](https://github.com/flq367/reality)