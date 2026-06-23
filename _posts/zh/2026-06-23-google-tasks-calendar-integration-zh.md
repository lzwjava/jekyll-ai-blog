---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Google Tasks与日历集成
translated: true
type: note
---

是的，Google Tasks 和 Google Calendar 原生集成。你在 Google Tasks 应用（或 iOS 上的 Tasks 小组件）中创建的任务会以绿色对勾形式显示在 Google Calendar 中——它们会出现在你设定的截止日期上，并且可以在 Pixel 设备上与日历事件一起内联查看。

关于集成，有几个值得了解的点：

- 任务仅在设置了截止日期时才会出现在 Calendar 中。没有截止日期 = 在 Calendar 中不可见。
- 任务显示在当天的顶部（全天区域），而不是作为时间块，除非你同时设定了具体时间。
- 在 Calendar 中完成任务会同步将 Tasks 中的任务标记为完成，反之亦然——双向同步。
- 绿色与日历事件颜色不同，便于在视觉上区分“待办事项”和“会议/活动”。

在 Pixel 设备上使用默认的 Google Calendar 应用时效果尤为清晰，因为 Google 的 Material You 主题会在日视图中为任务赋予统一的绿色对勾样式。

如果你围绕这一点构建自动化——Google Tasks 有 REST API (`tasks.googleapis.com`)，Calendar 也有。你可以通过 CLI 代理（如 `ww`、`zz` 等）以编程方式创建带截止日期的任务，它们会自动出现在 Calendar 中。如果你希望将来自代理工作流的提醒或待办事项导入到日常视图中，这值得考虑。