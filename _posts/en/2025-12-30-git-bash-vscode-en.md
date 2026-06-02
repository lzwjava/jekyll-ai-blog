---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Set Git Bash as VS Code Terminal
translated: false
type: note
---

Question: In VS Code on Windows, how to set Git Bash as a profile of the terminal?

Answer:

There are two main ways to set Git Bash as a terminal profile in Visual Studio Code on Windows: the easiest GUI method (recommended) and manually editing the settings.json file.

### Easiest Method (Using the Built-in Selector)

1. Open the integrated terminal in VS Code by pressing `Ctrl + `` (backtick) or going to **Terminal > New Terminal**.
2. In the terminal panel, click the dropdown arrow next to the "+" icon (or the current terminal name).
3. Select **Select Default Profile** from the menu.
4. Choose **Git Bash** from the list of available profiles (it should appear if Git for Windows is installed).
5. Close and reopen the terminal (or restart VS Code) for the change to take effect.

Git Bash is automatically detected by VS Code if Git is installed in the default location.

### Manual Method (Editing settings.json)

If Git Bash does not appear in the dropdown or you need custom configuration:

1. Open the Command Palette with `Ctrl + Shift + P`.
2. Type and select **Preferences: Open Settings (JSON)**.
3. Add or modify the following lines in your user settings.json:

```json
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

VS Code usually auto-detects Git Bash, so this single line is often sufficient. Restart VS Code after saving.

If it's not detected (rare), explicitly define the profile:

```json
"terminal.integrated.profiles.windows": {
    "Git Bash": {
        "path": "C:\\Program Files\\Git\\bin\\bash.exe",
        "icon": "terminal-bash"
    }
},
"terminal.integrated.defaultProfile.windows": "Git Bash"
```

Adjust the path if your Git installation is elsewhere (common paths: `C:\\Program Files\\Git\\bin\\bash.exe` or `C:\\Program Files (x86)\\Git\\bin\\bash.exe`).

**Notes**:

- Use `bash.exe` (not `git-bash.exe`) for proper integration.
- Adding `--login` to args can help load your ~/.bash_profile if needed, but it's optional.
- After changes, open a new terminal to see Git Bash as the default.

This will make Git Bash appear as a selectable profile and set it as the default when opening new terminals.

References:

- [https://code.visualstudio.com/docs/terminal/profiles](https://code.visualstudio.com/docs/terminal/profiles)
- [https://stackoverflow.com/questions/42606837/how-do-i-use-bash-on-windows-from-the-visual-studio-code-integrated-terminal](https://stackoverflow.com/questions/42606837/how-do-i-use-bash-on-windows-from-the-visual-studio-code-integrated-terminal)
- [https://bobbyhadz.com/blog/vscode-change-default-terminal](https://bobbyhadz.com/blog/vscode-change-default-terminal)
- [https://neutrondev.com/vs-code-integrate-git-bash-default-terminal/](https://neutrondev.com/vs-code-integrate-git-bash-default-terminal/)
