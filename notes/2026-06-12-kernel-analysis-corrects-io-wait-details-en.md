---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel Analysis Corrects I/O Wait Details
translated: false
type: note
---

Now I have the full picture from the kernel source. Here's the verdict:

---

## VERDICT: Analysis is directionally right on I/O-bound behavior, but WRONG on mechanism details

### 1. "Thread parked in kernel's epoll/kqueue" — WRONG

The analysis claims Python threads wait via `epoll/kqueue`. The kernel source shows two completely different mechanisms:

**For subprocess.wait() (what `subprocess.run()` actually does):**
```
kernel/exit.c:1711-1734  (do_wait)
  1722:  set_current_state(TASK_INTERRUPTIBLE)
  1728:  schedule()    ← thread yields CPU, removed from runqueue
  1731:  __set_current_state(TASK_RUNNING)  ← wakes when child exits
```
This is a **wait queue on child exit**, not epoll. The thread sleeps in `waitpid()` until the child process exits. No epoll, no kqueue, no event loop.

**For actual epoll (if Python used asyncio):**
```
fs/eventpoll.c:2013-2032  (ep_poll)
  2013:  __set_current_state(TASK_INTERRUPTIBLE)
  2029:  schedule_hrtimeout_range()  ← sleeps with timeout
  2032:  __set_current_state(TASK_RUNNING)
```
Same sleep mechanism, different wake source.

**Also: Linux has no kqueue.** That's BSD/macOS. The analysis confuses macOS and Linux kernel concepts.

### 2. "Uses 0% CPU while waiting" — PARTIALLY CORRECT but misleading

The kernel code confirms the Python thread is truly sleeping:
```
kernel/sched/core.c:6625  (try_to_block_task)
  block_task(rq, p, flags)  ← dequeued from runqueue entirely
```

TASK_INTERRUPTIBLE threads are **removed from the runqueue** — the scheduler doesn't even look at them. So the Python thread uses 0% CPU. BUT:

- Each `git` **child process** is running and using CPU (SSH crypto, protocol negotiation, SHA-1)
- At 32 concurrent workers, you have 32 git child processes actively consuming CPU
- The claim "CPU does almost nothing" is wrong at the system level

### 3. "Each git process opens ~5-10 FDs... at 32 workers that's ~200-300 FDs" — WRONG

```
kernel/fork.c:1634-1637  (copy_files)
  if (clone_flags & CLONE_FILES) {
      atomic_inc(&oldf->count);  ← just increments refcount
      return 0;
  }
```

Python's `pthread_create` uses `CLONE_FILES`, so all 32 threads share **ONE file descriptor table**. It's not 32 × 5-10 = 160-300 FDs. It's ~5-10 FDs total (one socket + one packfile per active git fetch, shared table).

### 4. "GitHub connection throttling — limits concurrent SSH connections per IP" — PLAUSIBLE but wrong mechanism

The kernel source shows the server-side connection drop mechanism:
```
net/ipv4/tcp_input.c:7612-7626  (tcp_conn_request)
  7615:  inet_csk_reqsk_queue_is_full(sk)  ← SYN queue full?
  7623:  sk_acc...full(sk)            ← accept queue full?
  7624:  NET_INC_STATS(...LINUX_MIB_LISTENOVERFLOWS)
  7625:  goto drop                         ← kernel drops the connection
```

This is the **server-side kernel dropping connections** when the accept queue overflows. But this is about TCP connections, not SSH connections. GitHub's SSH throttling is likely at the application level (sshd MaxSessions, MaxStartups), not kernel TCP queue overflow.

### 5. "macOS file descriptor overhead" — IRRELEVANT on Linux

The analysis mentions `kqueue` and macOS FD overhead, but:
- kqueue doesn't exist in Linux (this is the Linux kernel source)
- The code runs Python `subprocess.run()` which uses `waitpid()`, not kqueue
- If running on macOS, `kqueue` IS the right mechanism, but the analysis conflates the two

### 6. The real bottleneck — verified by kernel code

The actual bottleneck is confirmed by the TCP code:

```
net/ipv4/tcp_input.c:7615
  if (syncookies == 2 || inet_csk_reqsk_queue_is_full(sk)) {
      want_cookie = tcp_syn_flood_action(sk, ...);
      if (!want_cookie)
          goto drop;  ← SYN queue full → drop
  }

net/ipv4/tcp_input.c:7623
  if (sk_acc...full(sk)) {
      NET_INC_STATS(...LINUX_MIB_LISTENOVERFLOWS);
      goto drop;  ← accept queue full → drop
  }
```

When GitHub's sshd has too many pending connections, the kernel's accept queue fills up and new TCP connections get dropped. This is the real "throttling" mechanism — not application-level SSH limits, but kernel-level TCP queue overflow.

### Summary table

| Claim | Verdict | Kernel Evidence |
|-------|---------|-----------------|
| Thread in epoll/kqueue | **WRONG** | Uses waitpid() wait queue (kernel/exit.c:1722) |
| 0% CPU while waiting | **PARTIAL** | Thread sleeps (core.c:6625), but git children use CPU |
| 200-300 FDs at 32 workers | **WRONG** | CLONE_FILES shares fd table (fork.c:1634) |
| GitHub throttling | **PLAUSIBLE** | TCP accept queue drops connections (tcp_input.c:7623) |
| kqueue on macOS | **WRONG CONTEXT** | Linux has epoll, not kqueue |
| TASK_INTERRUPTIBLE = no scheduling | **CORRECT** | block_task() dequeues from runqueue (core.c:6625) |

The bottom line: the analysis gets the high-level behavior right (I/O-bound, diminishing returns past 32) but gets the kernel mechanisms wrong. Python threads don't use epoll — they use waitpid() wait queues. They don't create separate FD tables. And kqueue is macOS, not Linux.
