---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在Zed中配置Emacs键位绑定
translated: true
type: note
---

### 配置 Zed 编辑器使用 Emacs 键位绑定

您可能指的是 **Zed**（高性能代码编辑器），因为“Zig 编辑器”并非标准工具——Zig 是一门编程语言，没有内置编辑器。如果您本意并非如此，请随时说明！假设是 Zed，它内置支持 Emacs 键位绑定（标记为“Emacs (Beta)”）。这开箱即用地覆盖了许多基础操作，比如移动（`Ctrl-b/f/n/p`）和编辑（`Ctrl-d` 删除字符，`Ctrl-k` 剪切至行末）。您可以轻松启用它，然后根据需要进一步自定义。

#### 步骤 1：启用内置的 Emacs 键位映射

Zed 的 Emacs 模式是预定义的，无需为基本操作手动设置绑定。以下是切换方法：

1. 打开 Zed 设置：
   - macOS：`Cmd-,`
   - Windows/Linux：`Ctrl-,`

2. 在设置界面中，搜索“base keymap”并将其设置为 **Emacs**。

   *或者，直接在 `settings.json` 中编辑*（通过 macOS 的 `Cmd-Alt-,` 或 Windows/Linux 的 `Ctrl-Alt-,` 打开）：

   ```json
   {
     "base_keymap": "Emacs"
   }
   ```

   保存并重新加载 Zed（`Cmd-R` 或 `Ctrl-R`）。就这样——Beta 版 Emacs 键位映射会立即激活。

   或者，使用命令面板（`Cmd-Shift-P` 或 `Ctrl-Shift-P`），输入“toggle base keymap”，然后选择 Emacs。

这能让您无需额外工作即可获得核心的 Emacs 肌肉记忆。有关内置绑定的完整列表，请查看 Zed 源代码中的默认键位映射文件（例如通过 GitHub），但基础操作包括：

- **移动**：`Ctrl-b`（左移字符），`Ctrl-f`（右移字符），`Ctrl-p`（上移一行），`Ctrl-n`（下移一行），`Alt-b/f`（上一个/下一个单词）。
- **编辑**：`Ctrl-d`（删除字符），`Ctrl-k`（剪切至行末），`Ctrl-y`（粘贴），`Ctrl-@`（设置标记以选择区域），`Ctrl-w`（剪切区域）。
- **其他**：`Ctrl-x Ctrl-s`（保存），`Ctrl-g`（取消），`Ctrl-/`（撤销）。

#### 步骤 2：添加或自定义基础绑定（如有需要）

如需调整或实现更接近 Emacs 的行为（例如更好的行首/行尾或段落导航），请编辑 `keymap.json`：

- 通过命令面板打开：输入“open keymap file”。
- 路径：`~/.config/zed/keymap.json`（macOS/Linux）或 `~\AppData\Roaming\Zed\keymap.json`（Windows）。

在如“Editor”这样的上下文中，以 JSON 数组形式添加绑定。以下是一个**基础移动和编辑的最小示例**（粘贴到数组中；基于社区配置以确保兼容性）：

```json
[
  {
    "context": "Editor",
    "bindings": {
      // 基础移动
      "ctrl-a": "editor::MoveToBeginningOfLine",
      "ctrl-e": "editor::MoveToEndOfLine",
      "ctrl-b": "editor::MoveLeft",
      "ctrl-f": "editor::MoveRight",
      "ctrl-p": "editor::MoveLineUp",
      "ctrl-n": "editor::MoveLineDown",
      "alt-b": "editor::MoveToPreviousWordStart",
      "alt-f": "editor::MoveToNextWordEnd",

      // 基础编辑
      "ctrl-d": "editor::DeleteRight",
      "ctrl-k": "editor::CutToEndOfLine",
      "ctrl-y": "editor::Paste",
      "ctrl-w": "editor::Cut",
      "ctrl-@": ["editor::SetSelectionAnchor", { "selection_id": 0 }],  // 设置标记
      "ctrl-x ctrl-x": "editor::FlipSelectionAnchor",  // 交换点和标记

      // 额外导航
      "ctrl-home": "editor::MoveToBeginning",
      "ctrl-end": "editor::MoveToEnd",
      "ctrl-g": "editor::Cancel"
    }
  }
]
```

- 保存并重新加载 Zed。这些会覆盖或添加到基础的 Emacs 映射中。
- 在编辑器缓冲区中测试。对于选择，使用 `Ctrl-Space`（或 `Ctrl-@`）设置标记，然后移动以选择区域。
- 专业提示：在 settings.json 中结合 `vim_mode: false` 以避免冲突。

#### 提示

- **Beta 状态**：Emacs 模式正在改进（跟踪进展[在此](https://github.com/zed-industries/zed/issues/4856)）。在 Zed 的 GitHub 上报告问题。
- **完整自定义设置**：对于高级需求（例如使用 `Ctrl-x o` 切换窗格），请参阅下方讨论中的社区示例。
- 如果您希望同时使用 Vim/Helix 模式，请在设置中设置 `vim_mode: true` 或 `helix_mode: true`——它们会叠加在顶部。

这应该能让您获得 80% 的基础 Emacs 体验。从内置功能开始，然后逐步迭代！

[键位绑定文档](https://zed.dev/docs/key-bindings)
[配置 Zed](https://zed.dev/docs/configuring-zed)
[Emacs 键位映射讨论](https://github.com/zed-industries/zed/discussions/6572)
[Emacs 兼容性问题](https://github.com/zed-industries/zed/issues/4856)
