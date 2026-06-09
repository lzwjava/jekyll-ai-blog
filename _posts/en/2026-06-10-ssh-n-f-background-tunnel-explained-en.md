---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH -N -f Background Tunnel Explained
translated: false
type: note
---

Question: Why does the SSH command with `-N -f` exit immediately, while similar SSH commands without those flags stay running until `Ctrl+C`?

Answer:

The difference comes down to the meaning of the SSH flags you used:

1. **`-L 5001:127.0.0.1:5001`**

   * This sets up a **local port forwarding**: your local port `5001` forwards to `127.0.0.1:5001` on the remote host.

2. **`-N`**

   * Tells SSH **not to execute any remote commands**. It only sets up the port forwarding.

3. **`-f`**

   * Requests SSH to **go into the background** just before executing the command. This is typically used with `-N` so the SSH tunnel runs in the background without keeping a terminal open.

So your command:

```bash
ssh -L 5001:127.0.0.1:5001 amd-cloud -N -f
```

* Sets up the tunnel, then **immediately backgrounds itself**, which is why your terminal prompt returns right away.
* The tunnel is still running in the background; you can check it with `ps aux | grep ssh` or try connecting to `localhost:5001`.

In contrast, when you SSH without `-N -f`, like:

```bash
ssh -L 5001:127.0.0.1:5001 openclaw
```

* SSH logs you into the remote host and keeps the session **interactive**.
* The process stays in the foreground until you press `Ctrl+C` or `exit`.
* The port forwarding works as long as the session is alive.

**Key takeaway:**

* `-N -f` → background tunnel only, exits terminal immediately.
* No `-N -f` → foreground interactive session, stays until manually terminated.

You can also combine them depending on whether you want to keep the terminal free or stay logged in.

References:

* [SSH Manual: `-N` and `-f`](https://man.openbsd.org/ssh)
* [SSH Port Forwarding](https://www.ssh.com/academy/ssh/tunneling)
