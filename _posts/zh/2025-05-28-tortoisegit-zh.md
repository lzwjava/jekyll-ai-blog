---
audio: false
generated: true
lang: zh
layout: post
title: TortoiseGit
translated: true
type: note
---

TortoiseGit 是一款 Windows Shell 扩展程序，为流行的版本控制系统 Git 提供用户友好的图形界面。它直接集成在 Windows 资源管理器中，允许您通过右键菜单执行 Git 操作。本指南将介绍在 Windows 系统上安装、配置和使用 TortoiseGit 的方法，涵盖常见任务和最佳实践。

### TortoiseGit 概述
TortoiseGit 基于 msysGit（Windows 版 Git）构建，为 Git 命令提供图形化操作界面。这款工具特别适合偏好图形界面而非命令行操作的用户。其主要功能包括：
- 与 Windows 资源管理器的右键菜单集成
- 可视化差异比较和合并工具
- 支持常用 Git 工作流（提交、推送、拉取、分支、合并等）
- 与主流问题跟踪系统和外部工具集成

### 环境准备
安装 TortoiseGit 前请确保满足以下条件：
- Windows 操作系统（建议 Windows 10 或更高版本）
- 已安装 Git for Windows（TortoiseGit 依赖该组件）
- 掌握 Git 基础概念（代码库、提交、分支等）

### 安装步骤
1. **安装 Git for Windows**：
   - 从 [Git for Windows](https://gitforwindows.org/) 或 [Git SCM](https://git-scm.com/downloads) 下载最新版本
   - 运行安装程序并按提示操作。推荐设置：
     - 使用默认编辑器（如记事本）或选择 VS Code 等编辑器
     - 选择“在 Windows 命令提示符中使用 Git”以确保可访问性
     - HTTPS 传输选择“OpenSSL”
     - 行结束符选择“按原样检出，按原样提交”（跨平台团队协作除外）
   - 完成安装

2. **安装 TortoiseGit**：
   - 从 [TortoiseGit 官网](https://tortoisegit.org/download/) 下载最新版本
   - 运行安装程序：
     - 选择默认语言和组件
     - 确保检测到 Git for Windows（若缺失会提示安装）
     - 如需 SSH 支持请安装 TortoiseGitPlink
   - 按提示重启计算机

3. **验证安装**：
   - 在 Windows 资源管理器的任意文件夹内右键，应出现“Git 克隆”“在此创建 Git 代码库”等 TortoiseGit 选项

### 初始配置
安装完成后需配置用户信息和偏好设置：
1. **设置用户信息**：
   - 右键文件夹选择 **TortoiseGit > 设置**
   - 在设置窗口导航至 **Git > 配置**
   - 输入姓名和邮箱（需与 GitHub、GitLab 等平台保持一致）：
     ```
     姓名：您的姓名
     邮箱：your.email@example.com
     ```
   - 点击 **应用** 并 **确定**

2. **配置 SSH（可选）**：
   - 若使用 SSH 连接远程代码库：
     - 打开 **PuTTYgen**（随 TortoiseGit 安装）
     - 生成新 SSH 密钥对，保存私钥并复制公钥
     - 将公钥添加到 Git 托管服务（如 GitHub、GitLab）
     - 在 TortoiseGit 设置的 **Git > 远程** 中选 TortoiseGitPlink 作为 SSH 客户端

3. **设置差异比较与合并工具**：
   - 在 **TortoiseGit > 设置 > 差异查看器** 中选择工具（推荐默认 TortoiseGitMerge 或外部工具如 Beyond Compare）
   - 合并工具可在 **合并工具** 中配置（初学者推荐 TortoiseGitMerge）

### 基础操作
以下是通过 Windows 资源管理器右键菜单执行的常见 TortoiseGit 操作：

#### 1. **克隆代码库**
   - 右键文件夹选择 **Git 克隆**
   - 在对话框中：
     - 输入代码库 URL（如 `https://github.com/用户名/仓库.git`）
     - 指定本地存储目录
     - 可选：选择分支或加载 SSH 密钥
   - 点击 **确定** 开始克隆

#### 2. **创建新代码库**
   - 进入目标文件夹，右键选择 **在此创建 Git 代码库**
   - 如需创建服务端代码库可勾选“创建纯版本库”（本地使用通常不需勾选）
   - 点击 **确定**，系统将创建 `.git` 文件夹初始化代码库

#### 3. **提交更改**
   - 将文件添加至代码库文件夹
   - 右键文件夹或选中文件，选择 **Git 提交 -> "main"**（或当前分支）
   - 在提交对话框中：
     - 输入描述更改的提交信息
     - 勾选要暂存的文件
     - 点击 **确定** 或 **提交并推送** 将更改推送到远程代码库

#### 4. **推送更改**
   - 提交后右键选择 **TortoiseGit > 推送**
   - 选择远程代码库和分支
   - 按需完成身份验证（HTTPS 的用户名/密码或 SSH 密钥）
   - 点击 **确定** 开始推送

#### 5. **拉取更改**
   - 右键选择 **TortoiseGit > 拉取** 可更新本地代码库
   - 选择远程分支后点击 **确定**
   - 如出现冲突按提示解决（使用合并工具）

#### 6. **创建与切换分支**
   - 右键选择 **TortoiseGit > 创建分支**
   - 输入分支名称后点击 **确定**
   - 切换分支时右键选择 **TortoiseGit > 切换/检出** 并选择目标分支

#### 7. **查看历史记录**
   - 右键选择 **TortoiseGit > 显示日志**
   - 查看提交历史（含作者、日期和提交信息）
   - 右键提交记录可查看更改、还原或遴选提交

#### 8. **解决合并冲突**
   - 拉取或合并时若发生冲突，TortoiseGit 会发出通知
   - 右键冲突文件选择 **TortoiseGit > 解决**
   - 使用合并工具手动编辑冲突后标记为已解决
   - 提交解决后的更改

### 高级功能
1. **储藏更改**：
   - 右键选择 **TortoiseGit > 储藏保存** 可临时保存未提交的更改
   - 选择 **TortoiseGit > 储藏应用** 可恢复储藏的更改

2. **变基操作**：
   - 右键选择 **TortoiseGit > 变基**
   - 选择目标分支并按提示重新排序或压缩提交

3. **子模块管理**：
   - 右键选择 **TortoiseGit > 子模块更新** 或 **添加** 管理子模块
   - 子模块设置可在 TortoiseGit 设置中配置

4. **二分查找**：
   - 使用 **TortoiseGit > 二分查找开始** 定位引入错误的提交
   - 标记提交为“正常”或“异常”来缩小问题提交范围

### 最佳实践
- **频繁提交**：编写清晰的提交信息，进行小规模多次提交
- **定期拉取**：保持本地代码库更新以避免冲突
- **使用分支**：为新功能创建特性分支保持主分支稳定
- **备份 SSH 密钥**：安全存储并备份 SSH 密钥
- **审查更改**：提交前使用差异查看器检查更改内容

### 故障排除
- **认证问题**：检查 Git 托管服务的 SSH 密钥或凭证配置是否正确
- **合并冲突**：使用 TortoiseGitMerge 可视化解决冲突，合并前备份文件
- **右键菜单缺失**：检查 TortoiseGit 安装是否正确及设置中是否启用资源管理器集成
- **性能缓慢**：在 **TortoiseGit > 设置 > 图标覆盖** 中禁用非必要覆盖图标

### 示例工作流
以下是为项目贡献代码的典型工作流程：

# TortoiseGit 工作流示例

## 1. 克隆代码库
- 右键文件夹选择 **Git 克隆**
- 输入代码库 URL 和本地目录
- 点击 **确定**

## 2. 创建特性分支
- 右键选择 **TortoiseGit > 创建分支**
- 命名分支（如 `feature/add-login`）
- 点击 **确定** 并切换到新分支

## 3. 实施更改
- 在代码库文件夹中编辑文件
- 右键选择 **Git 提交 -> "feature/add-login"**
- 编写提交信息并暂存文件
- 点击 **提交**

## 4. 推送更改
- 右键选择 **TortoiseGit > 推送**
- 选择远程分支（如 `origin/feature/add-login`）
- 点击 **确定**

## 5. 创建拉取请求
- 在 Git 托管服务（如 GitHub）上从特性分支向主分支创建拉取请求
- 等待审核与合并

## 6. 更新本地代码库
- 切换至主分支（**TortoiseGit > 切换/检出**）
- 拉取更新（**TortoiseGit > 拉取**）

### 资源链接
- **官方文档**：[TortoiseGit 文档](https://tortoisegit.org/docs/)
- **Git for Windows**：[Git SCM](https://git-scm.com/)
- **教程资源**：在 YouTube 或技术博客搜索“TortoiseGit 教程”获取视频指南

TortoiseGit 通过直观的界面简化了 Git 操作，让 Windows 用户能够轻松进行版本控制。如需特定任务或高级配置的帮助，欢迎随时咨询！
