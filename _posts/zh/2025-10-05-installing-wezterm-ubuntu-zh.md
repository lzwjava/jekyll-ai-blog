---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在Ubuntu上安装WezTerm
translated: true
type: note
---

出现“无法定位软件包 wezterm”错误是因为 WezTerm 未包含在 Ubuntu 默认软件源中。你需要先添加官方第三方源，以下是使用原生 APT 方法的逐步解决方案（推荐用于实现无缝集成）：

1. 添加软件源的 GPG 密钥：

   ```
   curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg
   ```

2. 将软件源添加到源列表：

   ```
   echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list
   ```

3. 为密钥文件设置正确权限：

   ```
   sudo chmod 644 /usr/share/keyrings/wezterm-fury.gpg
   ```

4. 更新软件包列表：

   ```
   sudo apt update
   ```

5. 现在安装 WezTerm：

   ```
   sudo apt install wezterm
   ```

安装完成后，可通过终端输入 `wezterm` 运行。若需使用每夜版（前沿版本），在第 5 步中改用 `sudo apt install wezterm-nightly`——但请注意该版本无法与稳定版共存。

### 替代方案：Flatpak（无需添加软件源）

若倾向使用沙盒化安装且不修改 APT 源：

1. 安装 Flatpak（如尚未安装）：`sudo apt install flatpak`
2. 添加 Flathub：`flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`
3. 安装：`flatpak install flathub org.wezfurlong.wezterm`
4. 运行：`flatpak run org.wezfurlong.wezterm`（或添加别名：`alias wezterm='flatpak run org.wezfurlong.wezterm'`）

Flatpak 采用隔离环境，可能会限制某些高级功能，但更适合测试使用。

[WezTerm Linux 安装指南](https://wezterm.org/install/linux.html)
