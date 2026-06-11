---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kqueue Traced Through XNU Source
translated: false
type: note
---

Here's what kqueue is, traced through the XNU source:

## What kqueue is

kqueue is macOS/BSD's **event notification mechanism** — a kernel subsystem that lets a process say "wake me up when something happens on this file descriptor / process / timer / Mach port" without polling.

### The core data structures

**1. kqueue itself** (`bsd/sys/eventvar.h:156`):
```c
struct kqueue {
    lck_spin_t      kq_lock;      // protects all fields
    kq_state_t      kq_state;     // KQ_WORKQ | KQ_WORKLOOP | flags
    uint16_t        kq_level;     // nesting level
    uint32_t        kq_count;     // number of triggered (queued) events
    struct proc    *kq_p;         // owning process
};
```

The `kq_count` field is the key — it tracks only **triggered** events, not all registered events. This is what makes kqueue O(triggered) not O(registered).

**2. kqfile** — the file-descriptor form (`eventvar.h:172`):
```c
struct kqfile {
    struct kqueue   kqf_kqueue;     // core kqueue
    struct kqtailq  kqf_queue;      // queue of TRIGGERED knotes
    struct kqtailq  kqf_suppressed; // suppression queue
    struct selinfo  kqf_sel;        // for select() compat
};
```

**3. knote** — the event registration (`event_private.h:428`):
```c
struct knote {
    TAILQ_ENTRY(knote)  kn_tqe;        // linkage in kqueue's triggered queue
    SLIST_ENTRY(knote)  kn_link;        // linkage for fd search list
    SLIST_ENTRY(knote)  kn_selnext;     // klist element chain (on the watched object)
    kn_status_t         kn_status : 12; // KN_ACTIVE, KN_QUEUED, KN_DISABLED, etc.
    // ...
    struct kevent_internal_s kn_kevent;  // filter, ident, flags, data, udata
};
```

A knote is the **bridge** between a kqueue and a watched object. It lives on two lists simultaneously:
- `kn_selnext` — linked onto the watched object's `klist` (e.g., a socket's `sb_sel.si_note`)
- `kn_tqe` — linked onto the kqueue's `kqf_queue` when triggered

**4. filterops** — the event source abstraction (`event_private.h:727`):
```c
struct filterops {
    bool f_isfd;                          // true if ident == filedescriptor
    int  (*f_attach)(struct knote *kn, ...);   // register interest
    void (*f_detach)(struct knote *kn);        // unregister
    int  (*f_event)(struct knote *kn, long hint);  // is the event active?
    int  (*f_process)(struct knote *kn, ...);  // snapshot event data
};
```

Each event source (socket, vnode, process, timer, Mach port) provides its own filterops. For sockets, it's `filt_sockattach`, `filt_sockev`, `filt_sockprocess` in `uipc_socket.c`.

### The lifecycle

**Step 1: Create a kqueue** — `kqueue()` syscall (`kern_event.c:3092`):
```c
kqueue(struct proc *p, ...) {
    return kqueue_internal(p, NULL, NULL, retval);
}
```
→ `kqueue_internal()` → `kqueue_alloc()` → returns a file descriptor.

**Step 2: Register interest** — `kevent()` with `EV_ADD` flag (`kern_event.c:4006`):
```c
kevent_register(struct kqueue *kq, struct kevent_qos_s *kev, ...) {
    // find or create a knote for this filter+ident
    kn = kq_find_knote_and_kq_lock(kq, kev, ...);
    if (kn == NULL && (kev->flags & EV_ADD)) {
        // allocate new knote, call filter's f_attach()
        kn = knote_alloc(kq);
        result = filter_call(fops, f_attach(kn, kev));
        // link knote onto the watched object's klist
        knote_attach(&fdp->fd_knlist[fd], kn);
    }
}
```

This creates a knote and links it to both the kqueue and the file descriptor's knote list.

**Step 3: Wait for events** — `kevent()` without changes (`kern_event.c:8017`):
```c
kqueue_scan(kqueue_t kqu, int flags, ...) {
    for (;;) {
        kqlock(kqu);
        error = kqueue_process(kqu, flags, kectx, callback);  // process triggered events
        if (error || (flags & KEVENT_FLAG_IMMEDIATE)) {
            return error;
        }
        // no events yet — block the thread
        kqu.kqf->kqf_state |= KQ_SLEEP;
        assert_wait_deadline(&kqu.kqf->kqf_count, THREAD_ABORTSAFE, deadline);
        kqunlock(kqu);
        thread_block_parameter(kqueue_scan_continue, kqu.kqf);  // context switch away
    }
}
```

The thread is removed from the CPU run queue. Zero CPU usage.

**Step 4: Event fires** — e.g., TCP data arrives on a socket:

The network stack calls `sorwakeup()` → `sowakeup()` (`uipc_socket2.c:625`):
```c
sowakeup(struct socket *so, struct sockbuf *sb, ...) {
    selwakeup(&sb->sb_sel);           // wake select() waiters
    sbwakeup(sb);                     // wake msleep() waiters
    if (sb->sb_flags & SB_KNOTE) {
        KNOTE(&sb->sb_sel.si_note, SO_FILT_HINT_LOCKED);  // trigger kqueue knotes
    }
}
```

`KNOTE()` expands to `knote()` (`kern_event.c:6590`):
```c
knote(struct klist *list, long hint, ...) {
    SLIST_FOREACH_SAFE(kn, list, kn_selnext, tmp_kn) {
        knote_post(kn, hint);  // check filter, activate if ready
    }
}
```

`knote_post()` → calls the filter's `f_event()` → if `FILTER_ACTIVE` → `knote_activate()` → `knote_enqueue()`:
```c
knote_enqueue(kqueue_t kqu, struct knote *kn) {
    struct kqtailq *queue = knote_get_tailq(kqu, kn);
    TAILQ_INSERT_TAIL(queue, kn, kn_tqe);  // add to triggered queue
    kn->kn_status |= KN_QUEUED;
    kqu.kq->kq_count++;                    // increment triggered count
    // wake up thread blocked in kqueue_scan()
    kqfile_wakeup(kqu.kqf, 0, THREAD_AWAKENED);
}
```

**Step 5: Thread wakes up** — `kqueue_scan` continues, `kqueue_process()` iterates only the triggered queue:
```c
do {
    while ((kn = TAILQ_FIRST(queue)) != NULL) {
        knote_process(kn, kectx, callback);  // call filter's f_process(), copyout to user
    }
} while (queue-- > base_queue);
```

### What event sources exist

From `bsd/sys/event.h:70-84`:
```c
#define EVFILT_READ      (-1)   // fd is readable (socket has data, file has bytes)
#define EVFILT_WRITE     (-2)   // fd is writable (socket buffer has space)
#define EVFILT_AIO       (-3)   // async I/O complete
#define EVFILT_VNODE     (-4)   // file changed (write, delete, rename, attrib)
#define EVFILT_PROC      (-5)   // process state change (fork, exec, exit, signal)
#define EVFILT_SIGNAL    (-6)   // signal delivered
#define EVFILT_TIMER     (-7)   // periodic/one-shot timer
#define EVFILT_MACHPORT  (-8)   // Mach port message arrived
#define EVFILT_FS        (-9)   // filesystem event
#define EVFILT_USER      (-10)  // user-triggered event (manual wakeup)
#define EVFILT_VM        (-12)  // virtual memory event
#define EVFILT_EXCEPT    (-15)  // exception events
```

### The three kqueue flavors

XNU has three kqueue types:

1. **kqfile** — the classic `kqueue()` syscall result. One queue, used with `kevent()`/`select()`. (`eventvar.h:172`)

2. **kqworkq** — private per-process kqueue for GCD/libdispatch. Has per-QoS buckets (`KQWQ_NBUCKETS` = 6). Events are segregated by priority so high-QoS events get serviced first. (`eventvar.h:211`)

3. **kqworkloop** — the modern evolution. Supports bound threads (a thread permanently parked on the workloop), thread handoff, and QoS-aware processing. Used by Swift concurrency and modern GCD. Has `KQWL_NBUCKETS` = 5 priority levels. (`eventvar.h:234+`)

### kqueue vs select/poll

The critical difference: `select()` scans **all** registered FDs every time to check readiness. kqueue only processes knotes that have been **explicitly triggered** by the event source. The watched object (socket, vnode, etc.) calls `KNOTE()` when something happens — kqueue never polls.

This is why kqueue scales to thousands of FDs efficiently: the cost is proportional to the number of events that actually fire, not the number of things being watched.
