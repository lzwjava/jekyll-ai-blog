---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Parallel I/O: Threads Outperform Processes"
translated: false
type: note
---

Good question. Let me break it from first principles.

**The GIL (Global Interpreter Lock)**

CPython has one lock that prevents two Python bytecode instructions from running simultaneously on multiple CPU cores. This is the famous GIL. It means:

- Threading: multiple threads share ONE process, ONE memory space, but only ONE thread runs Python code at a time
- Multiprocessing: each process has its OWN Python interpreter, OWN memory, runs on its OWN CPU core

**What happens during `git pull`?**

Your Python code calls `subprocess.run(["git", "pull", ...])`. This does:

```
Python thread → fork() → exec("git") → git connects to GitHub → waits on socket → data arrives → returns to Python
```

The critical part: while git is running as a subprocess, your Python thread is **blocked on `os.waitpid()`** — it's sleeping in the kernel, NOT executing Python bytecode. When a thread sleeps in the kernel, **it releases the GIL**. Other threads can run freely.

So with 8 threads doing git pull:

```
Thread 1: fork git → sleep (GIL released) ──────────── wake up → done
Thread 2: fork git → sleep (GIL released) ──────────── wake up → done
Thread 3: fork git → sleep (GIL released) ────────── wake up → done
...
All 8 git subprocesses run in parallel on 8 OS processes
```

The GIL doesn't matter because your Python threads are sleeping 99% of the time. They only briefly wake up to record the result.

**Why multiprocessing is wasteful here:**

```
Multiprocessing: 8 full Python interpreters in memory
  - Each ~30-50MB RSS
  - Pickle/unpickle data between processes (serialization overhead)
  - Spawn cost: fork() + import world

Threading: 8 lightweight threads in ONE process
  - Each ~8KB stack
  - Shared memory (no serialization)
  - Spawn cost: just create a thread
```

For network I/O, both give the same parallelism (the OS schedules 8 git processes either way). But threads are 100x cheaper in memory and startup.

**When would you NEED multiprocessing?**

When the bottleneck is CPU — Python bytecode executing in a tight loop. The GIL prevents two threads from executing bytecode simultaneously. Example:

```python
# This does NOT speed up with threads — GIL blocks parallel execution
def cpu_heavy(n):
    return sum(i * i for i in range(n))

# This DOES speed up with multiprocessing — each process has its own GIL
with ProcessPoolExecutor(8) as pool:
    pool.map(cpu_heavy, [10**7] * 8)
```

**The decision tree:**

```
Is the work I/O-bound (network, disk, subprocess)?
  → YES → threads (cheap, GIL doesn't matter)
  → NO  → is it CPU-bound (math, parsing, ML)?
    → YES → multiprocessing (bypass GIL)
    → NO  → probably doesn't need parallelism
```

For `git pull`, it's 100% network wait. Threads are perfect. Multiprocessing would work too, just wastes memory for zero benefit.
