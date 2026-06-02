---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工具切换过渡别名
translated: true
type: note
---

**问题：** 你在 zprofile 中添加了 `alias code=zed` 作为 VS Code 的轻量替代方案——这是个好主意吗？一般来说，在电脑上改变使用习惯时，采用一段过渡期（比如将旧命令别名指向新工具）是否明智？

**回答：**

是的，这两个想法都很有道理。

**`alias code=zed` — 实用且简洁**

Zed 确实比 VS Code 更轻量。它用 Rust 编写，通过 GPUI 实现 GPU 加速，几乎没有 Electron 的开销。对于你的 MacBook Air M2（仅剩 54 GB 空闲空间，且可能因 LLM 工作负载而面临内存压力）来说，这一点很重要。这个别名让你的肌肉记忆（`code .`）继续生效，而底层工具已经变得更快速。

你还可以在 `.zprofile` 中进一步优化：

```zsh
alias code=zed
alias c=zed          # 更短的别名
alias zz="zed ."     # 直接打开当前目录
```

或者如果你想要回退逻辑：

```zsh
code() {
  if command -v zed &>/dev/null; then
    zed "$@"
  else
    /usr/local/bin/code "$@"  # 真正的 VS Code 作为回退
  fi
}
```

**过渡期使用别名 — 是的，这是一种常见的模式**

本质上这是一种垫片策略。你在习惯跟上之前，通过命令层来重定向行为。和以下做法原理相同：

- `alias python=python3`（Python 2→3 迁移时代）
- `alias vim=nvim`（切换编辑器时）
- `alias grep='rg'`（转向 ripgrep 时）
- 内核的 `compat` 层、macOS Rosetta、Linux 上的 `update-alternatives`

关键点在于：**习惯存在于动作记忆，而非你的意识中**。别名在执行层拦截，这样你就不必在头脑重新训练时与手指作斗争。几周后，你可以去掉别名，直接输入 `zed`——别名已经完成了它的使命。

这也是为什么你在切换编辑器时会保留相同的快捷键，或者为什么 Zed 开箱即支持 VS Code 按键映射。缩小新旧习惯之间的差异，能降低切换所需的激活能量。

总的来说，这是个聪明的做法。
