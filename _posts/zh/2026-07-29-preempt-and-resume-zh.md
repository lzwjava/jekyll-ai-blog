---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 抢占并恢复
translated: true
type: note
---

**Preempt** = 中断或抢占当前正在运行的任务，以便优先执行其他操作。

常见用途：

**操作系统/调度：** 高优先级进程中断 CPU 上正在运行的低优先级进程。
```c
// 抢占式多任务：操作系统调度器可以暂停正在运行的进程，
// 即使它尚未完成，以便将 CPU 时间分配给其他进程
if (higher_priority_task_ready) {
    save_context(current_task);
    switch_to(higher_priority_task);
}
```

**Kubernetes：** Pod 抢占——当资源紧张时，高优先级 Pod 驱逐低优先级 Pod 以获取调度机会。

**通用英语：** "to preempt a question" = 在别人提问之前抢先回答，即先发制人。

**GPU/训练上下文（与您相关）：** 可抢占/Spot 实例——云服务提供商可以抢占（终止）您在 Spot GPU 上的训练任务，以回收容量给更高付费的客户。这就是在 Spot MI300X/A100 实例上训练时检查点机制至关重要的原因——如果被抢占，您可以从最后一个检查点恢复，而不是丢失整个训练过程。