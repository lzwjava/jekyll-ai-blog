---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Camoufox代理下载缓慢问题
translated: true
type: note
---

问题：为什么使用 proxychains4 npx camoufox-js fetch 下载 Camoufox 时进度卡在 0% 并显示剩余 15659.0 秒？如何安装 Hermes？

回答：

您遇到的问题是 Camoufox 下载速度极慢（按当前速度估算约需 4 小时或更久）或完全卡在 0% 进度。使用 **proxychains** 时这种情况很常见，因为：

- Proxychains 强制所有连接通过您的代理（SOCKS/Tor 等），这通常会导致大型二进制文件下载极其缓慢或不稳定。
- 许多 CDN 和下载主机（例如提供 Camoufox 二进制文件的服务商）对代理/Tor 连接的性能表现很差，甚至可能阻断或中止此类连接。
- 进度条由 npx camoufox-js 内的下载器显示，而它未能妥善处理缓慢或不稳定的代理连接。

### 可尝试的快速解决方法（按顺序）：

1. **跳过 proxychains 进行下载**（推荐首选）
   不使用 proxychains 运行命令：
   ```
   npx camoufox-js fetch
   ```
   这样下载将使用您的正常网络连接，通常速度会快得多。

2. 如果出于隐私考虑确实需要使用代理：
   - 尝试在 `/opt/homebrew/etc/proxychains.conf` 中更换为不同/更优的代理
   - 如果当前使用 Tor，可改用速度更快的代理（住宅代理或高带宽代理）
   - 如果支持，可在 proxychains 配置中增加线程/链的数量

3. **安装 Hermes 的替代方法（假设您想通过 Camoufox 安装 Hermes 代理）**

   如果上述方法仍失败，请尝试以下步骤：

   - 取消当前卡住的进程（Ctrl+C）
   - 清除部分下载缓存：
     ```
     rm -rf ~/.cache/camoufox* || true
     rm -rf /tmp/camoufox* || true
     ```
   - 然后在不使用代理的情况下重试：
     ```
     npx camoufox-js fetch
     ```

   成功获取后，继续 Hermes 的安装。通常命令类似于：
   ```
   # Camoufox 获取成功后
   npx camoufox-js install   # 或实际安装 Hermes 的命令
   ```

   如果您正在遵循特定的 Hermes 安装指南，请提供确切的命令或 GitHub 仓库链接以便获得更精确的帮助。

4. **其他常见原因及解决方案**：
   - 磁盘空间不足 → 使用 `df -h` 检查
   - 即使不用代理也有网络问题 → 通过 `curl -I https://example.com` 或测速测试正常速度
   - npx 缓存过旧 → 尝试 `npx --yes camoufox-js fetch` 或清除 npm 缓存：`npm cache clean --force`
   - 防病毒软件/防火墙干扰（macOS 上较罕见）

“15659 秒”（约 4.35 小时）是基于当前下载速度估算的剩余时间。在 0% 进度且预估时间如此长的情况下，通常意味着连接被严重限速或几乎停滞。

**最佳即时措施：**  
取消进程（`Ctrl+C`），从命令中移除 proxychains，然后重新执行 fetch。在正常网络环境下，通常应在几秒或几分钟内完成。

如果仍然失败，请提供：
- 您遵循的 Hermes 安装指南详情
- 您的 proxychains.conf 内容（隐藏敏感部分）
- 最终失败后显示的任何错误信息

这将有助于我提供更具针对性的故障排除建议。