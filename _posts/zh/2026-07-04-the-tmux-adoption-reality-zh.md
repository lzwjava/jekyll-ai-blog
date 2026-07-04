---
audio: false
generated: true
image: false
lang: zh
layout: post
title: tmux 采用现实
translated: true
type: note
---

**问题：** 真的有很多人用 tmux 来切换项目吗，还是说这只是小众做法？

让我看看实际采用情况的数据。**回答：**

实话实说：这是一群声音很大的少数派——而非大多数。下面详细分析谁在用以及为什么用，这样你就能判断自己是否属于这个群体（你基本算）。

**哪些人重度使用 tmux：**

1. **任何通过 SSH 连接远程机器的人** —— 这是 killer 用例，也恰好是*你的*用例。当你 SSH 进入 RTX 4070 机器或 MI300X 实例时，tmux 几乎是必需品：终端会话因 SSH 断开而丢失，这种痛苦会促使大多数人入坑。你的训练任务在你合上 MacBook Air 后仍能继续运行。没有 tmux（或 `nohup`/`systemd`），WiFi 断连就会导致任务失败。

2. **终端优先的开发者** —— vim/neovim 用户、后端/基础架构人员、SRE。tmux 在 GitHub 上有超过 37k 星标，直到 2026 年还有人写文章讨论它，所以它并没有消亡。但它与 neovim 社群高度相关——这算是一种亚文化。

3. **新浪潮：CLI 代理用户。** 这是 2025–2026 年有趣的变化。运行 Claude Code、aider 或自定义代理（比如你的 `ww`/`iclaw`/`zz`）的人越来越多地使用 tmux 来并行运行多个长期存在的代理会话——每个项目一个代理，分离后定期检查。如果你在构建 CLI 代理，tmux 会话基本就是你的进程管理器。

**哪些人不用：**

- **大多数开发者，说实话。** 大部分人活在 VS Code / JetBrains 的集成终端 + IDE 工作区切换里。一个搜索结果完美体现了这一点：tmux 用户跟队友结对编程时，队友问“这是什么鬼，你甚至不能在这里正常粘贴”。这就是普通开发者的反应。
- **没有远程需求的现代终端用户。** Kitty、Ghostty 和 Alacritty 自带标签页、分屏等功能——而你用的 Warp 本身就支持标签页、分屏和保存会话。对于*本地*工作，Warp 已经提供了 tmux 70% 的功能。

**所以针对你的实际答案：**

- **本地在 MacBook Air 上**：你并非必须用 tmux——Warp 每个项目的标签页完全够用。一个 Warp 标签页 = 一个项目，这就是我描述的轻量版方案。
- **远程（4070 机器、MI300X 实例）**：是的，必须用 tmux，没得商量。这时候“很多人”实际上等于“几乎所有认真干活的人”。模式如下：

```bash
# 在远程机器上
tmux new -s train      # 在此启动训练任务，然后按 Ctrl-b d 分离
tmux new -s agent      # 长期运行的 CLI 代理

# 几天后，从你的 MacBook Air 上
ssh lzw@192.168.x.x -t "tmux attach -t train"
```

- **值得了解的替代方案**：`zellij`（Rust 编写，快捷键易发现）是现代的 tmux 竞争者——默认配置更友好，会话模型相同。鉴于你对 Rust 的兴趣，花 20 分钟了解它很值得。

你之前问题中的元观点仍然成立：具体机制不重要（tmux 会话、Warp 标签页、虚拟桌面）——重要的是*每个项目一个命名的上下文*，而不是 30 个无名终端。tmux 只是那个同时能应对断连的机制，这也是为什么重度远程用户——你所处的群体——会汇聚到它上面。

**参考资料：**

- [Why I love tmux — DEV Community](https://dev.to/antjanus/why-i-love-tmux-12ak)
- [How Tmux Supercharged My Development Workflow — Medium](https://devprogramming.medium.com/how-tmux-supercharged-my-development-workflow-5b9dcf004789)
- [Why You Should Finally Learn Tmux (Yes, Even in 2026) — Medium](https://medium.com/quick-programming/why-you-should-finally-learn-tmux-yes-even-in-2026-4dc9478bde30)
- [Tmux Tutorial: The Complete Developer Workflow Guide (2026) — DEV Community](https://dev.to/_d7eb1c1703182e3ce1782/tmux-tutorial-the-complete-developer-workflow-guide-2026-33b3)
