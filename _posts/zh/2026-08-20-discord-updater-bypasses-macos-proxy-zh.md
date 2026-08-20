---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Discord 更新程序绕过 macOS 代理
translated: true
type: note
---

## 摘要

### Discord 检查更新但永远无法完成的根本原因
**Discord 应用更新器**（`.../Discord.app/Contents/Resources/updater.node`，一个 Rust 实现的 `reqwest` 客户端）会对 `https://updates.discord.com/` → `54.89.135.129:443` 进行**原始 TCP 连接**。该客户端**忽略** macOS HTTP/S 代理（`127.0.0.1:7890`）以及 `HTTPS_PROXY` 环境变量。

来自其自身日志（`~/Library/Application Support/discord/logs/Discord_updater_rCURRENT.log`）的证明，每约 75 秒重复一次：
```
ERROR [updater_client]: ... host: updates.discord.com ...
  hyper::Error(Connect, ConnectError("tcp connect error",
  Os { code: 60, kind: TimedOut, message: "Operation timed out" }))
```

实时测试确认了不对称性：
- **通过 mihomo** `127.0.0.1:7890` → ✅ HTTP 200 (0.34s)
- **直连**（`--noproxy '*'`） → ❌ `Connection timed out`

`DOMAIN-SUFFIX,discord.com → Proxy` 规则本身是正确的——但只有在流量**到达** mihomo 时才有效，而由于 mihomo 运行在**代理模式且未启用 TUN**，这种情况并未发生。我的 shell 中的 `curl` 能正常工作，只是因为终端环境携带了 `https_proxy=...`；而从 Finder/Dock 启动的更新器则没有。

### 我采取的措施
1. 备份配置 → `config.yaml.bak.20260820203217`。
2. 在 `~/.config/mihomo/config.yaml` 中添加了一个 `tun:` 块：
   ```yaml
   tun:
     enable: true
     stack: gvisor
     dns-hijack:
       - "any:53"
     auto-route: true
     auto-detect-interface: true
   ```
3. 通过控制器 API（`PUT /configs?force=true`）推送配置重载——每次返回 **HTTP 204**。

### ⚠️ TUN **未激活**
`/configs` 仍报告：
```
tun: {enable: False, stack: gVisor, inet4-address: ['198.18.0.1/30'], ...}
```
关键观察：
- `enable` 保持 `False`。
- `inet4-address` 显示的是**默认**的 `198.18.0.1/30`，而非我在文件中写入的 `.2/30`——因此运行中的实例**并未应用**我的 tun 块（仅部分字段生效）。

### TUN 为何未启动（在操作系统层面被阻止）
你的 mihomo：
- 以普通用户 `lzwjava` 身份运行（无 sudo/root 权限）。
- **未签名**（`code object is not signed at all`）。
- 在 macOS 上，创建/路由 `utun` 接口需要 `com.apple.security.network.tunnel` 授权（或提升的权限）。普通用户且未签名的进程无法做到——因此 TUN 静默保持禁用状态。

### 推荐的后续步骤（由你选择）
1. **最可靠——使用管理管理员 TUN 的 GUI：** 你已安装了 **ClashX Pro**，它为你处理了特权助手/授权，并可持久化配置。使用其配置编辑器（底层仍是 mihomo）并启用 UI 中的“TUN / 增强模式”——它会正确提权并启动接口。鉴于你的现有环境，这是最简洁的修复方式。
2. 通过 `sudo` 手动运行 mihomo（会提示输入密码，TUN 将正常工作），例如 `sudo ~/bin/mihomo...`。权衡：以 root 身份运行，需手动监控。
3. 为二进制文件签名包含隧道授权，并运行一个特权助手来设置接口——更为复杂。

**如果你愿意，我可以撤销对配置的修改**，仅保留代理层修复并采用 ClashX Pro 方案——或帮你设置 `sudo` 启动方式。你倾向哪条路线？