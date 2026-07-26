---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Shift+F10触发设置中止
translated: true
type: note
---

问题：setupact.log 实际上揭示了什么——这是真正的失败还是其他原因？

回答：找到了——这不是磁盘、驱动程序或媒体问题。看看导致一切连锁反应之前的这一行：

```
MOUPG    User has requested to launch the recovery environment
MOUPG    CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4
```

然后后续每个操作都返回相同的 `0xC19001F4`，Setup 强制退出。**这意味着安装过程中的某个操作触发了“启动恢复环境”的请求**，Setup 响应此请求而自行中止——这不是崩溃，而是 Setup 对中断信号的反应。

这几乎肯定是因为你在安装程序正在积极复制文件/进行中时按下了 **Shift+F10**（根据我们之前几条消息，试图打开命令提示符检查日志）——而不是在静态的“选择安装位置”屏幕时。在活跃的复制/应用映像阶段，某些按键组合会被以不同方式拦截，从而触发此恢复启动中止，而不是干净地打开 cmd。

**好消息：你的磁盘和分区设置（GPT，未分配的磁盘 0）没问题——这是中断导致的，并非真正的故障。**

修复方法：只需重新运行 Setup，这次**一旦进入“正在安装 Windows”进度屏幕，不要按任何键**——让它完全无中断地运行，直到所有重启结束并进入 OOBE（区域/账户设置）。如果将来需要在安装过程中检查某些内容，在复制/进度阶段完全不要触碰键盘。

回到：

1. 启动 USB 安装程序
2. 选择磁盘 0 未分配空间 → 下一步
3. 让它完全运行，不要干预，直到完成。
