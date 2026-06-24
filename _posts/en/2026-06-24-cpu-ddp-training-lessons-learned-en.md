---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU DDP Training Lessons Learned
translated: false
type: note
---

Training stopped. Both processes dead on both machines.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  KEY LESSONS — 2-NODE CPU DDP TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT WE RAN
  Model: nanochat d8 (126M params)
  Nodes: 2 (master 192.168.1.36 + worker 192.168.1.28)
  Backend: Gloo (CPU-only DDP)
  Duration: 26.4 hours, 1329/5000 steps
  Loss: 10.40 → 5.02

LESSON 1: GLOO NEEDS BIDIRECTIONAL CONNECTIVITY
  The TCPStore rendezvous (port 29500) only requires worker→master.
  But Gloo's data transport needs master→worker on ephemeral ports too.
  The worker's firewall blocked these. Without opening it, training hangs
  silently at the rendezvous phase — no error, just stuck.
  Fix: Open firewall on worker for the master's IP, or use
  GLOO_PORT_RANGE and open that specific range.

LESSON 2: KILL STALE PROCESSES BEFORE RELAUNCHING
  Orphaned torchrun/base_train processes (PPID=1) hold port 29500 and
  interfere with new launches. Always check before starting:
    ps aux | grep -E 'torchrun|base_train' | grep -v grep
    ss -tlnp | grep 29500
  Kill with: pkill -9 -f torchrun; fuser -k 29500/tcp

LESSON 3: TMUX FOR EVERYTHING, NEVER BACKGROUND SSH
  Background SSH (&) dies silently when the session drops. tmux survives
  disconnections. Use tmux for all long-running remote processes.
  Pattern: tmux new-session -d -s name 'command; sleep 999999'
  The sleep keeps the tmux session alive after the command exits.

LESSON 4: CPU DDP PARALLELISM GAIN IS MINIMAL
  2 nodes, each with ~24 CPU cores, gave 57 tok/s total.
  Single-node CPU was ~60 tok/s. The Gloo all-reduce over Ethernet
  (~1 Gbps) is so slow it nearly negates the parallelism benefit.
  CPU DDP is only worth it if you need the combined RAM, not for speed.

LESSON 5: NESTED SSH + TMUX = QUOTING HELL
  Running tmux on the worker through SSH-through-SSH breaks quoting.
  Solution: write a script file to the worker first, then tmux it:
    ssh master "ssh worker 'cat > /tmp/run.sh << EOF ... EOF'"
    ssh master "ssh worker 'tmux new -d -s x \"bash /tmp/run.sh\"'"

LESSON 6: LOG CAPTURE IS TRICKIER THAN YOU'D EXPECT
  tee captures stdout but torchrun writes progress to stderr.
  script -q -c "cmd" log.txt captures both but buffers heavily.
  tmux capture-pane -p is the most reliable way to read remote output.
  PYTHONUNBUFFERED=1 helps but doesn't fix everything.

LESSON 7: SSH EXIT CODE 255 IS NORMAL FOR NESTED SSH
  When doing ssh host1 "ssh host2 cmd", exit code 255 from the outer
  SSH doesn't mean the inner command failed. Check the inner command's
  actual output separately.

LESSON 8: MODEL SIZE LABELED "80M" WAS ACTUALLY 126M
  The script said "~80M params" but value_embeds alone is 67M.
  Always check the actual parameter count printed at startup.
  The 126M model in float32 = ~500MB per rank. Easily fits in RAM
  on both machines.

LESSON 9: NETWORK DEBUGGING CHECKLIST

  1. Can worker reach master's TCPStore port? (bash /dev/tcp test)
  2. Can master reach worker on ephemeral ports? (same test)
  3. Is Tailscale interfering? (check tailscale status)
  4. Is nsswitch.conf resolving hostname to loopback? (grep myhostname)
  5. Is GLOO_SOCKET_IFNAME set to the right interface?

LESSON 10: CPU TRAINING IS MEMORY-BOUND, NOT COMPUTE-BOUND
  The 57 tok/s bottleneck is DDR bandwidth (~50-80 GB/s), not CPU
  compute. Adding more CPU cores or nodes doesn't help much because
  the data bus is saturated. Only a GPU (504 GB/s GDDR6X) or HBM
  (1-3 TB/s) can break this wall.
