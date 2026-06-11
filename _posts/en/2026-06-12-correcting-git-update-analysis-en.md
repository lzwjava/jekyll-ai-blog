---
audio: false
generated: true
image: false
lang: en
layout: post
title: Correcting Git Update Analysis
translated: false
type: note
---

Here's the verification against the actual source code at `ww/git/git_update.py`:

**What the code actually does:**

```
Line 207:  default=32  ← confirmed, 32 is the default --jobs
Line 278:  max_workers = min(args.jobs, len(valid_paths))  ← capped at repo count
Line 281:  ThreadPoolExecutor(max_workers=max_workers)  ← confirmed, threads not processes
```

Two-phase design (confirmed):

- Phase 1 (line 274-293): fetch all repos in parallel → check which need pulling
- Phase 2 (line 296-311): pull only repos that actually changed

Repos.json has 161 repos (not 160, close enough).

**Where the analysis is WRONG or misleading:**

1. **"Thread spends 99% of time waiting on network RTT"** — wrong granularity. Each `fetch_repo` call (line 71-98) spawns MULTIPLE subprocess calls:
   - `_get_current_branch()` → `git rev-parse --abbrev-ref HEAD` (subprocess #1)
   - `_has_upstream()` → `git rev-parse --abbrev-ref branch@{u}` (subprocess #2)
   - `git fetch` (subprocess #3, the actual network I/O)
   - `git rev-list --count HEAD..@{u}` (subprocess #4)

   That's 4 subprocess spawns per repo, not one network round-trip. Each subprocess has fork+exec overhead (~1-5ms each on macOS). At 161 repos × 4 calls = 644 subprocess spawns.

2. **"The thread is parked in the kernel's epoll/kqueue"** — fundamentally wrong threading model. Python's `subprocess.run()` is blocking I/O. The thread blocks in `waitpid()` syscall waiting for the child process. It's NOT using epoll/kqueue async I/O. It's a kernel-level thread blocking, not an event loop. The distinction matters: 32 threads = 32 OS threads consuming kernel stack memory (~8KB each), not 32 async handles on a single thread.

3. **"Uses 0% CPU while waiting"** — misleading. The Python thread is indeed sleeping, but each `git` child process uses CPU for:
   - SSH key exchange / TLS negotiation (CPU-intensive crypto)
   - Git protocol negotiation (pack-protocol parsing)
   - SHA-1 hash verification of received objects
   - Packfile decompression and indexing

   At 32 concurrent git processes, you WILL see non-trivial CPU usage. The claim confuses "Python thread is sleeping" with "system is idle."

4. **"Each git process opens ~5-10 FDs"** — underestimated. Each `fetch_repo` spawns 4 sequential child processes. At peak, 32 concurrent threads × 1 active child × ~5 FDs = ~160 FDs. But the parent Python process also has FDs for thread stacks, pipe buffers, etc. Actual peak is more like 200-400 FDs. Still well within `ulimit -n 2560`, but the number is wrong.

5. **"DMIT proxy bottleneck"** — unverifiable from code. The code just calls `git fetch` with no proxy configuration visible here. Whether hysteria2 is configured at the OS/proxy level or in `~/.ssh/config` is external to this code.

**Where the analysis is CORRECT:**

- 32 as default is confirmed in code (line 207)
- `ThreadPoolExecutor` is correct for I/O-bound work
- GitHub does rate-limit concurrent SSH connections (documented behavior)
- Diminishing returns beyond ~32 is plausible given the 4-subprocess-per-repo overhead means each "fetch" takes longer than just one RTT
- The `min(args.jobs, len(valid_paths))` cap means 32 is also roughly the point where you're processing ~5 repos per batch (161/32 ≈ 5), which keeps the thread pool saturated without excessive queuing

**The real reason 32 works well:**

It's not about network RTT or epoll. It's that each `fetch_repo` does 4 sequential subprocess calls, each with fork+exec+waitpid overhead. With 32 threads, you overlap the network waits of ~32 concurrent `git fetch` calls while the subprocess spawn overhead of the other calls is negligible. Beyond 32, you're spawning more git processes than GitHub wants to serve concurrently, so they queue server-side. The bottleneck is GitHub's SSH connection acceptance rate, not your local threading.
