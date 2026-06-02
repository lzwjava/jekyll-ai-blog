---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 将 Git Bash 设置为 VS Code 终端
translated: true
type: note
---

Question: 在 Windows 上的 VS Code 中，如何将 Git Bash 设置为 terminal 的 profile？

Answer:

在 Windows 上的 Visual Studio Code 中，有两种主要方法可以将 Git Bash 设置为 terminal profile：最简单的 GUI 方式（推荐）和手动编辑 settings.json 文件。

### 最简单的方法（使用内置选择器）

1. 按 `Ctrl + `` (反引号) 或通过 **Terminal > New Terminal** 在 VS Code 中打开集成 terminal。
2. 在 terminal 面板中，点击 "+" 图标（或当前 terminal 名称）旁边的下拉箭头。
3. 从菜单中选择 **Select Default Profile**。
4. 从可用 profiles 列表中选择 **Git Bash**（如果已安装 Git for Windows，它应该会出现）。
5. 关闭并重新打开 terminal（或重启 VS Code）使更改生效。

如果 Git 安装在默认位置，VS Code 会自动检测到 Git Bash。

### 手动方法（编辑 settings.json）

如果 Git Bash 没有出现在下拉列表中，或者你需要自定义配置：

1. 使用 `Ctrl + Shift + P` 打开 Command Palette。
2. 输入并选择 **Preferences: Open Settings (JSON)**。
3. 在你的用户 settings.json 中添加或修改以下行：

```json
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

VS Code 通常会自动检测 Git Bash，因此这一行通常就足够了。保存后重启 VS Code。

如果未检测到（罕见情况），请显式定义 profile：

```json
"terminal.integrated.profiles.windows": {
    "Git Bash": {
        "path": "C:\\Program Files\\Git\\bin\\bash.exe",
        "icon": "terminal-bash"
    }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

如果你的 Git 安装在其他地方，请调整路径（常见路径：`C:\\Program Files\\Git\\bin\\bash.exe` 或 `C:\\Program Files (x86)\\Git\\bin\\bash.exe`）。

**注意**：

- 为了正确集成，请使用 `bash.exe`（而不是 `git-bash.exe`）。
- 如果需要，可以在 args 中添加 `--login` 以帮助加载你的 ~/.bash_profile，但这是可选的。
- 更改后，打开一个新的 terminal 即可看到 Git Bash 已作为默认设置。

这将使 Git Bash 作为一个可选的 profile 出现，并在打开新 terminal 时将其设为默认。

References:

- [https://code.visualstudio.com/docs/terminal/profiles](https://code.visualstudio.com/docs/terminal/profiles)
- [https://stackoverflow.com/questions/42606837/how-do-i-use-bash-on-windows-from-the-visual-studio-code-integrated-terminal](https://stackoverflow.com/questions/42606837/how-do-i-use-bash-on-windows-from-the-visual-studio-code-integrated-terminal)
- [https://bobbyhadz.com/blog/vscode-change-default-terminal](https://bobbyhadz.com/blog/vscode-change-default-terminal)
- [https://neutrondev.com/vs-code-integrate-git-bash-default-terminal/](https://neutrondev.com/vs-code-integrate-git-bash-default-terminal/)
