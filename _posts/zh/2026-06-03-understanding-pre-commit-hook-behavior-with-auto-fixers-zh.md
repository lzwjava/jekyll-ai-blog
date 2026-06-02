---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解带有自动修复器的预提交钩子行为
translated: true
type: note
---

我看到摩擦——但重点是：`trailing-whitespace` 和 `end-of-file-fixer` **已经自动修复**了。"Failed" 状态只是说明它们修改了文件。Pre-commit 出于设计目的有意中止提交，因此你必须 `git add` 然后再次提交。

在 `.pre-commit-config.yaml` 中**没有配置标志**能让 pre-commit 自动暂存并继续——这是 pre-commit 作者有意为之的安全选择。它不像 `ruff --fix` 那样修复后同一个钩子会重新检查；对于 pre-commit-hooks 的修复器，"修复"就是修改，任何修改都意味着失败。

所以实际选项是：

1. **编辑器端修复（推荐）**——让你的编辑器在保存时自动去掉行尾空格并确保文件末尾有换行。这样这些钩子就不会触发。我可以添加一个 `.editorconfig` 文件，让 VS Code / 大多数编辑器自动完成此操作。
2. **移除这两个烦人的钩子**——从 `.pre-commit-config.yaml` 中删除 `trailing-whitespace` 和 `end-of-file-fixer`。它们主要捕获编辑器的粗心行为；如果你的编辑器处理好了，它们就是多余的。
3. **包装脚本**——一个 `git commit` 包装器，先运行 `pre-commit run`，然后 `git add -u`，再提交。额外的组件较多，能工作但存在于配置文件之外。

你想要哪个？我的选择是 #1（editorconfig）+ 保留钩子作为安全网——这样你就不会遇到双重提交，但来自其他机器的提交仍然会被清理。