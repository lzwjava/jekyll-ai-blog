---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu上通过Snap更新VSCode
translated: true
type: note
---

要在 Ubuntu 上更新通过 Snap 安装的 Visual Studio Code（VSCode），请按照以下步骤操作：

1. **打开终端**：按 `Ctrl + Alt + T` 即可打开。

2. **检查更新**：Snap 会自动在后台检查更新，但您也可以通过运行以下命令手动触发更新检查：

   ```bash
   sudo snap refresh
   ```

3. **更新 VSCode**：如果有新版本的 VSCode 可用，`snap refresh` 命令将下载并安装它。您会看到显示进度的输出，例如：

   ```
   code 1.85.2 来自 Visual Studio Code (code✓) 已更新
   ```

   如果没有可用更新，则会显示：

   ```
   所有 Snap 包均为最新版本。
   ```

4. **验证更新**：要确认 VSCode 的安装版本，请运行：

   ```bash
   code --version
   ```

   这将显示 VSCode 的当前版本。

### 注意事项

- **自动更新**：Snap 包（包括 VSCode）通常会在后台自动更新。除非您希望强制更新，否则通常无需手动干预。
- **Root 权限**：系统级的 Snap 操作需要 `sudo` 命令。
- **检查 Snap 状态**：如果要查看已安装的 Snap 包及其版本，请使用：

   ```bash
   snap list
   ```

- **故障排除**：如果更新失败，请确保网络连接稳定且 Snap 守护进程正在运行（`sudo systemctl status snapd`）。您也可以尝试通过以下命令刷新 Snap 元数据：

   ```bash
   sudo snap refresh --list
   ```

此过程可确保 VSCode 保持与 Snap 商店中最新版本同步。
