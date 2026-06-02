---
audio: false
generated: true
lang: zh
layout: post
title: 配置qBittorrent实现做种与自动文件管理
translated: true
type: note
---

看起来您希望配置 qBittorrent 在持续做种的同时，自动将下载完成的 `.mkv` 文件移动到 `/var/www/movies` 目录以供服务器使用。以下将逐步指导您实现此需求（假设您在 `/var/www/movies` 为有效目录的系统上使用 qBittorrent，例如搭载 Apache 或 Nginx 的 Linux 服务器）。具体设置如下：

---

### 分步指南

#### 1. **理解 qBittorrent 文件管理机制**
   - qBittorrent 支持在下载完成后自动移动文件并保持做种，前提是正确使用其内置的"设置位置"或"移动"功能。若通过外部方式手动移动文件（如文件管理器），将导致做种中断，除非重新指向新位置。

#### 2. **配置 qBittorrent 设置**
   - 打开 qBittorrent
   - 进入 **工具 > 选项**（或按 `Alt + O`）

   ##### a) **设置默认下载位置**
   - 在 **下载** 选项卡中：
     - 将 **默认保存路径** 设为临时下载目录（如 `/home/user/downloads` 或其他有空间的位置），该目录用于存储下载中和做种中的文件，直至文件被移动
     - 可选设置：在 **将未完成文件保存至** 指定相同或不同目录

   ##### b) **启用自动文件移动**
   - 找到 ** torrent 完成时** 区域：
     - 勾选 **自动移动已完成下载到**
     - 将路径设置为 `/var/www/movies`，这样 qBittorrent 会在下载完成后将 `.mkv` 文件移至该目录
   - 重要说明：移动后 qBittorrent 将从新位置 (`/var/www/movies`) 继续做种，无需担心做种中断

   ##### c) **可选：仅筛选 .mkv 文件**
   - 若需仅移动 `.mkv` 文件（保留其他文件类型如 `.txt` 或 `.nfo`），可改用 **运行外部程序** 功能（参见下文第3步）替代自动移动选项

   ##### d) **设置做种限制**
   - 在 **BitTorrent** 或 **下载** 选项卡中：
     - 根据需要设置做种限制（如达到特定分享率或时长）。若需无限做种，将 **分享率** 和 **时间** 设为 `0` 或取消勾选限制
     - 此设置可确保 qBittorrent 从 `/var/www/movies` 持续上传做种
   - 点击 **应用** 并 **确定** 保存设置

#### 3. **替代方案：通过"运行外部程序"实现精细控制**
   - 若需更定制化操作（如仅移动 `.mkv` 文件且其他文件保留在原位置做种）：
     - 在 **选项 > 下载** 中找到 **运行外部程序**
     - 勾选 ** Torrent 完成时运行外部程序**
     - 输入如下命令：
       ```
       mv "%F"/*.mkv /var/www/movies/
       ```
       - `%F` 是 qBittorrent 用于表示内容文件夹路径的占位符。此命令仅移动 `.mkv` 文件至 `/var/www/movies`
     - 注意：移动后 `.mkv` 文件将从新位置继续做种，其他文件（如 `.torrent`, `.nfo`）仍保留在原位置做种

#### 4. **权限验证**
   - 确保 qBittorrent 对 `/var/www/movies` 具有写权限：
     - Linux 系统执行：
       ```
       sudo chown -R <qbittorrent用户>:<qbittorrent用户组> /var/www/movies
       sudo chmod -R 775 /var/www/movies
       ```
       将 `<qbittorrent用户>` 和 `<qbittorrent用户组>` 替换为运行 qBittorrent 的实际用户和组（如您的用户名或服务账户 `qbittorrent`）
   - 若权限不足，qBittorrent 将无法移动文件至该目录

#### 5. **测试配置**
   - 向 qBittorrent 添加包含 `.mkv` 文件的种子
   - 等待下载完成
   - 验证以下事项：
     - `.mkv` 文件已移至 `/var/www/movies`
     - 种子状态切换为 **做种**，且上传速度显示仍在共享文件
   - 访问 `/var/www/movies` 确认文件存在且可通过网页服务器访问（如 `http://<服务器IP>/movies`）

#### 6. **手动移动现有文件（如需）**
   - 对于已下载且需移至 `/var/www/movies` 但不中断做种的种子：
     - 在 qBittorrent 中右键点击种子
     - 选择 **设置位置**
     - 选择 `/var/www/movies` 并让 qBittorrent 移动文件
     - 移动完成后将从新位置继续做种

#### 7. **优化上传设置**
   - 为最大化做种效率：
     - 进入 **选项 > 速度**：
       - 将 **上传限制** 设为 `0`（无限制）或较高值（如最大上传速度的80%）
     - 进入 **选项 > 连接**：
       - 确保勾选 **启用 UPnP / NAT-PMP 端口转发**（若路由器支持），或手动配置端口转发以改善连接性
       - 增加 **全局最大上传连接数**（如设为50或100）以允许更多节点连接

---

### 关键说明
- **做种连续性**：只要通过 qBittorrent 内置功能移动文件（自动移动或"设置位置"），程序会自动更新内部跟踪记录并从 `/var/www/movies` 继续做种
- **网页服务器访问**：请确保网页服务器（如 Apache/Nginx）已配置为可访问 `/var/www/movies` 目录（此配置超出 qBittorrent 范围，但对实现服务器目标至关重要）
- **存储空间**：确保 `/var/www/movies` 有足够空间存储文件

若遇到问题（如文件未移动或做种停止），请提供系统详情（操作系统、qBittorrent 版本等），我将协助进一步优化解决方案！
