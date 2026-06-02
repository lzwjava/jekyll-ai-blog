---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GitHub Xcode插件揭秘
translated: true
type: note
---

### 什么是 Reveal-In-GitHub？

Reveal-In-GitHub 是一款 Xcode 插件，可让您从 Xcode 工作区快速跳转到当前代码库的 GitHub 关键功能页面。该插件专为在 GitHub 托管的 Git 项目开发者设计，只需一键（或使用键盘快捷键）即可访问提交历史、追溯视图、拉取请求、议题和通知等功能——无需离开 Xcode 或手动输入网址。

### 前提条件

- 已安装 Xcode（已在最新版本测试，未指定最低版本要求）
- 项目必须是在 GitHub 托管的 Git 代码库（插件会自动检测代码库 URL 和文件路径）
- 若项目有多个 Git 远程仓库，首次使用时将提示选择默认仓库

### 安装方法

提供两种主要安装方式：

#### 方案一：通过 Alcatraz 安装（推荐）

1. 若未安装 Alcatraz（Xcode 插件管理器），请先安装。可参考在线教程，如需中文指南可查看[此文章](http://blog.devtang.com/blog/2014/03/05/use-alcatraz-to-manage-xcode-plugins/)
2. 在 Xcode 中打开 Alcatraz（通过菜单栏：`Window > Package Manager`）
3. 搜索 "Reveal In GitHub"
4. 点击 **安装**
5. 重启 Xcode

#### 方案二：手动安装

1. 克隆代码库：

   ```
   git clone https://github.com/lzwjava/Reveal-In-GitHub.git
   ```

2. 在 Xcode 中打开 `Reveal-In-GitHub.xcodeproj` 文件
3. 编译项目（Product > Build 或 ⌘B），将生成 `Reveal-In-GitHub.xcplugin` 文件
4. 将插件移动至：
   `~/Library/Application Support/Developer/Shared/Xcode/Plug-ins/`
5. 重启 Xcode

安装完成后，插件将出现在 Xcode 菜单栏的 **Editor > Reveal In GitHub** 下

### 使用指南

安装并重启 Xcode 后：

1. 在 Xcode 中打开 GitHub 托管的项目并编辑源文件（例如定位到特定代码行）
2. 使用键盘快捷键或 **Editor > Reveal In GitHub** 菜单项跳转至 GitHub。插件会自动检测代码库、当前文件、行号和最新提交哈希值

以下是内置菜单项与快捷键速查表（快捷键遵循 ⌃⇧⌘ + 标题首字母模式）：

| 菜单项         | 快捷键       | 功能说明 | GitHub 网址示例（针对 lzwjava/LZAlbum 代码库中 fd7224 提交的 LZAlbumManager.m 文件第 40 行） |
|----------------|-------------|--------------|-----------------------------------------------------------------------------------------------|
| **设置**       | ⌃⇧⌘S      | 打开自定义面板 | 不适用 |
| **代码库**     | ⌃⇧⌘R      | 打开代码库主页 | <https://github.com/lzwjava/LZAlbum> |
| **议题**       | ⌃⇧⌘I      | 打开议题列表 | <https://github.com/lzwjava/LZAlbum/issues> |
| **拉取请求**   | ⌃⇧⌘P      | 打开拉取请求列表 | <https://github.com/lzwjava/LZAlbum/pulls> |
| **快速文件**   | ⌃⇧⌘Q      | 打开当前行文件视图 | <https://github.com/lzwjava/LZAlbum/blob/fd7224/LZAlbum/manager/LZAlbumManager.m#L40> |
| **历史记录**   | ⌃⇧⌘L     | 打开文件提交历史 | <https://github.com/lzwjava/LZAlbum/commits/fd7224/LZAlbum/manager/LZAlbumManager.m> |
| **追溯**       | ⌃⇧⌘B      | 打开当前行追溯视图 | <https://github.com/lzwjava/LZAlbum/blame/fd7224/LZAlbum/manager/LZAlbumManager.m#L40> |
| **通知**       | ⌃⇧⌘N   | 打开代码库通知 | <https://github.com/lzwjava/LZAlbum/notifications?all=1> |

- **使用技巧**：
  - 快捷键不会与 Xcode 默认快捷键冲突
  - 若选中文本范围，部分操作（如追溯）将定位到该范围（例如 #L40-L43）
  - 测试方法：打开项目定位到某行，按 ⌃⇧⌘B 即可在浏览器中打开追溯页面

### 自定义设置

如需调整或添加菜单项：

1. 按 ⌃⇧⌘S 或访问 **Editor > Reveal In GitHub > 设置**
2. 在设置面板中：
   - 点击"+"按钮添加新项：输入标题（如"Wiki"）、快捷键和 URL 模式
   - URL 模式使用占位符：
     - `{git_remote_url}`：代码库完整 URL（如 <https://github.com/user/repo）>
     - `{commit}`：当前分支最新提交哈希值
     - `{file_path}`：文件相对路径
     - `#{selection}`：当前行或选中范围（如 #L40）
   - 示例：创建 Wiki 链接时，设置模式为 `{git_remote_url}/wiki`
3. 若有多个远程仓库，可使用"清除默认仓库"按钮重置选择

本插件灵感来源于 [ShowInGitHub](https://github.com/larsxschneider/ShowInGitHub)，采用 MIT 许可证授权。

[Reveal-In-GitHub 代码库地址](https://github.com/lzwjava/Reveal-In-GitHub)
