---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Sleep Wake Network Delay
translated: false
type: note
---

This is a classic macOS wake-from-sleep networking issue.

When you open the lid, macOS resumes from sleep. The WiFi interface comes back up, but the network stack isn't fully ready yet — TCP connections fail at the SSL handshake because the underlying socket gets a connection reset or times out before the network is actually usable.

The sequence:

1. Lid opens → macOS wakes
2. WiFi reconnects (takes 2-5 seconds)
3. DNS starts working
4. TCP connections become reliable
5. TLS/SSL handshakes succeed

You ran `git pull` during step 2-3, before the network was stable.

The fix is simple — just wait a few seconds after opening the lid, then retry:

```bash
git pull
```

If you want a more robust approach, you can wrap it with a retry:

```bash
for i in 1 2 3; do git pull && break; sleep 3; done
```

Or if this happens frequently, you can force git to use a specific TLS backend and add a connection timeout:

```bash
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 10
```

This makes git retry if the connection is too slow during the first 10 seconds, rather than failing immediately with the SSL error.

Also — if you're using a proxy (which I know you are with hysteria2), the proxy tunnel itself needs to re-establish after sleep, which adds even more delay. The SSL_ERROR_SYSCALL specifically suggests the connection was reset mid-handshake, which is exactly what happens when the network drops out from under an in-progress connection.
