---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to read XNU and FreeBSD kqueue source
translated: false
type: note
---

**Question:** How do I get the macOS (XNU) and BSD kernel source code to read the actual `kqueue`/`kevent` implementation?

**Answer:**

macOS's kernel (XNU) is open source. Apple publishes it on GitHub under `apple-oss-distributions`, and kqueue originated in FreeBSD, so grab both:

```bash
# XNU — the macOS kernel (Mach + BSD layer + IOKit)
git clone https://github.com/apple-oss-distributions/xnu.git
cd xnu

# kqueue lives in the BSD layer:
ls bsd/kern/kern_event.c        # kqueue/kevent core (~10k lines)
ls bsd/sys/event.h              # struct kevent, EVFILT_* definitions
ls bsd/kern/sys_generic.c       # select/poll for comparison
```

```bash
# FreeBSD — where kqueue was invented (Jonathan Lemon, 2000)
git clone --depth 1 https://github.com/freebsd/freebsd-src.git
ls freebsd-src/sys/kern/kern_event.c   # the original implementation
```

Key entry points to read in XNU's `bsd/kern/kern_event.c`:

```bash
grep -n "^kevent\|^static.*kqueue_scan\|^kqueue_begin_processing" bsd/kern/kern_event.c
```

- `kevent_internal()` — syscall entry, the analog of `do_epoll_wait`
- `kqueue_scan()` — the wait loop; the analog of `ep_poll` you were looking at. The sleep happens via `waitq_assert_wait64_leeway()` + `thread_block()` instead of Linux's `__set_current_state` + `schedule_hrtimeout_range()`. XNU uses Mach waitqs/continuations, not Linux waitqueues — that's the structural difference behind the same "sleep until event or timeout" pattern.
- `knote()` / `knote_post()` — the wake source: subsystems (sockets, pipes, vnodes) post events to attached knotes, analogous to `ep_poll_callback`.

Tags matter — to read the source matching *your* running macOS:

```bash
git tag | grep xnu | tail -5      # e.g. xnu-11215.x for macOS 15.x
uname -v                          # shows your kernel's xnu version string
git checkout xnu-11215.81.4       # match it
```

A few practical notes: XNU also builds — Apple ships a `KDK` (Kernel Debug Kit) at developer.apple.com/download if you want symbols/debugging, and the repo's README documents building with the macOS SDK. For browsing without cloning, `opensource.apple.com/source/xnu/` has older releases and GitHub's code search works well on the repo.

The mapping for your epoll comparison: Linux `eventpoll.c` epitem ↔ XNU `knote`; `ep_poll_callback` ↔ `knote_post`; red-black tree of fds ↔ per-fd `klist` hung off the fileproc. FreeBSD's `kern_event.c` is shorter and cleaner than XNU's (XNU added workloops, QoS, and Mach port filters for libdispatch), so read FreeBSD first if you want the algorithm, XNU second if you want what actually runs on your Mac.

**References:**

- [apple-oss-distributions/xnu](https://github.com/apple-oss-distributions/xnu)
- [freebsd/freebsd-src](https://github.com/freebsd/freebsd-src)
- [Apple Open Source](https://opensource.apple.com)
