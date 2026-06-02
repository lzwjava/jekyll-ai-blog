---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在VS Code中排除忽略的文件
translated: true
type: note
---

你可以通过调整 `settings.json` 中的三项设置，让“转到文件”（快速打开，Ctrl + P）包含位于 `.gitignore` 中的文件：

1. **让搜索忽略你的 `.gitignore` 规则**

   ```jsonc
   "search.useIgnoreFiles": false,      // 不遵循 .gitignore
   "search.useGlobalIgnoreFiles": false // 不遵循全局 gitignore
   ```
2. **确保你的排除规则不会隐藏这些文件**
   默认情况下 VS Code 会将 `files.exclude` 中的所有模式继承到 `search.exclude`。如果你曾手动排除了 `.gitignore` 中的目录，请重新启用它们：

   ```jsonc
   "search.exclude": {
     "**/.git": false,          // 要索引 .git 目录（如需要）
     "**/.gitignore": false     // 绝对不要隐藏 .gitignore 文件本身
     // …其他需要覆盖的匹配模式
   }
   ```
3. **重新加载窗口**
   保存用户或工作区设置后，运行 **开发者：重新加载窗口** (⇧ ⌘ P → “Reload Window”)，让文件索引器获取更改。

现在当你按下 Ctrl + P 时，就能按名称看到*所有*文件——无论是否被忽略。（[stackoverflow.com][1]）

[1]: https://stackoverflow.com/questions/62855190/how-do-you-include-git-ignored-files-in-vscode-quick-search?utm_source=chatgpt.com "How do you include git ignored files in VSCode quick search"
