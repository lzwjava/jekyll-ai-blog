---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Ollama's Text File Busy Error
translated: false
type: note
---

Question: What is happening with the Ollama installation, and how do I fix the "text file busy" error to get Ollama running?

Answer:

The "text file busy" error (`ETXTBSY`) means the OS has the binary **memory-mapped or open by a running process**, so you can't overwrite it in place. This commonly happens when:

- A crashed/zombie process still holds the file open
- systemd is attempting to restart the service in a loop
- A partial install left the binary in a locked state

## Step-by-Step Fix

### 1. Stop everything touching the binary

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo pkill -9 ollama
sudo fuser -k /usr/local/bin/ollama   # force-release any open file handles
```

### 2. Verify nothing holds it open

```bash
sudo lsof /usr/local/bin/ollama
# Should return nothing
```

### 3. Remove the broken binary (don't overwrite — delete first)

```bash
sudo rm -f /usr/local/bin/ollama
```

Deleting (unlink) works even when overwriting fails, because `rm` removes the **directory entry**, not the file data. Any process still holding it open keeps its own reference until it exits.

### 4. Reinstall Ollama cleanly

```bash
curl -fsSL https://ollama.com/install.sh | sudo sh
```

Or manually if the network is slow:

```bash
# Download to a temp location first
curl -L https://ollama.com/download/ollama-linux-amd64 -o /tmp/ollama-new
sudo install -m 755 /tmp/ollama-new /usr/local/bin/ollama
```

### 5. Re-enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### 6. Verify it's listening

```bash
curl http://localhost:11434/api/tags
```

---

## Why `status=203` (EXEC failure)?

systemd error code 203 means the binary either:
- **Doesn't exist** at the expected path
- **Isn't executable** (wrong permissions)
- **Has a missing shared library** (`ldd` would show broken deps)
- **Architecture mismatch** (e.g., ARM binary on x86)

After reinstalling, run `ldd /usr/local/bin/ollama` to confirm all libraries resolve correctly before starting the service.

References:

- [Ollama Linux Installation](https://ollama.com/download/linux)
- [Understanding systemd exit code 203](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)
- [Linux ETXTBSY explanation](https://man7.org/linux/man-pages/man2/open.2.html)
