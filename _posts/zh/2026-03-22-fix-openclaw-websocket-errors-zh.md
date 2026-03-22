---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw WebSocket 连接错误
translated: true
type: note
---

**问题：** 如何修复 OpenClaw gateway 中的 WebSocket 连接错误 “ws://192.168.1.36:18789/” failed: WebSocket is closed before the connection is established？

**回答：**

此错误通常表示 WebSocket 握手已启动，但服务器立即拒绝并关闭它（通常使用代码 1008）。这**不是**因为在本地 LAN 上使用 `ws://`（HTTP）而不是 `wss://`（HTTPS）导致的——在大多数情况下，纯 HTTP + ws:// 可以正常工作。

根本原因几乎总是以下服务器端检查失败之一（或两者）：

1. **Origin not allowed** — 浏览器中的 `Origin` 标头不符合允许列表  
2. **Device identity required** — 即使对于 Control UI，gateway 也会强制执行设备配对/身份验证，除非明确禁用

### 快速修复步骤（LAN / HTTP 设置）

1. **检查当前配置**  
   运行此命令（如果您的 CLI 路径不同，请调整）：

   ```
   openclaw config get gateway.controlUi
   ```

   查找：
   - `allowedOrigins`：应包含您确切的浏览器 URL，例如 `["http://192.168.1.36:18789"]`  
     （无尾随斜杠，确切协议 + IP + 端口）
   - `dangerouslyDisableDeviceAuth`：应为 `true`

   如果任一项缺失或错误 → 这就是问题所在。

2. **设置正确值**

   ```bash
   # 设置浏览器中使用的确切 origin
   openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'

   # 禁用设备身份检查（非安全上下文/非回环浏览器访问需要）
   openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true

   # 可选，但对于纯 HTTP 通常有帮助：
   openclaw config set gateway.controlUi.allowInsecureAuth true
   ```

   **`allowedOrigins` 的重要说明：**
   - 必须**完全匹配**浏览器地址栏中显示的内容（协议 + 主机 + 端口）。
   - **不要**使用 `["*"]`，除非这是临时测试机器——这会带来很大的安全风险。
   - 如果您通过 `http://localhost:18789` 或其他主机名访问，也添加它：`["http://192.168.1.36:18789", "http://localhost:18789"]`

3. **重启 gateway** 以使更改生效

   ```bash
   openclaw gateway restart
   ```

   或如果使用 systemd：

   ```bash
   systemctl --user restart openclaw-gateway.service
   ```

4. **检查 gateway 日志以获取真实拒绝原因**

   ```bash
   journalctl --user -u openclaw-gateway.service -n 80 --no-pager
   ```

   查找包含以下内容的行：
   - `origin not allowed`
   - `device-required`
   - `code=1008`
   - `reason=`

   这将确切告诉您哪个检查失败了。

### HTTPS / wss:// 替代方案（更安全的长期方案）

- 如果使用 HTTPS，您可以完全避免 `dangerouslyDisableDeviceAuth`，因为浏览器将 HTTPS 页面视为安全上下文 → 设备身份可以通过其他机制处理。
- 但在 LAN 上，您需要：
  - 自签名证书（浏览器显示警告；您必须手动信任它 → 繁琐）
  - 或更好：使用反向代理（Caddy / Nginx）+ 本地 DNS（例如 `openclaw.lan`）+ 自签名或 mkcert 证书
- 大多数用户为简单 LAN 访问保留 HTTP + 上述两个配置设置。

### 常见陷阱

- 配置键**区分大小写**且正确嵌套（`gateway.controlUi.…`）
- 更改在 gateway 重启前不会生效
- 如果您最近更新了 OpenClaw，有些版本有 bug，导致 `dangerouslyDisableDeviceAuth` 被忽略 → 检查您的版本并考虑降级/升级
- 确保在普通浏览器标签页中打开 UI（不是 iframe / 嵌入式）

应用配置 + 重启后，刷新 Control UI 页面 — WebSocket 应该能连接。

**参考资料：**  

- [https://docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)
- [https://github.com/openclaw/openclaw/issues/41043](https://github.com/openclaw/openclaw/issues/41043)
- [https://github.com/openclaw/openclaw/issues/44485](https://github.com/openclaw/openclaw/issues/44485)
- [https://docs.openclaw.ai/web/control-ui](https://docs.openclaw.ai/web/control-ui)