---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 操作系统进程调度详解
translated: true
type: note
---

问题：What is Process Scheduling (进程的调度)?

答案：

**Process Scheduling** 是操作系统决定哪个进程在给定时刻使用CPU的机制。由于CPU（每核）一次只能执行一个进程，操作系统必须高效地在所有就绪进程间复用CPU时间。

---

### 关键概念

**调度器类型（按时间跨度）：**

- **Long-term scheduler** – 决定哪些进程被允许进入就绪队列（job scheduler）
- **Short-term scheduler** – 决定哪个就绪进程接下来在CPU上运行（CPU scheduler，运行最频繁）
- **Medium-term scheduler** – 处理进程在内存和外存之间的交换

---

### 调度标准

| Criterion | Goal |
| --- | --- |
| CPU Utilization | 尽可能让CPU保持忙碌 |
| Throughput | 最大化每单位时间完成的进程数 |
| Turnaround Time | 最小化从提交到完成的总时间 |
| Waiting Time | 最小化在就绪队列中花费的时间 |
| Response Time | 最小化直到首次响应的时间 |

---

### 常见调度算法

1. **FCFS (First-Come, First-Served)** – 最简单；非抢占；存在 *convoy effect*
2. **SJF (Shortest Job First)** – 最优平均等待时间；难以预测 burst time
3. **SRTF (Shortest Remaining Time First)** – SJF的抢占版本
4. **Round Robin (RR)** – 每个进程获得固定时间片；公平且广泛应用
5. **Priority Scheduling** – 优先级高的先运行；可能导致 *starvation*（通过aging解决）
6. **Multilevel Queue** – 按进程类型分隔队列（foreground/background）
7. **Multilevel Feedback Queue (MLFQ)** – 进程可根据行为在队列间移动；用于现代操作系统（Linux, Windows）

---

### 抢占 vs. 非抢占

| | Non-Preemptive | Preemptive |
| --- | --- | --- |
| 定义 | 进程自愿释放CPU之前一直保持 | 操作系统可以强制取走CPU |
| 风险 | 长进程阻塞其他进程 | 需要context-switch开销 |
| 示例 | FCFS, SJF | RR, SRTF |

---

### Context Switch (上下文切换)

当调度器从一个进程切换到另一个时，它执行一次 **context switch**：将当前进程的状态（registers, PC, stack pointer）保存到其PCB (Process Control Block)中，并加载下一个进程的状态。这会产生一个虽小但实际的开销。

---

### Linux Scheduler (CFS – Completely Fair Scheduler)

现代Linux使用 **CFS**，它旨在通过按 *virtual runtime* (vruntime) 排序的红黑树给每个进程“公平”的CPU时间份额。vruntime最小的进程总是在下一次运行。

参考文献：

- [Operating System Concepts (Silberschatz) – Chapter 5: CPU Scheduling](https://os.ecci.ucr.ac.cr/slides/Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf)
- [Linux CFS Scheduler – Kernel Docs](https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html)
- [Process Scheduling – OSDev Wiki](https://wiki.osdev.org/Scheduling_Algorithms)
