---
audio: false
generated: true
image: false
lang: en
layout: post
title: XNU Source Code Verdict
translated: false
type: note
---

Now I have enough XNU source evidence. Here's the verdict:

---

## XNU Source Code Verdict on "Why 32 is the sweet spot"

### Claim 1: "It's parked in the kernel's epoll/kqueue"

**Partially wrong terminology, correct mechanism.**

macOS uses kqueue, not epoll (that's Linux). But the blocking mechanism is real. From `kern_event.c:8038-8044`:

```c
kqu.kqf->kqf_state |= KQ_SLEEP;
assert_wait_deadline(&kqu.kqf->kqf_count, THREAD_ABORTSAFE,
    kectx->kec_deadline);
kqunlock(kqu);

if (__probable((flags & (KEVENT_FLAG_POLL | KEVENT_FLAG_KERNEL)) == 0)) {
    thread_block_parameter(kqueue_scan_continue, qu.kqf);
    __builtin_unreachable();
}
```

The thread calls `assert_wait_deadline()` (registers itself on a wait queue) then `thread_block_parameter()` which calls `thread_block_reason()` at `sched_prim.c:3752`. This does a full context switch — the thread is removed from the CPU run queue entirely. **Verdict: CORRECT that the thread uses 0% CPU while waiting.**

### Claim 2: "no scheduling, no burning cycles"

**Correct.** From `sched_prim.c:3788-3801`:

```c
self->continuation = continuation;
self->parameter = parameter;
// ...
new_thread = thread_select(self, processor, &reason);
thread_invoke(self, new_thread, reason);
```

The thread hands off its CPU core to another thread. It's not polling, not spinning. The thread state transitions to `TH_WAIT` (0x01 per `thread.h:512`), removed from `TH_RUN` (0x04). **Verdict: CORRECT.**

### Claim 3: "the kernel's kqueue starts doing more work polling them" at 64+ FDs

**WRONG. This is the biggest error in the article.**

kqueue does NOT poll registered FDs. It's purely event-driven. From `kern_event.c:7859-7868`:

```c
do {
    while ((kn = TAILQ_FIRST(queue)) != NULL) {
        error = knote_process(kn, kectx, callback);
        // ...
    }
} while (queue-- > base_queue);
```

`kqueue_process()` iterates only over **triggered knotes** in the tail queue (`kqf_queue`), not all registered knotes. When TCP data arrives on a socket, the network stack calls `sorwakeup()` → `sowakeup()` → `KNOTE()` → `knote_enqueue()` which adds only that specific knote to the queue. The scan is O(triggered), not O(registered).

This is fundamentally different from `select()` which scans all FDs every time. kqueue with 200 registered FDs where only 3 have events does the same work as kqueue with 2000 registered FDs where 3 have events. **Verdict: The "more work polling" claim is FALSE.**

### Claim 4: "each git process opens ~5-10 FDs" and "200-300 FDs at 32 workers"

**Roughly correct.** From `syslimits.h:108` and `param.h:101`:

```c
#define OPEN_MAX    10240   /* max open files per process */
#define NOFILE      256     /* default max open files per process */
```

macOS allows up to 10,240 FDs per process. Each git process opens socket + packfile + index + loose objects, so ~5-10 FDs is reasonable. At 32 workers, ~200-300 FDs is plausible and well within limits. **Verdict: CORRECT.**

### Claim 5: "GitHub connection throttling at ~30-40 concurrent SSH"

**Cannot verify from XNU source** — this is a server-side GitHub policy, not a kernel behavior. But it's plausible. SSH connections have significant setup overhead (key exchange, channel multiplexing).

### Claim 6: The math and batch calculations

**Correct in principle, wrong in precision.** The theoretical minimum calculations are sound (160 repos / N workers × RTT). But the actual numbers (24.1s, 9.9s, 9.6s) are presented as precise measurements — if those are from actual benchmarks, they're fine. If estimated, the precision is misleading.

---

## Summary

| Claim | Verdict |
|-------|---------|
| Threads parked in kqueue use 0% CPU | CORRECT |
| No scheduling/cycles while waiting | CORRECT |
| kqueue does more work polling at higher FD counts | **WRONG** — kqueue is event-driven, O(triggered) not O(FDs) |
| ~5-10 FDs per git process | CORRECT |
| 32 is the sweet spot | Plausible but the kqueue reasoning is wrong |

**The real reason 32 is the sweet spot has nothing to do with kqueue overhead.** It's purely about:
1. GitHub's server-side connection acceptance rate
2. Your proxy (DMIT/hysteria2) bandwidth/connection pool limits
3. Diminishing returns when network RTT dominates — adding workers beyond the bottleneck's capacity just creates more connections in the TCP backlog, not more throughput

The article's kqueue analysis is the weakest part. kqueue scales gracefully to thousands of FDs — that's literally what it was designed for (unlike `select()`). The bottleneck is the network path, not the kernel.
