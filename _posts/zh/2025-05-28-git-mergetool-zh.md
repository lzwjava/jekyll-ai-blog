---
audio: false
generated: true
lang: zh
layout: post
title: 配置TortoiseGit为Git合并工具
translated: true
type: note
---

要将 TortoiseGit 配置为 Git 的合并工具，您需要在 Git 配置中设置 TortoiseGitMerge（TortoiseGit 附带的合并工具）。以下是实现此目标的步骤：

### 前提条件
- 确保系统已安装 TortoiseGit。您可以从 [tortoisegit.org](https://tortoisegit.org) 下载。
- 确认 TortoiseGitMerge 可执行文件可用（通常位于 `C:\Program Files\TortoiseGit\bin\TortoiseGitMerge.exe`）。

### 配置 TortoiseGitMerge 为 Git 合并工具的步骤

1. **打开命令提示符或 Git Bash**
   - 您可以使用 Windows 命令提示符、PowerShell 或 Git Bash 来运行必要的 Git 配置命令。

2. **设置 TortoiseGitMerge 为合并工具**
   运行以下命令配置 Git 使用 TortoiseGitMerge：

   ```bash
   git config --global merge.tool tortoisegitmerge
   git config --global mergetool.tortoisemerge.cmd "\"C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe\" -base:\"$BASE\" -theirs:\"$REMOTE\" -mine:\"$LOCAL\" -merged:\"$MERGED\""
   ```

   **说明**：
   - `merge.tool tortoisegitmerge`：将合并工具名称设置为 `tortoisegitmerge`（您可以选择任何名称，但这是约定俗成的）。
   - `mergetool.tortoisemerge.cmd`：指定运行 TortoiseGitMerge 的命令及相应参数：
     - `-base:"$BASE"`：共同祖先文件。
     - `-theirs:"$REMOTE"`：来自要合并分支的文件。
     - `-mine:"$LOCAL"`：来自您当前分支的文件。
     - `-merged:"$MERGED"`：保存已解决合并结果的输出文件。
   - 在路径中使用正斜杠（`/`），并根据需要转义引号，尤其是路径包含空格时。

   **注意**：如果 TortoiseGit 安装在其他位置（例如 `E:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe`），请调整路径。

3. **可选：禁用合并工具提示**
   为避免每次运行 `git mergetool` 时出现提示，可以禁用提示：

   ```bash
   git config --global mergetool.prompt false
   ```

4. **可选：确保 TortoiseGitMerge 在系统 PATH 中**
   如果 Git 找不到 TortoiseGitMerge，请确保其目录在系统的 PATH 环境变量中：
   - 右键点击“此电脑”或“我的电脑” → 属性 → 高级系统设置 → 环境变量。
   - 在“系统变量”下，找到并编辑 `Path` 变量，添加 `C:\Program Files\TortoiseGit\bin`。
   - 或者，在 Git 配置中显式设置路径：

     ```bash
     git config --global mergetool.tortoisemerge.path "C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe"
     ```

5. **测试配置**
   - 在 Git 仓库中创建合并冲突（例如，合并两个有冲突更改的分支）。
   - 运行以下命令启动合并工具：

     ```bash
     git mergetool
     ```

   - TortoiseGitMerge 应会打开，显示冲突文件的基础版本、他人版本和我的版本的三窗格视图。底部窗格是合并结果。

6. **在 TortoiseGitMerge 中解决冲突**
   - 在三窗格视图中，TortoiseGitMerge 显示：
     - **左窗格**：“他人”版本（来自要合并的分支）。
     - **右窗格**：“我的”版本（来自您当前的分支）。
     - **中间窗格**：基础（共同祖先）版本。
     - **底部窗格**：用于解决冲突的合并结果。
   - 右键点击冲突部分，选择如“使用‘他人’文本块”、“使用‘我的’文本块”等选项，或手动编辑合并文件。
   - 解决后，保存文件（文件 → 保存）并关闭 TortoiseGitMerge。
   - 如果 TortoiseGitMerge 成功退出（退出代码 0），Git 会将文件标记为已解决。如果出现提示，确认将冲突标记为已解决。

7. **提交已解决的合并**
   解决冲突后，提交更改：

   ```bash
   git commit
   ```

   **注意**：如果冲突发生在 rebase 或 cherry-pick 过程中，请使用相应的 TortoiseGit 对话框（Rebase 或 Cherry-pick）继续过程，而不是标准的提交对话框。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-conflicts.html)

### 通过 TortoiseGit GUI 使用 TortoiseGitMerge
如果您更喜欢使用 TortoiseGit GUI 解决冲突：
1. 在 Windows 资源管理器中右键点击冲突文件。
2. 选择 **TortoiseGit → 编辑冲突**。
3. TortoiseGitMerge 将打开，允许您如上所述解决冲突。
4. 保存后，再次右键点击并选择 **TortoiseGit → 已解决** 以将文件标记为已解决。
5. 使用 TortoiseGit 的提交对话框提交更改。

### 故障排除
- **错误：“不支持的合并工具 ‘tortoisemerge’”**
  - 确保 `TortoiseGitMerge.exe` 的路径正确且可访问。
  - 验证工具名称在 `merge.tool` 和 `mergetool.<tool>.cmd` 配置中完全匹配。
  - 检查 TortoiseGitMerge 是否在 PATH 中或使用 `mergetool.tortoisemerge.path` 显式设置。[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)
- **文件路径中的空格**
  - 如果文件路径包含空格，使用转义引号的命令语法（如上所示）应能正确处理。[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)
- **Cygwin 用户**
  - 如果使用 Cygwin，调整路径以使用 Cygwin 的挂载点，例如：

    ```bash
    git config --global mergetool.tortoisemerge.cmd '"/cygdrive/c/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe" -base:"$BASE" -theirs:"$REMOTE" -mine:"$LOCAL" -merged:"$MERGED"'
    ```

    这考虑了 Cygwin 的 `/cygdrive/c/` 路径结构。[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)
- **找不到 TortoiseGitMerge**
  - 如果您之前使用过 TortoiseSVN 的 TortoiseMerge，请确保指向 `TortoiseGitMerge.exe`，因为可执行文件名称在 TortoiseGit 1.8 版本中已更改。[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)[](https://stackoverflow.com/questions/15881449/why-doesnt-tortoisemerge-work-as-my-mergetool)

### 附加说明
- TortoiseGitMerge 支持用于冲突解决的三窗格视图，非常适合合并。它会自动合并非冲突更改并高亮显示冲突以供手动解决。[](https://tortoisegit.org/docs/tortoisegitmerge/tmerge-dug.html)[](https://manios.org/2018/05/30/git-merge-conflicts-using-tortoise-git-merge-windows)
- 如果您也想将 TortoiseGitMerge 用作差异工具，类似地配置：

  ```bash
  git config --global diff.tool tortoisediff
  git config --global difftool.tortoisediff.cmd "\"C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe\" -mine:\"$REMOTE\" -base:\"$LOCAL\""
  ```

  然后使用 `git difftool` 比较文件。[](https://stackoverflow.com/questions/16493368/can-tortoisemerge-be-used-as-a-difftool-with-windows-git-bash)
- 对于高级设置，您可以配置 TortoiseGit 等待合并工具关闭并根据退出代码自动将文件标记为已解决。在 TortoiseGit 设置 → 外部程序 → 合并工具中，选择“在执行外部合并工具时阻止 TortoiseGit”并启用“信任退出代码”。[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-settings.html)

### 来源
- TortoiseGit 文档：[](https://tortoisegit.org/docs/tortoisegitmerge/tmerge-dug.html)[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-merge.html)[](https://tortoisegit.org/docs/tortoisegit/tgit-dug-conflicts.html)
- Stack Overflow 及其他网络资源：[](https://devstuffs.wordpress.com/2013/03/08/setting-tortoisegitmerge-in-msysgit-as-the-git-mergetool/)[](https://stackoverflow.com/questions/5190188/why-cant-i-use-tortoisemerge-as-my-git-merge-tool-on-windows)[](https://stackoverflow.com/questions/16493368/can-tortoisemerge-be-used-as-a-difftool-with-windows-git-bash)

按照这些步骤，您应该能够有效地使用 TortoiseGitMerge 作为您的 Git 合并工具，无论是通过命令行还是 TortoiseGit GUI。
