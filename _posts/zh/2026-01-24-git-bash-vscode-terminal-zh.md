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

**Question:** 如何在 Windows 中将 VS Code Terminal Profile 设置为使用 Git Bash？

**Answer:**

以下是在 Windows 上的 Visual Studio Code 中将 Git Bash 设置为默认 Terminal 的最可靠且最新的方法（2025年）：

### Method 1: 推荐方法 (通过 Terminal Profiles - 最简单)

1. 按下 **Ctrl + ,** → 打开 Settings
2. 搜索：`terminal.integrated.profiles.windows`
3. 点击 **"Edit in settings.json"** (或点击右上角的 {} 图标)
4. 添加或修改以下内容：

```json
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "source": "Git Bash",
    "icon": "terminal-bash"
  },
  "PowerShell": {
    "source": "PowerShell",
    "icon": "terminal-powershell"
  },
  "Command Prompt": {
    "path": [
      "${env:windir}\\Sysnative\\cmd.exe",
      "${env:windir}\\System32\\cmd.exe"
    ],
    "args": []
  }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

5. 保存文件 → 新打开的 Terminal 将使用 Git Bash

### Method 2: 快速设置 (如果已经自动检测到 Git Bash)

许多最近的 VS Code 版本会自动检测 Git Bash。你可以直接执行以下操作：

1. 打开 Command Palette (**Ctrl+Shift+P**)
2. 输入 → **Terminal: Select Default Profile**
3. 选择 **Git Bash**

如果你在列表中没有看到 Git Bash → 请使用 Method 1 或 Method 3。

### Method 3: 显式路径 (当自动检测失败时最可靠)

```json
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "path": "C:\\Program Files\\Git\\bin\\bash.exe",
    "icon": "terminal-bash",
    "args": [
      "--login",
      "-i"
    ]
  }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

常见的备选路径（选择你系统中存在的路径）：

```text
C:\Program Files\Git\bin\bash.exe
C:\Program Files\Git\git-bash.exe
C:\Program Files (x86)\Git\bin\bash.exe
C:\tools\Git\bin\bash.exe               ← 在 Scoop / 手动安装中常见
```

### Bonus: 让 Git Bash 体验更现代化

添加这些可选但非常受欢迎的设置：

```json
"terminal.integrated.shellArgs.windows": ["--login", "-i"],
"terminal.integrated.fontFamily": "Cascadia Code, Consolas, 'Courier New', monospace",
"terminal.integrated.cursorStyle": "line",
"terminal.integrated.cursorBlinking": true,
"terminal.integrated.scrollback": 10000,
```

### 快速排错清单

- 未安装 Git → 从 https://git-scm.com 安装
- Git Bash 仍未出现 → 重启 VS Code
- 使用的是 Portable Git? → 在 `path` 字段中使用完整路径
- 使用 Scoop/Chocolatey 的自定义位置? → 使用 `where bash` 命令查找真实路径

2025 年最常用的成功组合：

```json
"terminal.integrated.defaultProfile.windows": "Git Bash",
"terminal.integrated.profiles.windows": {
  "Git Bash": {
    "path": "C:\\Program Files\\Git\\bin\\bash.exe",
    "icon": "terminal-bash"
  }
}
```

祝你好运！

**References:**

- 无需引用（基于当前 VS Code + Git for Windows 的行为）