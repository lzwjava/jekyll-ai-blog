---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端优先栈与性能洞察
translated: true
type: note
---

很酷的配置！以终端为主、CLI 为重、Zed 作为编辑器——这是一个简洁的技术栈。Ghostty 确实很棒（GPU 加速、启动快、配置友好）。

从你的 `top` 输出中观察到一些值得注意的地方：

**cfprefsd 消耗了 36% + 30% 的 CPU**——两个实例。这是 macOS 偏好设置守护进程在异常运行，很可能是有应用在不断循环读写 `UserDefaults`。微信是常见的嫌疑犯（注意那 68 分钟的 CPU 时间）。你可以尝试：

```bash
# 查看哪个进程最常调用 cfprefsd
sudo fs_usage -f filesys cfprefsd 2>/dev/null | grep plist | head -30
```

**内存紧张**——已使用 15G，仅剩 115M，交换出 33K。压缩器工作繁重（压缩了 5G）。Ghostty 占用 368M，微信 764M，Safari 262M，WindowServer 678M——内存基本满了。在 M2 16GB 机型上，对于这种多应用负载，这已是上限。

**WindowServer 的 48% CPU 占用**即使在活跃桌面环境中也很高——可能是透明度/模糊效果，或高刷新率外接显示器。如果还没设置建议检查：系统设置 → 辅助功能 → 减少动态效果 + 减少透明度。

关于终端优先的趋势：完全同意。坚持 CLI 原生开发的工程师迭代速度更快——反馈循环更快，一切可脚本化，无需管理 GUI 状态。Zed 的特别之处在于它专为键盘优先使用而设计，并集成了原生 AI 功能（不过在我看来，对于繁重的代理工作，终端中的 Claude Code 更胜一筹）。你正在走的这条路——Ghostty + Zed + CLI 代理——正是认真做 AI 的工程师们所选择的。