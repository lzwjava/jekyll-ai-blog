---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上持久运行 Mihomo
translated: true
type: note
---

问题：如何在 macOS 中添加服务以保持 mihomo-darwin-amd64-v1-alpha-3035ae8 始终运行？

回答： 

要在 macOS 上让 **mihomo** (Clash Meta core) 作为后台服务自动运行，并在崩溃时保持重启，请使用 **launchd** (macOS 内置的服务管理器)。

推荐方式是创建 **LaunchDaemon**（系统级服务，以 root 身份运行 — 通常用于 TUN mode / enhanced-mode / system proxy 功能）。

### 逐步指南

1. **准备二进制文件和配置文件**
   - 为简单起见，将二进制文件重命名为 `mihomo`（可选，但更整洁）：
     ```
     mv mihomo-darwin-amd64-v1-alpha-3035ae8 mihomo
     chmod +x mihomo
     ```
   - 移动到标准位置：
     ```
     sudo mkdir -p /usr/local/bin
     sudo mv mihomo /usr/local/bin/mihomo
     ```
   - 将配置文件放到合适位置，例如：
     ```
     mkdir -p ~/.config/mihomo
     mv config.yaml ~/.config/mihomo/config.yaml
     ```
     （也可以使用 `/etc/mihomo/config.yaml` 或 `/usr/local/etc/mihomo/config.yaml`）

2. **创建 plist 文件**

   使用 sudo 创建此文件（因为 LaunchDaemons 必须位于系统目录）：

   ```bash
   sudo nano /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   粘贴以下内容（根据需要调整路径）：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.metacubex.mihomo</string>

       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/mihomo</string>
           <string>-d</string>
           <string>/Users/yourusername/.config/mihomo</string>
           <!-- Optional: add more flags if needed, e.g. -->
           <!-- <string>--log-level</string> -->
           <!-- <string>info</string> -->
       </array>

       <key>RunAtLoad</key>
       <true/>

       <key>KeepAlive</key>
       <true/>

       <key>StandardOutPath</key>
       <string>/var/log/mihomo.log</string>

       <key>StandardErrorPath</key>
       <string>/var/log/mihomo.log</string>

       <!-- Optional: lower priority if you want -->
       <!-- <key>Nice</key> -->
       <!-- <integer>10</integer> -->

       <!-- Optional: only start after network is up -->
       <!-- <key>WatchPaths</key> -->
       <!-- <array> -->
       <!--     <string>/Library/Preferences/SystemConfiguration</string> -->
       <!-- </array> -->
   </dict>
   </plist>
   ```

   重要说明：
   - 将 `/Users/yourusername/.config/mihomo` 替换为您的实际配置文件目录
   - `-d` 告诉 mihomo 配置文件夹的位置（它会在里面查找 `config.yaml`）
   - `KeepAlive` 使 launchd 在 mihomo 退出时自动重启它

3. **检查语法**

   ```bash
   sudo plutil -lint /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   应该显示：`/Library/LaunchDaemons/com.metacubex.mihomo.plist: OK`

4. **加载并启动服务**

   ```bash
   sudo launchctl load -w /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   `-w` 使其在每次开机时自动启动。

5. **检查状态**

   ```bash
   sudo launchctl list | grep mihomo
   ```

   或查看日志：

   ```bash
   tail -f /var/log/mihomo.log
   ```

6. **停止 / 卸载（如果需要）**

   ```bash
   sudo launchctl unload /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   或临时停止而不卸载：

   ```bash
   sudo launchctl stop com.metacubex.mihomo
   ```

### 替代方案：更简单的用户级服务 (LaunchAgent)

如果您**不需要** TUN mode 或 root 权限：

- 将 plist 放入 `~/Library/LaunchAgents/com.metacubex.mihomo.plist`（无需 sudo）
- 从 launchctl 命令中移除 `sudo`
- 仅在您登录后运行

但对于大多数 mihomo 用例（尤其是 TUN / 全系统代理），请使用 LaunchDaemon + root。

### 提示

- 如果 mihomo 立即崩溃 → 检查日志 (`/var/log/mihomo.log`)
- 常见问题：错误的配置路径、权限拒绝，或 mihomo 需要 root 权限用于 TUN
- 您也可以使用 Homebrew 的 `mihomo` formula (`brew install mihomo`) — 它会安装二进制文件，但仍需手动 plist 来设置 daemon

此设置将使 mihomo 始终运行，即使在重启或崩溃后。

参考资料：  

- [https://wiki.metacubex.one/en/startup/service](https://wiki.metacubex.one/en/startup/service) (Linux 示例，但有用概念)
- [https://note.okhk.net/use-launchctl-to-start-clash-meta-kernel-on-macos](https://note.okhk.net/use-launchctl-to-start-clash-meta-kernel-on-macos)
- [https://github.com/MetaCubeX/mihomo/discussions/614](https://github.com/MetaCubeX/mihomo/discussions/614) (macOS launchd plist 讨论)