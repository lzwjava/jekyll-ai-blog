---
audio: false
generated: true
image: false
lang: en
layout: post
title: OS Process Scheduling Explained
translated: false
type: note
---

Question: What is Process Scheduling (进程的调度)?

Answer:

**Process Scheduling** is the mechanism by which an operating system decides which process gets to use the CPU at any given moment. Since a CPU can only execute one process at a time (per core), the OS must efficiently multiplex CPU time among all ready processes.

---

### Key Concepts

**Scheduler Types (by time horizon):**

- **Long-term scheduler** – decides which processes are admitted into the ready queue (job scheduler)
- **Short-term scheduler** – decides which ready process runs next on the CPU (CPU scheduler, runs most frequently)
- **Medium-term scheduler** – handles swapping processes in/out of memory

---

### Scheduling Criteria

| Criterion | Goal |
| --- | --- |
| CPU Utilization | Keep CPU as busy as possible |
| Throughput | Maximize processes completed per unit time |
| Turnaround Time | Minimize total time from submission to completion |
| Waiting Time | Minimize time spent in the ready queue |
| Response Time | Minimize time until first response |

---

### Common Scheduling Algorithms

1. **FCFS (First-Come, First-Served)** – simplest; non-preemptive; suffers from the *convoy effect*
2. **SJF (Shortest Job First)** – optimal average waiting time; hard to predict burst time
3. **SRTF (Shortest Remaining Time First)** – preemptive version of SJF
4. **Round Robin (RR)** – each process gets a fixed time quantum; fair and widely used
5. **Priority Scheduling** – higher priority runs first; can cause *starvation* (solved by aging)
6. **Multilevel Queue** – separate queues per process type (foreground/background)
7. **Multilevel Feedback Queue (MLFQ)** – processes can move between queues based on behavior; used in modern OSes (Linux, Windows)

---

### Preemptive vs. Non-Preemptive

| | Non-Preemptive | Preemptive |
| --- | --- | --- |
| Definition | Process keeps CPU until it voluntarily releases | OS can forcibly take CPU away |
| Risk | Long processes block others | Requires context-switch overhead |
| Example | FCFS, SJF | RR, SRTF |

---

### Context Switch (上下文切换)

When the scheduler switches from one process to another, it performs a **context switch**: saving the current process's state (registers, PC, stack pointer) into its PCB (Process Control Block) and loading the next process's state. This has a small but real overhead cost.

---

### Linux Scheduler (CFS – Completely Fair Scheduler)

Modern Linux uses the **CFS**, which aims to give every process a "fair" share of CPU time using a red-black tree ordered by *virtual runtime* (vruntime). The process with the smallest vruntime always runs next.

References:

- [Operating System Concepts (Silberschatz) – Chapter 5: CPU Scheduling](https://os.ecci.ucr.ac.cr/slides/Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf)
- [Linux CFS Scheduler – Kernel Docs](https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html)
- [Process Scheduling – OSDev Wiki](https://wiki.osdev.org/Scheduling_Algorithms)
