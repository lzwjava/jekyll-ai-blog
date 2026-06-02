---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 当你需要时间机器时，它却失灵了
translated: true
type: note
---

**Question:** 关于 macOS 中的 Time Machine，有哪些冷门或非主流的观点？

**Answer:**

以下是一些关于 Time Machine 的**冷门**或具有争议性的观点/想法。尽管许多人仍将其视为较好的内置备份系统，但在论坛、支持帖和技术讨论中（尤其是资深用户或挑剔的用户之间），经常会出现以下声音：

- **Time Machine 在实际使用中不可靠且脆弱**
  许多长期用户声称它“在出问题前一切都好”，经常出现静默损坏（silent corruption）、晦涩的错误提示、备份无故被标记为损坏以及删除失败。有些人说，只有在你拼命想要恢复数据时，才会发现备份已经坏了。

- **它被过度神化了，人们高估了它的优越性/安全性**
  华丽的星空恢复界面备受赞誉，但批评者认为，与第三方工具（如 CCC、SuperDuper!、rsync 等）相比，其实际可靠性平庸。有些人甚至认为，对于重要数据，仅依赖 Time Machine 简直是“自我毁灭”。

- **不应将 Time Machine 作为唯一的/首要的备份方案**
  一个相当强硬的少数派观点建议完全关闭它，或者仅将其作为二级备份。他们更倾向于使用可引导的克隆（Carbon Copy Cloner / SuperDuper!），因为 Time Machine 的运作机制不够透明，难以验证，并且在最近的 macOS 版本中，其进行全系统灾难恢复的表现较差。

- **在某些 macOS 更新（如 Sonoma、Sequoia 等）后，Time Machine 基本处于损坏状态**
  在大版本发布后，投诉量激增——iCloud Drive 同步导致备份永久阻塞、Apple Silicon 上的首次备份失败、自 Catalina/APFS 更改以来的严重降速、加密异常，以及频繁需要彻底抹除并重建备份。

- **“设置后即忘”的承诺具有误导性**
  许多用户表示，实际上你需要每月手动验证备份、仔细排除特定文件夹、在 macOS 大版本升级期间密切关注，并接受它偶尔需要数小时或数天时间来“修复”或从头开始备份的现实。

- **在最需要的时候，从 Time Machine 恢复数据往往会失败**
  有大量报告指出，尽管最近的备份显示“成功”，但用户仍无法恢复关键文件或系统——要么是恢复过程卡死，要么是权限问题导致一切崩溃，或者旧版本的文件根本无法访问/使用。

- **它不是真正的归档方案**
  在普通用户中一个不具代表性的观点是：Time Machine 会在空间不足时激进地清除旧备份，它从未被设计用于长期归档。如果你想保留 5 到 10 年前的文件，它是错误的工具。

这些观点与“它既棒又简单”的主流共识相比确实属于少数，但在 Reddit、MacRumors、Apple Discussions、Hacker News 和技术博客中始终存在——特别是来自高级用户、开发者以及多次遭遇失败经历的人。

**References:**

- [https://www.reddit.com/r/mac/comments/1og6yop/time_machine_is_completely_unreliable_in_2025](https://www.reddit.com/r/mac/comments/1og6yop/time_machine_is_completely_unreliable_in_2025)
- [https://forums.macrumors.com/threads/i-hate-time-machine.2167090](https://forums.macrumors.com/threads/i-hate-time-machine.2167090)
- [https://news.ycombinator.com/item?id=36473209](https://news.ycombinator.com/item?id=36473209)
- [https://discussions.apple.com/thread/255407478](https://discussions.apple.com/thread/255407478)
- [https://forums.macrumors.com/threads/is-there-a-point-in-still-using-time-machine.2394703](https://forums.macrumors.com/threads/is-there-a-point-in-still-using-time-machine.2394703)
