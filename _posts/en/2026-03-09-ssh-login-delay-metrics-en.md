---
audio: false
generated: true
image: false
lang: en
layout: post
title: Measuring SSH Login Delays Precisely
translated: false
type: note
---

**Question:** How can you measure SSH login latency — what command-line options or tools can you use to detect a delay like the 500ms anomaly Andres Freund noticed?

---

**Answer:**

## Methods to Measure & Detect SSH Login Delay

There are several approaches, from the simplest one-liner to detailed diagnostic deep-dives.

---

### Method 1 — `time` command (The Simplest Way)

This is most likely the method Andres Freund used first. Wrap your `ssh` command with `time`:

```bash
time ssh user@hostname hostname
```

**Example normal output:**
```
linux01.localdomain

real    0m0.120s     ← this is your total login round-trip time
user    0m0.021s
sys     0m0.008s
```

**Anomalous output (XZ backdoor scenario):**
```
real    0m0.620s     ← 500ms unexplained extra delay!
```

You can also run it multiple times for consistency:
```bash
for i in {1..5}; do time ssh user@host hostname; done
```

---

### Method 2 — `-v` / `-vv` / `-vvv` Verbose Mode (Pinpoint Where the Delay Occurs)

Connect to your server using `ssh -v user@server_ip`. The verbose output provides detailed information about the connection process, including authentication steps, cipher negotiations, and potential timeouts, which can reveal specific points of delay. Using `-vv` or `-vvv` increases the verbosity further.

```bash
ssh -v user@hostname hostname       # basic verbose
ssh -vv user@hostname hostname      # more detail
ssh -vvv user@hostname hostname     # maximum detail
```

Using `-vvv` shows each handshake stage with timing, so you can identify exactly which phase — TCP connect, key exchange, authentication, or shell startup — is slow.

**Sample output showing where time is spent:**
```
debug1: Connecting to hostname [1.2.3.4] port 22.
debug1: Connection established.
debug1: identity file /home/user/.ssh/id_rsa
debug2: kex: server->client ...
debug3: Waited 520ms here   ← you'd see a gap in timestamps
debug1: Authentication succeeded (publickey).
```

---

### Method 3 — `ssh -E logfile` + Timestamps (Log with timing)

Write verbose output to a file with timestamps for analysis:

```bash
ssh -vvv -E /tmp/ssh_debug.log user@hostname hostname
# Then inspect the log:
cat /tmp/ssh_debug.log
```

Or pipe through `ts` (timestamp tool from `moreutils`):

```bash
ssh -vvv user@hostname hostname 2>&1 | ts '%.s'
```

This prepends a Unix timestamp to each debug line, making it easy to spot where the 500ms was lost.

---

### Method 4 — `sshping` Tool (Dedicated SSH Latency Benchmark)

`sshping` is an SSH-based ping utility that measures interactive character echo latency and file transfer throughput.

```bash
# Install
sudo apt-get install libssh-dev
# then build from https://github.com/spook/sshping

# Run
sshping -H user@hostname
```

It reports: `ssh-Login-Time` (time to establish TCP, authenticate, and form the SSH session), `Minimum-Latency`, `Median-Latency`, `Average-Latency`, `Maximum-Latency`, and transfer rates — all in human-readable format.

**Example output:**
```
ssh-Login-Time:   1.84 s
Minimum-Latency:  633 us
Median-Latency:   751 us
Average-Latency:  764 us
Maximum-Latency:  1.15 ms
Upload-Rate:      9.33 MB/s
```

---

### Method 5 — `strace` on sshd (Server-Side, Deep Diagnosis)

You can run `strace` on the server-side `sshd` process to trace system calls and find exactly what the daemon is waiting on — file reads, network lookups, library calls, etc. It is not 100% safe for use on critical production processes, but is powerful for debugging.

```bash
# On the server, find the sshd child PID during a login attempt:
ps -ef | grep sshd

# Attach strace to trace system calls with timestamps:
strace -tt -p <PID>
```

This is essentially what Andres Freund did when he ran **Valgrind** — a similar deep introspection tool — against the process and noticed anomalous behavior from `liblzma`.

---

### Method 6 — Valgrind (What Andres Actually Used)

Andres ran benchmarks using Valgrind for memory profiling:

```bash
valgrind --tool=callgrind ssh user@host hostname
```

The Valgrind errors pointed at `liblzma`, which pulled on the thread that unraveled the whole XZ backdoor.

---

### Quick Reference Table

| Method | Command | What it detects |
|---|---|---|
| Basic timing | `time ssh user@host hostname` | Total login roundtrip |
| Verbose | `ssh -vvv user@host hostname` | Which phase is slow |
| Timestamped log | `ssh -vvv ... 2>&1 \| ts '%.s'` | Millisecond-level phase gaps |
| sshping | `sshping -H user@host` | Structured latency report |
| strace (server) | `strace -tt -p <sshd_pid>` | System calls causing delay |
| Valgrind | `valgrind ssh user@host hostname` | Memory/library anomalies |

---

### Key Takeaway

For detecting the XZ-style anomaly specifically, the most practical everyday command is:

```bash
time ssh user@host hostname
```

If the `real` time is consistently 400–600ms higher than expected (and your network ping is normal), that's your red flag — exactly what Andres noticed, which led him to investigate further with Valgrind and eventually uncover the backdoor.

---

**References:**

- [Tanel Poder Blog — Troubleshooting Linux SSH Login Delay](https://tanelpoder.com/posts/troubleshooting-linux-ssh-logon-delay-always-takes-10-seconds/)
- [PingTesti.com — SSH Latency Explained](https://www.pingtesti.com/en/blog/ssh-latency-explained/)
- [GitHub — spook/sshping](https://github.com/spook/sshping)
- [sshping man page — openSUSE](https://manpages.opensuse.org/Tumbleweed/sshping/sshping.8.en.html)
