---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于 OpenClaw UI 访问的 SSH 隧道
translated: true
type: note
---

问题：使用 SSH 端口转发命令 `ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36` 时，OpenClaw Control UI 中的复制按钮是否会正常工作？

回答：

是的，使用这个 SSH 隧道设置应该允许完整的 Control UI（包括复制按钮和其他 clipboard 功能）在浏览器中正常工作。

### 为什么这个设置能修复原有的 WebSocket 问题并启用复制功能

- **Origin 变为 localhost（secure context）**
  在本地机器上运行 `ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36` 并保持隧道打开，然后在浏览器中打开 `http://localhost:18789`（或 `http://127.0.0.1:18789`），浏览器会将页面视为来自 **<http://localhost:18789**。>
  OpenClaw gateway 将 `localhost`（127.0.0.1）视为 **loopback / secure context**，即使是纯 HTTP。这会绕过适用于非 loopback / 远程 IP（如您原来的 `http://192.168.1.36:18789` 访问）的多项严格安全检查。

- **自动放宽的关键安全检查**
  - **Origin allowlist（`allowedOrigins`）**：localhost 被隐式允许（loopback 访问无需显式设置 `allowedOrigins`）。
  - **设备身份 / 配对要求**：浏览器将 localhost 视为 secure context → OpenClaw 不再需要 `dangerouslyDisableDeviceAuth: true`。通常“device-required”拒绝（code 1008）会消失。
  - **不安全认证回退**：通常不需要，但如果仍有问题，可以设置 `gateway.controlUi.allowInsecureAuth: true` 作为备用。

- **复制按钮 / clipboard 访问具体说明**
  Control UI 中的复制按钮使用现代 Clipboard API（`navigator.clipboard.writeText()`）。
  该 API 需要 **secure context**（HTTPS 或 localhost/127.0.0.1）。
  通过 `http://192.168.1.36:18789`（非安全、非 loopback）访问会阻塞 clipboard 权限 → 复制按钮失败或显示“unavailable. No GUI detected.”
  通过 SSH 隧道（`http://localhost:18789`）访问提供 secure context → clipboard 正常工作，无需额外浏览器提示或错误。

### 如何正确使用

1. 在本地计算机上打开终端并运行：

   ```bash
   ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
   ```

   - 保持此终端打开（关闭终端隧道会断开）。
   - 可能需要输入密码或使用密钥认证。

2. 在同一本地计算机的浏览器中访问：
   `http://localhost:18789`
   （或 `http://127.0.0.1:18789` — 效果相同）

3. 如果提示登录，请使用 gateway token（通常在 onboarding 过程中显示，或在服务器的 `~/.openclaw/openclaw.json` 中）。

4. Control UI 应完全加载，WebSocket 无中断连接，复制按钮（例如用于 token、命令、日志）正常工作。

### 可选：使其更方便

- 在 `~/.ssh/config` 中添加以下内容以便更容易重连：

  ```
  Host openclaw-tunnel
      HostName 192.168.1.36
      User lzw
      LocalForward 18789 127.0.0.1:18789
  ```

  然后只需运行：`ssh -N openclaw-tunnel`

- 对于持久隧道（自动重连），如果已安装 `autossh`，使用：
  `autossh -M 0 -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`

- 如果仍出现“origin not allowed”（localhost 下罕见）：
  在服务器（192.168.1.36）上运行：

  ```bash
  openclaw config set gateway.controlUi.allowedOrigins '["http://localhost:18789", "http://127.0.0.1:18789"]'
  openclaw gateway restart
  ```

此 SSH 隧道方法是 OpenClaw 文档中官方推荐的用于安全 LAN/远程访问的方式，无需公开暴露端口或设置 HTTPS。

参考资料：

- [https://docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)
- [https://docs.openclaw.ai/gateway/remote](https://docs.openclaw.ai/gateway/remote)
- [https://github.com/openclaw/openclaw/issues/1679](https://github.com/openclaw/openclaw/issues/1679)
- [https://intercom.help/lumadock/en/articles/13548567-openclaw-quickstart-onboarding-over-ssh](https://intercom.help/lumadock/en/articles/13548567-openclaw-quickstart-onboarding-over-ssh)
