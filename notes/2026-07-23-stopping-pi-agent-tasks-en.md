---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stopping pi agent tasks
translated: false
type: note
---

Question: When using pi agent for a long-running task, how do you stop it?

Answer:

For a CLI agent like **pi agent**, stopping a long-running task is usually the same as stopping a foreground terminal process:

```bash
Ctrl + C
```

This sends `SIGINT` to the running agent. Most well-behaved agents catch it and stop gracefully.

If it ignores `Ctrl+C`:

### 1. Find the process

```bash
ps aux | grep pi
```

or:

```bash
pgrep -af pi
```

Example:

```
lzw   12345  ... pi-agent ...
```

### 2. Send termination signal

```bash
kill 12345
```

If still stuck:

```bash
kill -9 12345
```

`kill -9` is the hard stop (`SIGKILL`), no cleanup.

---

### If pi agent spawned child processes

Sometimes the agent launches:

* `npm install`
* `python`
* `docker`
* build jobs
* test runners

You may need to kill the process tree:

```bash
pstree -p $(pgrep -f pi)
```

or:

```bash
pkill -P <parent_pid>
```

---

### For tmux / remote sessions

If you run agents inside tmux:

```bash
tmux attach
```

then:

```
Ctrl+C
```

or kill the whole session:

```bash
tmux kill-session -t <session_name>
```

---

### Agent-native workflow tip

For long autonomous runs, I usually run agents in a separate session:

```bash
tmux new -s agent
pi
```

Then you can detach:

```
Ctrl+B D
```

and later:

```bash
tmux attach -t agent
```

This avoids accidentally killing the agent by closing the terminal.

For "yolo mode" agents (skip confirmations), tmux + `Ctrl+C` is basically the standard control loop: let it run, inspect occasionally, interrupt when the trajectory is wrong.