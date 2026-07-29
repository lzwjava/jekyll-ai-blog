---
audio: false
generated: true
image: false
lang: en
layout: post
title: Preempt and Resume
translated: false
type: note
---

**Preempt** = to interrupt or take priority over something that's currently running, in order to do something else first.

Common uses:

**OS/scheduling:** A higher-priority process interrupts a lower-priority one running on the CPU.
```c
// preemptive multitasking: OS scheduler can pause a running process
// even if it hasn't finished, to give CPU time to another process
if (higher_priority_task_ready) {
    save_context(current_task);
    switch_to(higher_priority_task);
}
```

**Kubernetes:** pod preemption — a higher-priority pod evicts a lower-priority one to get scheduled when resources are tight.

**General English:** "to preempt a question" = answer it before someone asks, i.e. act first to prevent something.

**GPU/training context (relevant to you):** preemptible/spot instances — cloud providers can preempt (kill) your training job on spot GPUs to reclaim capacity for higher-paying customers. This is why checkpointing matters when training on spot MI300X/A100 instances — if preempted, you resume from the last checkpoint instead of losing the run.
