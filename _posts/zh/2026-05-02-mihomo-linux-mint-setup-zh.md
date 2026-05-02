---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Linux Mint上Mihomo的设置与配置
translated: true
type: note
---

## 综合回顾：Linux Mint 22.3 上的 mihomo 配置

### 操作内容

**1. 二进制安装**
- 从 GitHub releases 下载 mihomo v1.19.24 (linux/amd64)
- 安装至 `~/.local/bin/mihomo`（用户空间，无需 sudo）
- 在 `~/.bashrc` 中将 `~/.local/bin` 添加至 `$PATH`

**2. 配置文件**
- 将完整的 `~/.config/mihomo/config.yaml` 从 Mac 复制到 Linux 机器
- 配置包含：SS 代理、Hysteria2 代理、规则集（Global/China/ChinaIP）、20+ 域名规则

**3. Systemd 用户服务**
- 创建 `~/.config/systemd/user/mihomo.service`
- 已启用（用户登录时自动启动）
- 以用户 `xiaoxin` 运行，非 root 权限

**4. 系统代理（Cinnamon 桌面环境）**
- 通过 `gsettings` 配置（通过 SSH 使用 `/run/user/1000/bus` 访问）
- 模式：`manual`，HTTP/HTTPS → `127.0.0.1:7890`

**5. 终端代理**
- 在 `~/.bashrc` 中添加 `http_proxy`、`https_proxy` 等环境变量

---

### 运行正常部分 ✓

| 端口 | 协议 | 状态 |
|------|----------|--------|
| 7890 | HTTP 代理 | ✓ 监听中 |
| 7891 | SOCKS5 代理 | ✓ 监听中 |
| 7892 | 混合代理（HTTP+SOCKS）| ✓ 监听中 |
| 9090 | REST API / 控制面板 | ✓ 监听中 |

---

### 已知问题 / 缺失项

**端口 53 的 DNS — 权限被拒绝**
- 配置设置为 `listen: 0.0.0.0:53`，但非 root 用户无法绑定端口 53
- `fake-ip` 模式失效 — DNS 解析回退到系统解析器
- 修复方案：
  ```bash
  sudo setcap cap_net_bind_service=+ep ~/.local/bin/mihomo
  systemctl --user restart mihomo
  ```
  或将配置改为 `listen: 0.0.0.0:5353` 并用 iptables 重定向

**系统二进制路径需要 sudo**
- 二进制文件位于 `~/.local/bin/` 而非 `/usr/local/bin/`，因为 SSH 非交互环境下无密码时无法执行 sudo
- 后果：仅用户 `xiaoxin` 可访问 `mihomo`，非系统全局可用

**用户服务 vs 系统服务**
- `systemctl --user` 仅在 `xiaoxin` 登录时运行，除非设置 `loginctl enable-linger xiaoxin`
- 未启用 linger 时，mihomo 在 xiaoxin 登出后停止
- 修复方案：
  ```bash
  sudo loginctl enable-linger xiaoxin
  ```

**规则集下载待处理**
- 首次启动时，mihomo 从 `cdn.jsdmirror.cn` 下载 Global/China/ChinaIP 规则集
- 这些下载需要不经过代理的网络访问（先有鸡还是先有蛋问题）— 但由于 CDN 位于中国，DIRECT 策略可正常工作

**`allow-lan: true` 但无防火墙规则**
- Mihomo 监听 `*:7890`（所有网络接口），意味着局域网设备可将其作为代理使用
- 若非本意，需添加防火墙规则：`sudo ufw deny from any to any port 7890 comment "limit mihomo"`

---

### 建议后续操作

```bash
# 1. 启用 linger 使服务在登出后持续运行
sudo loginctl enable-linger xiaoxin

# 2. 修复 DNS 端口 53 绑定
sudo setcap cap_net_bind_service=+ep ~/.local/bin/mihomo
systemctl --user restart mihomo

# 3. 验证代理是否工作
curl -x http://127.0.0.1:7890 https://www.google.com -I
```

---

### 流程问题（元层面）

- 下载耗时约 5 分钟，速度约 45 KB/s — Linux 机器到 GitHub 的连接较慢；下次可考虑使用镜像源
- 非 TTY SSH 会话中的 `sudo` 是常见痛点 — 解决方案：在 sudoers 中为特定命令配置 `NOPASSWD`，或使用 `scp` + 手动 sudo 步骤
- 使用了多个轮询循环而非单个阻塞等待 — 监控方式比理想情况更繁琐