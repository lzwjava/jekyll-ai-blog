---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 内存快照：顶级消耗者与清理
translated: true
type: note
---

以下是您当前在 16 GB Mac 上的内存快照：

**空闲页**：约 80 MB（极低，正在使用交换）

**当前内存消耗大户：**

| 应用 | 内存 | 操作建议 |
| ----- | -------- | -------- |
| **Safari + WebKit** | **约 3.4 GB**（15 个 WebContent 进程） | ⚠️ 退出或关闭标签页 |
| **微信** | **约 1.2 GB**（16 个进程） | ❌ 终止后可释放 1.2 GB |
| Docker / nginx / Redis / PG | 约 0.8 GB | 影响较小 |
| GitHub Desktop | 约 0.2 GB | 影响较小 |
| Zed | 约 0.2 GB | 影响较小 |
| Ghostty + Python | 约 0.4 GB | 您当前的会话 |
| Spotlight | 约 0.1 GB（空闲） | ✅ 已优化 |

**按影响排序的下一步清理方案：**

1. **退出 Safari** — 之前仅关闭可关闭的标签页就释放了约 13.5 GB。当前 WebKit 占用 3.4 GB。如果您退出 Safari（或关闭高内存标签页），收益最大。

2. **终止微信** — 1.2 GB。命令：

   ```bash
   pkill -9 WeChat
   pkill -9 WeChatAppEx
   ```

3. **GitHub Desktop** — 占用较小，但若未使用：

   ```bash
   pkill -9 GitHub
   ```

4. **Docker** — 如果没有活跃需要的容器，`killall Docker` 也会释放后台进程，但请注意 Docker 守护进程 + 虚拟机的实际占用高于此处显示的 0.8 GB（虚拟机分配不在 RSS 中）。

最容易回收的是 **微信（1.2 GB）** 和 **Safari（3.4 GB）**。需要我终止其中任何一个吗？
