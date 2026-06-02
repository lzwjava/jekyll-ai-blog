---
audio: false
generated: true
lang: zh
layout: post
title: Git分支可视化工具
translated: true
type: note
---

要在 Windows 上可视化 Git 仓库中的多个分支，可以使用 TortoiseGit 或其他工具来显示选定分支的图形。TortoiseGit 的修订图功能强大，但在显示所有分支时可能显得杂乱。以下是使用 TortoiseGit 查看多个特定分支图形的步骤，以及提供更灵活替代方案的工具。

### 使用 TortoiseGit 查看多个分支
TortoiseGit 的修订图可以显示多个分支，但界面不允许直接选择特定分支。不过，您可以通过筛选视图来聚焦相关分支。

1. **打开修订图**：
   - 在 Windows 资源管理器中导航至您的仓库文件夹。
   - 右键单击文件夹，选择 **TortoiseGit** > **修订图**。
   - 默认情况下，这会显示所有引用（分支、标签等）的图形，如果分支数量众多，界面可能会显得杂乱。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-revgraph.html)

2. **筛选特定分支**：
   - 在修订图窗口中，使用**筛选选项**减少杂乱显示：
     - 前往 **查看** 菜单，选择 **显示分支与合并** 以突出分支关系。[](https://stackoverflow.com/questions/67642974/tortoisegit-log-can-i-view-only-branch-and-merge-commits)
     - 要聚焦特定分支，可右键单击某次提交并选择 **显示日志** 以打开日志对话框，在此可通过 **查看 > 标签 > 本地分支** 或 **远程分支** 切换显示相关引用。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-showlog.html)
   - 或者，在日志对话框中使用 **遍历行为 > 压缩图形** 选项简化图形，仅显示合并点和带引用（如分支末端）的提交。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-showlog.html)[](https://stackoverflow.com/questions/67642974/tortoisegit-log-can-i-view-only-branch-and-merge-commits)

3. **导航图形**：
   - 使用**概览窗口**通过拖拽高亮区域来导航大型图形。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-revgraph.html)
   - 悬停在修订节点上可查看日期、作者和注释等详细信息。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-revgraph.html)
   - 按住 Ctrl 键单击两个修订版本，可通过右键菜单进行比较（例如 **比较修订版本**）。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-revgraph.html)

4. **局限性**：
   - TortoiseGit 的修订图默认显示所有分支（除非进行筛选），且图形视图没有直接选项用于仅选择特定分支。[](https://stackoverflow.com/questions/60244772/how-to-interpret-tortoise-git-revision-graph)
   - 若需要更清晰的视图，可考虑使用下文介绍的替代工具。

### 查看多个分支的替代工具
如果 TortoiseGit 界面在选择特定分支方面功能有限，可尝试以下工具，它们能提供更灵活的分支可视化控制：

#### 1. **Visual Studio Code 配合 Git Graph 扩展**
   - **安装**：下载 Visual Studio Code 并安装 **Git Graph** 扩展。[](https://x.com/midudev/status/1797990974917927150)
   - **使用方法**：
     - 在 VS Code 中打开您的仓库。
     - 通过源代码管理选项卡或命令面板（`Ctrl+Shift+P`，输入 "Git Graph"）访问 Git Graph 视图。
     - 点击界面中的分支名称可选择要在图形中显示的特定分支。
     - 图形会以颜色编码的线条清晰显示提交、分支和合并操作。[](https://ardalis.com/git-graph-visualizes-branches-in-vs-code-for-free/)
   - **优势**：轻量级、免费，支持交互式选择多个分支。提供提交比较和基础 Git 操作功能。[](https://ardalis.com/git-graph-visualizes-branches-in-vs-code-for-free/)

#### 2. **SourceTree**
   - **安装**：为 Windows 下载 SourceTree（免费）。[](https://stackoverflow.com/questions/12324050/how-can-i-visualize-github-branch-history-on-windows)[](https://stackoverflow.com/questions/12912985/git-visual-diff-between-branches)
   - **使用方法**：
     - 在 SourceTree 中打开您的仓库。
     - **历史记录**视图会显示分支和提交的图形化呈现。
     - 使用左侧分支列表切换特定分支的可见性，仅聚焦于您想查看的分支。
     - 右键单击分支或提交可执行合并或比较等操作。[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)
   - **优势**：清晰的分支可视化效果，具有一致的色彩编码和拖拽式合并等交互功能。[](https://superuser.com/questions/699094/how-can-i-visualize-git-flow-branches)[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)

#### 3. **GitKraken**
   - **安装**：下载 GitKraken（开源项目免费，私有仓库需付费）。[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)[](https://stackoverflow.com/questions/1838873/visualizing-branch-topology-in-git)
   - **使用方法**：
     - 在 GitKraken 中打开您的仓库。
     - 中央图形区域会显示所有分支，可通过分支列表隐藏/显示特定分支。
     - 点击分支标签可聚焦特定分支，或使用搜索功能筛选提交。[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)
   - **优势**：界面直观且视觉吸引力强，具有一致的分支着色和冲突解决等高级功能。[](https://superuser.com/questions/699094/how-can-i-visualize-git-flow-branches)[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)

#### 4. **使用 `git log` 命令行工具**
   - 若偏好基于终端的解决方案，可使用 Git 内置的图形视图：
     ```bash
     git log --graph --oneline --decorate --branches=<分支1> --branches=<分支2>
     ```
     将 `<分支1>` 和 `<分支2>` 替换为您要可视化的分支名称（例如 `feature1`、`feature2`）。使用 `--branches=*` 可显示所有分支，或显式指定多个分支。[](https://how-to.dev/how-to-display-git-branches-as-a-tree-in-cli)
   - **便捷别名设置**：
     创建 Git 别名以便快速访问：
     ```bash
     git config --global alias.tree "log --graph --oneline --decorate --branches="
     ```
     然后运行 `git tree feature1 feature2` 即可查看仅包含这些分支的图形。[](https://how-to.dev/how-to-display-git-branches-as-a-tree-in-cli)
   - **优势**：无需额外软件，可精确指定分支。输出为基于文本的格式，但在小型仓库中清晰可读。[](https://x.com/GWierzowiecki/status/1927657575048179899)

### 推荐建议
- **追求简洁与集成**：使用 **VS Code 配合 Git Graph 扩展**，这是轻量级免费方案，支持选择特定分支。[](https://x.com/midudev/status/1797990974917927150)
- **需要高级可视化**：使用 **GitKraken** 或 **SourceTree**，提供更精美的图形界面，支持交互式分支选择和一致的颜色编码。[](https://www.geeksforgeeks.org/how-to-visualizing-branch-topology-in-git/)
- **TortoiseGit 用户**：可继续使用修订图，通过**压缩图形**或**显示分支与合并**等筛选功能聚焦关键分支，但需注意其在选择特定分支方面的局限性。[](https://stackoverflow.com/questions/67642974/tortoisegit-log-can-i-view-only-branch-and-merge-commits)
- **终端用户**：使用带特定分支筛选器的 `git log` 命令，无需额外工具即可实现快速精确的可视化。[](https://how-to.dev/how-to-display-git-branches-as-a-tree-in-cli)

如果您需要处理大量分支，GitKraken 或 SourceTree 可能是选择性可视化目标分支的最佳选择，因为它们提供直观的分支切换功能。如需协助设置这些工具或进一步说明，请随时告知！
