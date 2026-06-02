---
audio: false
generated: true
lang: zh
layout: post
title: VS Code源代码管理指南
translated: true
type: note
---

Visual Studio Code（VS Code）内置了强大的源代码管理功能，允许开发者直接在编辑器中管理 Git、Mercurial 等版本控制系统（VCS）。本指南全面介绍如何在 VS Code 中使用源代码管理，重点讲解最常用的 VCS——Git，涵盖设置、关键功能、工作流程和高级用法。

### VS Code 源代码管理概览

VS Code 的源代码管理视图提供了直观的界面来与版本控制系统交互。它默认集成 Git 并支持通过扩展连接其他 VCS。该视图可显示变更、允许暂存、提交、分支管理、合并等操作，全程无需离开编辑器。以下是如何高效利用源代码管理的分步指南。

### 1. **在 VS Code 中设置源代码管理**

使用源代码管理需先安装 Git 并初始化仓库。具体步骤如下：

#### 前置准备

- **安装 Git**：从 [git-scm.com](https://git-scm.com/) 下载安装 Git。在终端运行 `git --version` 验证安装。
- **配置 Git**：

  ```bash
  git config --global user.name "您的姓名"
  git config --global user.email "您的邮箱@example.com"
  ```

- **安装 VS Code**：从 [code.visualstudio.com](https://code.visualstudio.com/) 安装最新版 VS Code。

#### 初始化 Git 仓库

1. 在 VS Code 中打开项目文件夹。
2. 打开终端（Ctrl+`或 macOS 的 Cmd+`）并运行：

   ```bash
   git init
   ```

   这将在项目中创建 `.git` 文件夹，将其初始化为 Git 仓库。
3. 或克隆现有仓库：

   ```bash
   git clone <仓库地址>
   ```

   然后在 VS Code 中打开克隆的文件夹。

#### 启用源代码管理视图

- 点击活动栏的源代码管理图标（顶部第三个分支状图标）或按 `Ctrl+Shift+G`（Windows/Linux）／`Cmd+Shift+G`（macOS）打开视图。
- 如果检测到 Git 仓库，VS Code 将显示包含变更管理选项的源代码管理视图。

### 2. **使用源代码管理视图**

源代码管理视图是版本控制任务的核心界面，显示：

- **变更**：自上次提交后修改、添加或删除的文件。
- **暂存变更**：准备提交的文件。
- **提交信息框**：用于输入提交信息。
- **操作按钮**：提交、刷新等功能的按钮。

#### 常用工作流程

1. **修改文件**：在项目中编辑文件。VS Code 自动检测变更并列入源代码管理视图的“变更”列表。
2. **暂存变更**：
   - 点击文件旁的 `+` 图标暂存单个文件，或通过三点菜单选择“暂存所有变更”。
   - 暂存操作将变更准备用于下次提交。
3. **编写提交信息**：
   - 在源代码管理视图顶部的文本框中输入描述性信息。
   - 示例：`新增用户认证功能`。
4. **提交变更**：
   - 点击对勾图标或按 `Ctrl+Enter`（Windows/Linux）／`Cmd+Enter`（macOS）提交已暂存变更。
   - 通过三点菜单选择“提交全部”、“提交已暂存”或“提交全部并推送”。
5. **推送至远程仓库**：
   - 若已连接远程仓库（如 GitHub），通过三点菜单的“推送”选项或终端运行 `git push` 推送变更。

### 3. **VS Code 源代码管理关键功能**

VS Code 提供多项功能优化版本控制体验：

#### 差异对比视图

- 点击“变更”下的文件可打开并排对比视图，显示与上次提交的差异。
- 使用行内操作暂存或丢弃特定代码行。

#### 分支管理

- 切换分支：点击状态栏左下角的分支名称，或使用源代码管理视图分支菜单（三点 > 分支 > 切换到...）。
- 新建分支：从分支菜单选择“创建分支”，输入名称并确认。
- 合并分支：使用“分支 > 合并分支”选择要合并到当前分支的分支。

#### 拉取与获取

- **拉取**：通过三点菜单的“拉取”选项同步远程仓库变更。
- **获取**：使用“获取”检索远程变更但不合并。

#### 冲突解决

- 合并或拉取时出现冲突，VS Code 会高亮冲突文件并提供行内解决界面：
  - 选择“接受当前变更”、“接受传入变更”、“接受双方变更”或手动编辑文件。
  - 暂存并提交已解决的文件。

#### Git Lens 扩展

安装 **GitLens** 扩展获取高级 Git 功能：

- 查看提交历史、追溯注解和文件变更。
- 访问仓库洞察（如近期提交和存储内容）。
- 通过扩展视图（`Ctrl+Shift+X` 或 `Cmd+Shift+X`）安装。

### 4. **高级用法**

#### 存储变更

- 临时保存未提交的变更：
  - 进入三点菜单 > 存储 > 存储。
  - 后续通过同一菜单应用或弹出存储内容。
- 适用于切换分支时保存未完成工作。

#### 终端 Git 命令

- 对界面未直接支持的任务，可使用集成终端：

  ```bash
  git rebase <分支>
  git cherry-pick <提交>
  git log --oneline
  ```

#### 自定义源代码管理

- **设置**：通过 VS Code 设置（`Ctrl+,` 或 `Cmd+,`）调整源代码管理行为：
  - `git.autoRepositoryDetection`：启用/禁用自动 Git 仓库检测。
  - `git.enableSmartCommit`：无暂存文件时提交所有变更。
- **SCM 提供商**：安装 Mercurial 或 SVN 等其他 VCS 的扩展。

#### GitHub 集成

- 使用 **GitHub Pull Requests and Issues** 扩展直接在 VS Code 管理 PR 和议题。
- 通过左下角账户菜单验证 GitHub 账户，以便从 GitHub 仓库推送/拉取。

### 5. **示例工作流程：创建并推送功能分支**

以下是在 VS Code 中实施常见 Git 工作流程的实践示例：

# VS Code 中的 Git 工作流程示例

## 创建并推送功能分支的步骤

1. **新建分支**：
   - 在源代码管理视图中，点击状态栏的分支名称或使用三点菜单 > 分支 > 创建分支。
   - 命名分支（如 `feature/add-login`）。
   - VS Code 将切换至新分支。

2. **修改并暂存变更**：
   - 编辑文件（例如向 `src/Login.js` 添加登录组件）。
   - 文件将出现在源代码管理视图的“变更”中。
   - 点击 `+` 图标暂存变更或选择“暂存所有变更”。

3. **提交变更**：
   - 输入提交信息（如 `新增登录组件`）。
   - 点击对勾或按 `Ctrl+Enter`（Windows/Linux）／`Cmd+Enter`（macOS）提交。

4. **推送分支**：
   - 若未设置远程仓库，先添加：

     ```bash
     git remote add origin <仓库地址>
     ```

   - 推送分支：三点菜单 > 推送，或运行：

     ```bash
     git push -u origin feature/add-login
     ```

5. **创建拉取请求**：
   - 若使用 GitHub，在浏览器中打开仓库或使用 GitHub Pull Requests 扩展创建 PR。
   - 将 PR 关联至 `feature/add-login` 分支。

## 实用技巧

- 定期从主分支拉取更新以避免冲突。
- 使用描述性提交信息提升协作效率。
- 安装 GitLens 增强提交历史和追溯视图。

### 6. **常见问题排查**

- **未检测到 Git**：确保 Git 已安装并加入系统 PATH。安装后重启 VS Code。
- **认证错误**：配置 SSH 密钥或使用 GitHub/GitLab 个人访问令牌。通过账户菜单完成认证。
- **合并冲突**：使用行内冲突解决工具或手动编辑文件后暂存提交。
- **性能缓慢**：大型项目中可禁用 `git.autoRepositoryDetection`，或使用 GitLens 优化 Git 操作。

### 7. **最佳实践**

- **频繁提交**：通过小型逻辑提交跟踪进度。
- **描述性信息**：遵循 `<类型>(<范围>): <描述>` 等规范（如 `feat(auth): 新增登录端点`）。
- **定期拉取**：与远程仓库保持同步以减少冲突。
- **备份存储**：应用存储前确认不会覆盖重要变更。
- **善用扩展**：使用 GitLens、Git History 或 Git Graph 增强功能。

### 8. **扩展资源**

- **VS Code 文档**：[VS Code 版本控制](https://code.visualstudio.com/docs/editor/versioncontrol)
- **Git 文档**：[git-scm.com/doc](https://git-scm.com/doc)
- **GitLens 扩展**：可在 VS Code 应用市场获取。
- **GitHub Pull Requests 扩展**：用于管理 PR 和议题。

本指南涵盖了 VS Code 源代码管理的基础与高级功能，重点关注 Git。遵循这些步骤和最佳实践，您将能直接在编辑器中高效管理版本控制工作流程。
