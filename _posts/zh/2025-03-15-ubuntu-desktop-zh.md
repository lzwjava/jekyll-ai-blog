---
audio: false
generated: true
lang: zh
layout: post
title: 在 Ubuntu 上安装桌面环境
translated: true
type: note
---

听起来您的 Ubuntu 系统可能没有安装图形用户界面（GUI），这就解释了为什么您看不到文件浏览器（在 Linux 中通常称为文件管理器）或任何类似“访达”的程序。这种情况可能发生在您安装了 Ubuntu 服务器版本、选择了最小化安装，或者存在阻止 GUI 加载的问题。别担心——我们可以通过安装 GNOME（Ubuntu 的默认桌面环境）或其他您偏好的 GUI 来解决这个问题。以下是详细操作步骤。

### 第一步：更新系统

在安装任何软件之前，最好先确保软件包列表是最新的并且系统已完全升级。打开终端并运行以下命令：

```bash
sudo apt update
```

此命令用于刷新可用软件包列表。

```bash
sudo apt upgrade
```

此命令将所有已安装的软件包更新到最新版本。如果出现提示，按 `Y` 确认。

### 第二步：安装 GNOME 桌面环境

既然您提到想要“类似 GNOME 或其他”的 GUI，我们就从 GNOME 开始，因为它是 Ubuntu 桌面的默认环境，并包含一个名为 Nautilus 的文件管理器。运行以下命令进行安装：

```bash
sudo apt install ubuntu-desktop
```

此命令将安装完整的 GNOME 桌面环境以及标准应用程序，如文件管理器、网页浏览器等。根据您的网速和系统性能，安装可能需要几分钟。如果要求选择显示管理器（例如 GDM 或 LightDM），通常可以按 Enter 键选择默认选项（GNOME 使用 GDM）。

### 第三步：重启系统

安装完成后，重启系统以启动 GUI：

```bash
sudo reboot
```

系统重启后，您应该会看到图形登录界面。登录后，您将拥有一个功能齐全的桌面，其中包含可用于浏览文件的文件管理器（Nautilus）。

### 如果仍然无法使用怎么办？

如果重启后仍然看不到 GUI，可能是显示管理器或图形驱动程序存在问题。您可以尝试手动启动显示管理器进行测试：

```bash
sudo systemctl start gdm
```

如果这样能显示登录界面，那就太好了！为确保每次启动时自动启动，请运行：

```bash
sudo systemctl enable gdm
```

如果 GUI 仍未出现，请通过以下命令查看系统日志以检查错误：

```bash
journalctl -b
```

查找与 `gdm`、`Xorg` 或图形驱动程序相关的消息，并随时提供这些详细信息以寻求进一步帮助。

### 替代 GUI 选项

如果您更喜欢其他 GUI 而不是 GNOME，以下是一些流行的替代方案：

- **KDE Plasma**（时尚且可定制）：

  ```bash
  sudo apt install kubuntu-desktop
  ```

- **XFCE**（轻量且快速）：

  ```bash
  sudo apt install xubuntu-desktop
  ```

- **LXDE**（非常轻量，适合旧硬件）：

  ```bash
  sudo apt install lubuntu-desktop
  ```

安装以上任一选项后，使用 `sudo reboot` 重启，您将获得一个带有文件管理器的桌面环境（例如，KDE 使用 Dolphin，XFCE 使用 Thunar）。

### 为什么我没有 GUI？

您可能没有看到 GUI 的原因包括：

- 您安装了 Ubuntu Server，该版本默认不包含桌面环境。
- 您在安装过程中选择了最小化安装，跳过了 GUI。
- 极少数情况下，GUI 已安装但由于配置或硬件问题而无法启动。

如果问题在于缺少 GUI，按照上述方法安装 `ubuntu-desktop` 应该可以解决。如果您怀疑是现有 GUI 的问题，请告诉我，我们可以进一步排查！

### 总结

要在 Ubuntu 系统上安装 GNOME 并获取文件浏览器：

1. `sudo apt update`
2. `sudo apt upgrade`
3. `sudo apt install ubuntu-desktop`
4. `sudo reboot`

您很快将拥有一个带有文件管理器的图形界面可供使用。享受您的 Ubuntu 桌面吧！
