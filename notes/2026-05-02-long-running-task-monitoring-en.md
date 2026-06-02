---
audio: false
generated: true
image: false
lang: en
layout: post
title: Long-Running Task Monitoring Explained
translated: false
type: note
---

Question: How does Claude Code implement “Monitor(tail download output for completion signal)” and similar long-running monitoring steps?

Answer:

What you’re seeing in that transcript is a pattern from an **agentic tool-execution loop**, not a single “magic command”. Systems like Claude Code typically implement this using a combination of:

---

## 1. Long-running tool calls are **async jobs**

When the model issues something like:

> Monitor(tail download output for completion signal)

it is usually translated into something like:

* Start a background task (e.g., shell command, remote SSH job, download, build, etc.)
* Return immediately with a **task ID**
* Keep the job running outside the LLM process

So internally it becomes:

```
task_id = start_command("tail download.log")
```

---

## 2. A **polling / event subscription loop**

The “Monitor” abstraction is just a wrapper over one of these two patterns:

### A) Polling

The system repeatedly checks status:

```text
GET /task_status?task_id=b7oxfxl1j
```

and returns:

* progress (e.g. 61%, 70%)
* logs (new tail output)
* completion state

This is why you see:

> “61% done… 70% done…”

---

### B) Event streaming (better design)

Instead of polling, the system subscribes to updates:

* stdout streaming (like `tail -f`)
* filesystem watcher events
* websocket from remote executor

Example:

```
subscribe(task_id=b7oxfxl1j)
→ emits:
  - log update
  - progress update
  - completion event
```

---

## 3. “tail download output” is usually log streaming

That specific phrase strongly suggests:

* a file download is happening
* progress is written to stdout or a log file
* the monitor is attached via:

### Linux-style implementation

```bash
tail -f download.log
```

or:

```bash
rsync --progress
curl -O --progress-bar
```

Then the system parses:

* percentage
* bytes downloaded
* ETA

and converts it into structured progress.

---

## 4. “completion signal” is just a sentinel condition

The monitor stops when it detects:

* process exit code = 0
* file exists (`mihomo binary exists`)
* specific log line appears:

  ```
  INSTALL COMPLETE
  ```

* or checksum verification passes

So internally:

```python
while True:
    status = check_task()
    if status.done:
        break
```

---

## 5. Why Claude Code can “wait and talk in between”

This is the key design:

The model is not actually sleeping.

Instead:

1. Tool runs in external executor
2. Model gets intermittent updates
3. Model re-issues reasoning + next tool calls

So the loop is:

```
LLM → tool call → executor runs → event/progress → LLM → next action
```

---

## 6. “Searching for patterns (ctrl+o)” = log scanning tool

This part:

> Searched for 25 patterns…

is typically:

* grep-like scanning over logs
* or structured output parsing
* or regex filters applied to streaming stdout

Example:

```bash
grep -E "download|error|complete" log.txt
```

---

## 7. Why this architecture is used

Because it enables:

* long-running installs (minutes to hours)
* remote machines (SSH / containers)
* partial progress visibility
* autonomous recovery (retry if stuck)
* interactive agent behavior

Without it, the model would just “block and wait”, which is impossible in stateless inference.

---

## Mental model

Think of Claude Code not as “waiting”, but as:

> A controller that repeatedly delegates work to tools and reacts to their state updates.

---

If you want, I can break down how to build a minimal version of this (like a Python agent + subprocess monitor + event loop).
