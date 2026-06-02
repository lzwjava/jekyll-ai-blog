---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 将媒体文件传输至外置硬盘
translated: true
type: note
---

### 将照片和视频移至 macOS 外接磁盘

根据系统信息，您当前运行的是 macOS 15.6.1 系统，外接磁盘挂载在 `/Volumes/Untitled`（总容量 2.0 TB，可用空间 1.5 TB）。移动照片和视频涉及将文件从 Mac 存储（如照片存储在 `~/Pictures`，视频存储在 `~/Movies`）传输到外接磁盘。您可以通过图形界面（访达）或终端等命令行工具进行操作，下文将介绍这两种方法。请注意这里指的是移动文件本身，而非整个照片图库（如需移动图库，请先从照片应用导出）。

**重要注意事项：**
- **提前备份**：操作前请确保文件已备份，避免数据丢失
- **权限要求**：部分操作需要管理员权限，若终端命令提示权限不足，请以管理员身份运行
- **空间检查**：确认文件大小未超过外接磁盘可用空间（当前为 1.5 TB）
- **文件路径**：默认照片路径为 `~/Pictures`，视频路径为 `~/Movies`。若文件存储在其他目录（如下载文件夹），请相应调整路径
- **安全卸载**：移动完成后，通过访达 > 推出或执行 `diskutil unmount /Volumes/Untitled` 命令安全卸载磁盘

#### 1. 使用访达（图形界面 - 适合新手）
这是最适合普通用户的操作方式，通过 macOS 文件管理器拖放即可完成

1. **定位外接磁盘与文件：**
   - 打开访达（点击程序坞中的笑脸图标）
   - 在侧边栏“位置”下找到“Untitled”（您的外接磁盘），点击浏览内容
   - 新建访达窗口（Command + N）导航至照片/视频存储位置（如“图片”或“影片”文件夹）

2. **移动文件：**
   - 选择要移动的照片/视频（按住 Command 可多选）
   - 将其拖拽至外接磁盘窗口（建议先在磁盘中创建“PhotosBackup”等文件夹进行分类）
   - 如需移动（永久转移并释放 Mac 空间）：拖拽时按住 Option 键。如需复制（保留原件）：直接拖拽即可
     - 也可在复制后右键点击原文件选择“移到废纸篓”实现移动效果
   - 建议在磁盘中创建分类文件夹（右键 > 新建文件夹），如“Photos”和“Videos”

3. **验证与弹出：**
   - 在访达中打开外接磁盘确认文件已存在
   - 将磁盘图标拖至废纸篓（或右键点击 > 推出）安全卸载后再断开连接

此方法可保留元数据（如创建日期）并高效处理大文件

#### 2. 使用终端（命令行方式 - 适合批量操作）
若您偏好使用命令处理（如您的 Python 脚本所示），可通过终端进行精确操作，特别适合自动化或递归移动

1. **导航至文件与磁盘路径：**
   - 打开终端（应用程序 > 实用工具 > 终端）
   - 查看当前目录：运行 `pwd` 并按需导航（如 `cd ~/Pictures` 进入照片目录）
   - 确认磁盘已挂载：运行 `ls /Volumes` 查看“Untitled”。根据系统输出，您的磁盘已正常挂载

2. **移动文件：**
   - **移动**文件（永久转移并删除原件）：
     - 单个文件：`mv /path/to/photo.jpg /Volumes/Untitled/Photos/`
     - 整个目录：`mv ~/Pictures/PhotosLibrary /Volumes/Untitled/`
     - 完整移动示例：`mv ~/Pictures/* /Volumes/Untitled/Photos/`（将图片文件夹所有内容移至磁盘新文件夹，可添加 `-v` 参数显示详细输出）
   - **复制**文件（保留原件）：使用 `cp` 命令，递归目录需加 `-r` 参数
     - 示例：`cp -r ~/Pictures/PhotosLibrary /Volumes/Untitled/Photos/`（递归复制，适合需要保留原件的备份）
   - 移动视频文件：`cp -r ~/Movies/Videos/ /Volumes/Untitled/Videos/`
   - 处理隐藏文件或权限问题：如需权限可添加 `sudo`（如 `sudo mv ~/Pictures/photo.jpg /Volumes/Untitled/`）
   - 安全预览：执行 `ls -la ~/Pictures` 查看文件列表

3. **验证与卸载：**
   - 检查磁盘：运行 `ls /Volumes/Untitled` 确认传输完成
   - 安全卸载：执行 `diskutil unmount /Volumes/Untitled` 后物理断开磁盘

**高级技巧：**
- **使用 Rsync 同步**：增量备份（仅传输新文件/变更文件）可使用 `rsync -av ~/Pictures /Volumes/Untitled/Photos`（若未预装 rsync 需安装，但 macOS 已内置）
- **自动化处理**：可整合至 Python 脚本（如基于 `list_portable_disks.py` 输出，使用 `subprocess` 运行 `cp` 或 `mv` 命令）
- **MacBook 特性**：您的 M2 MacBook Air（型号 Mac14,2）通过 USB-C 传输速度较快，如需监控电池/温度可通过活动监视器查看

若遇到问题（如权限错误），请提供具体文件路径或错误信息以便进一步指导。此流程在您的系统配置下应能稳定运行。
