---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Fingerprint Saved Locally
translated: false
type: note
---

Question: If you type "yes" on the RunPod proxy SSH connection, does it save the fingerprint locally?

Answer: Yes. Any time SSH prompts `Are you sure you want to continue connecting (yes/no/[fingerprint])?` and you answer `yes`, it appends an entry to your local `~/.ssh/known_hosts` file — regardless of whether you're connecting via the proxy (`ssh.runpod.io`) or direct TCP.

The entry looks like:

```
ssh.runpod.io ssh-ed25519 AAAA...<key-data>
```

For the proxy case specifically:

- The key gets stored keyed on the hostname `ssh.runpod.io` (default port 22, so no port suffix needed).
- Since RunPod's proxy always presents the *same* host key for `ssh.runpod.io` (it's the gateway machine's key, not your pod's), that one `known_hosts` entry covers **all** your pods forever — that's exactly why you don't get re-prompted next time, even for a different pod.

For the direct TCP case:

- The entry gets stored as `[213.173.99.50]:26246 ssh-ed25519 AAAA...` (bracket+port notation since it's non-default port).
- This entry is specific to that exact IP:port. New pod → new IP/port → new entry needed → new prompt.

You can verify what's saved:

```bash
grep runpod ~/.ssh/known_hosts
ssh-keygen -F ssh.runpod.io   # check if a specific host is already trusted
```

And if RunPod ever rotates their proxy's host key (rare, but possible during infra changes), you'd get a `REMOTE HOST IDENTIFICATION HAS CHANGED` warning and need to remove the stale entry:

```bash
ssh-keygen -R ssh.runpod.io
```

References:

- [OpenSSH known_hosts man page](https://man.openbsd.org/ssh#known_hosts)
- [RunPod SSH docs](https://docs.runpod.io/pods/configuration/use-ssh)
