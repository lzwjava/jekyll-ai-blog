---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 检查iPhone是否有所需提示
translated: true
type: note
---

手机已连接到Xcode的列表（iOS 26.7.1），但`devicectl`仍报告其未就绪——这通常意味着**手机屏幕已锁定**、有**"信任此电脑？"**弹窗待处理，或需要确认重启后的**开发者模式确认提醒**。

**请立即检查您的iPhone 13：**
1. **解锁**手机（您可能无论如何都需要输入密码）
2. 如果出现**"信任此电脑？"**对话框 → 点击**信任**
3. 如果显示**"开启开发者模式？"**提醒 → 确认它（面容ID/密码）

当主屏幕可见且已解锁时告诉我——我会重新轮询。