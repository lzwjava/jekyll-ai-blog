---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复Firefox APT存储库错误
translated: true
type: note
---

您遇到的错误是针对 Mozilla Firefox APT 软件源（`https://packages.mozilla.org/apt`）的，在获取 `binary-all/Packages` 索引文件时失败，返回 400 Bad Request。这是其他 Ubuntu/Debian 用户报告过的一个已知的间歇性问题，通常与代理配置有关（您本地代理 `127.0.0.1:7890` 暗示可能使用了 Clash、V2Ray 或类似工具，这些工具可能会篡改 APT 的 HTTPS 请求）。好消息是 APT 会忽略此失败并使用缓存的/旧的索引，因此系统更新不会被阻止——但这可能会妨碍您获取最新的 Firefox deb 软件包。

### 可尝试的快速修复方法（按顺序）
1. **清除 APT 缓存**（这可以解决损坏或过期的索引文件，对部分用户有效）：
   ```
   sudo apt clean
   sudo apt update
   ```

2. **为 APT 临时绕过代理**（因为 400 错误通常源于代理对该软件源 HTTPS 的干扰）：
   ```
   unset http_proxy https_proxy all_proxy
   sudo -E apt update
   ```
   - 在同一终端会话中运行此命令。如果有效，您可以将 `unset` 这几行添加到您的 `~/.bashrc` 文件中（或仅在运行 APT 命令前执行），或者暂时禁用代理应用程序。
   - 如果您的代理是系统全局设置的（例如在 `/etc/environment` 中），请编辑该文件以排除 APT 或暂时注释掉相关行。

3. **全局为 APT 禁用代理**（如果上述方法有效，但您想要一个一劳永逸的选项）：
   ```
   echo 'Acquire::http::Proxy "";
   Acquire::https::Proxy "";' | sudo tee /etc/apt/apt.conf.d/99no-proxy
   sudo apt update
   ```
   - 这会告诉 APT 完全忽略代理。如果需要，可以通过删除 `/etc/apt/apt.conf.d/99no-proxy` 文件来恢复。

### 如果您需要最新版 Firefox 但不想用此软件源
如果该软件源持续失败，而您只想要更新 Firefox：
- **切换到 Snap**（Ubuntu 默认方式，易于更新，无需处理软件源麻烦）：
  ```
  sudo snap install firefox
  ```
- **或者使用 Flatpak**（如果您更喜欢）：
  ```
  sudo apt install flatpak
  flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
  flatpak install flathub org.mozilla.firefox
  ```

### 预防措施/注意事项
- Mozilla 软件源是非官方的，用于获取最新版的 Firefox deb 包——除非您特别需要 deb 包，否则请考虑坚持使用 Ubuntu 的 snap 版本。
- 如果这些方法都无效，请检查您的代理日志（例如 Clash 仪表板）中是否有被拒绝的指向 `packages.mozilla.org` 的请求，或者完全在不使用代理的情况下进行测试。
- 修复后再次运行 `sudo apt update` 以验证。

如果这些方法未能解决问题，请分享更多详细信息，例如您的代理设置或完整的 `/etc/apt/sources.list.d/mozilla.list` 文件内容，以便进行更深入的故障排除。

[Ubuntu 23.10 - 更新问题](https://askubuntu.com/questions/1507571/ubuntu-23-10-update-problems-some-index-files-failed-to-download)
[Firefox apt 软件源错误](https://www.reddit.com/r/firefox/comments/1ois308/firefox_apt_repository_error/)
