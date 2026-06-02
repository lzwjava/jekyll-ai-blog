---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Angular CLI Shell 挂起
translated: true
type: note
---

完成。以下是摘要：

**根本原因：** `~/.zshrc` 第23行中的 `source <(ng completion script)`。Angular CLI 的 `ng completion script` 虽然输出了正确的补全文本，但 Node 进程从未退出——它一直挂起。每个新的 Ghostty 标签页（或任何终端）都要等待 60 秒以上才能完成此操作。

**已应用的修复：**
1. 将补全脚本静态保存到 `~/.ng-completion.zsh`
2. 将动态的 `source <(ng completion script)` 替换为 `source ~/.ng-completion.zsh`

**结果：** Shell 启动时间从 **60 秒以上 → 0.25 秒**。现在打开新的 Ghostty 标签页应该可以瞬间完成。

注意：如果你添加了新的 Angular CLI 命令并需要更新补全，只需重新运行 `timeout 5 ng completion script > ~/.ng-completion.zsh`（补全内容很少变化）。
