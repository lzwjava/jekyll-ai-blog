---
audio: false
generated: true
lang: zh
layout: post
title: Infuse问题
translated: true
type: note
---

Infuse 中出现的“Failed to open input stream in demuxing stream”错误通常表示该应用无法正常访问或处理您尝试播放的视频文件。既然您是通过 Nginx 服务器（例如 `http://192.168.1.27/movies/yourfile.mkv`）流式传输 `.mkv` 文件，并且 VLC 可以正常播放而 Infuse 不行，问题可能源于网络连接、文件兼容性或 Infuse 的特殊机制。以下是排查和修复步骤：

### 1. 验证网络连接
Infuse 经常因网络中断或配置错误而报此错误。
- **测试可访问性**：在您的 iPad（或运行 Infuse 的设备）上，确认 URL 可用：
  - 打开 Safari 并访问 `http://192.168.1.27/movies/`。您应该能看到文件列表。
  - 点击 `yourfile.mkv`——它可能无法播放，但请确认链接可访问。
- **Ping 服务器**：在 iPad 上，使用 **Network Ping Lite**（App Store 免费应用）等工具 ping `192.168.1.27`。如果失败，请检查 Wi-Fi 或服务器防火墙。
- **防火墙检查**：在 Ubuntu 服务器上：
  ```bash
  sudo ufw status
  ```
  确保 80 端口开放（`80/tcp ALLOW`）。如果没有：
  ```bash
  sudo ufw allow 80
  sudo systemctl restart nginx
  ```

### 2. 重启 Infuse 和设备
临时故障可能导致此错误。
- **关闭 Infuse**：双击 Home 键（或在新款 iPad 上上滑）并向上滑动 Infuse 以关闭。
- **重新打开**：启动 Infuse 并重试流媒体播放。
- **重启 iPad**：长按电源键，滑动关机，然后重启。再次测试。

### 3. 检查文件兼容性
虽然 Infuse 支持 `.mkv`，但错误可能与文件的编解码器或结构有关。
- **测试其他文件**：上传一个小的、确认可用的 `.mkv` 文件（例如使用 H.264 视频和 AAC 音频编码）到 `/var/www/movies/`：
  ```bash
  sudo mv /path/to/testfile.mkv /var/www/movies/
  sudo chown www-data:www-data /var/www/movies/testfile.mkv
  sudo chmod 644 /var/www/movies/testfile.mkv
  ```
  在 Infuse 中尝试播放 `http://192.168.1.27/movies/testfile.mkv`。
- **编解码器检查**：既然 VLC 可以播放，文件很可能可以流式传输，但 Infuse 可能对某些罕见编解码器（如 VP9、Opus）支持不佳。使用 Mac 上的 VLC 检查：
  - 打开 `.mkv`，按 `Cmd + I`（工具 > 编解码器信息），记下视频/音频编解码器。
  - 如果不是 H.264/AAC，使用 HandBrake（免费，handbrake.fr）重新编码：
    - 加载 `.mkv`，选择“H.264 (x264)”视频和“AAC”音频，然后转换。

### 4. 调整 Nginx 配置
Infuse 可能需要特定的头部或设置以实现流畅的流媒体播放。
- **更新配置**：编辑您的 Nginx 文件（例如 `/etc/nginx/sites-enabled/default`）：
  ```nginx
  server {
      listen 80;
      server_name 192.168.1.27 localhost;

      location /movies/ {
          alias /var/www/movies/;
          autoindex on;
          add_header Accept-Ranges bytes;  # 确保范围请求工作
          add_header Content-Disposition "inline";  # 有助于流媒体播放
      }
  }
  ```
- **重新加载**：
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```
- **原因**：`Accept-Ranges` 确保 Infuse 可以请求文件的部分内容（对流媒体至关重要）。

### 5. 提交诊断报告
Infuse 的开发人员建议在问题持续时使用此方法。
- **步骤**：
  1. 在 Infuse 中，进入 **设置 > 通用**。
  2. 点击 **提交诊断报告**。
  3. 记下它给出的代码。
  4. 访问 [Firecore 社区论坛](https://community.firecore.com/)，发布代码并描述您的设置（Nginx、`.mkv`、HTTP 流媒体）。
- **原因**：他们可以确定是程序错误还是配置问题。

### 6. 替代解决方案
如果 Infuse 持续失败：
- **使用 VLC**：在 iPad 上坚持使用 VLC for Mobile（因为它工作可靠）。
- **更换应用**：尝试使用 **nPlayer** 或 **PlayerXtreme**（App Store）播放相同 URL。

### 可能原因
既然 VLC 可以正常流式传输，很可能是网络小问题或 Infuse 对 HTTP 流的处理更严格。Nginx 调整（步骤 4）和测试文件（步骤 3）通常能解决此问题。如果不行，诊断报告会提供更多线索。

尝试这些步骤后，请告诉我您看到的情况——特别是任何日志错误或诊断代码！
