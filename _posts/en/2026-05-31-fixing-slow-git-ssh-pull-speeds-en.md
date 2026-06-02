---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Slow Git SSH Pull Speeds
translated: false
type: note
---

Here's the full breakdown of the investigation and fix.

---

## Problem

Git pull on `Qwen2.5-Coder` was downloading at 81 KiB/s through SSH (`git@github.com:QwenLM/Qwen2.5-Coder.git`), pulling 2976 objects (~30 MB).

---

## Investigation Steps

### Step 1: Check git remote and proxy config

```bash
git -C /Users/lzwjava/projects/Qwen2.5-Coder remote -v
# → git@github.com:QwenLM/Qwen2.5-Coder.git (SSH)

git config --global --list | grep -iE 'proxy|http'
# → http.proxy=127.0.0.1:7890
# → https.proxy=127.0.0.1:7890
```

The HTTP proxy (7890) is configured for git, but the remote uses SSH — so git's `http.proxy` doesn't apply. SSH has its own proxy path.

### Step 2: Check SSH config

```bash
cat ~/.ssh/config
```

Found the key line:

```
Host !192.168.*.*
    ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

This means **all non-local SSH connections** (including GitHub) go through `ncat` → SOCKS5 proxy at `localhost:7891`. This is the SSH data path, separate from git's HTTP proxy.

### Step 3: Check what's running on the proxy ports

```bash
lsof -i :7890 -sTCP:LISTEN
lsof -i :7891 -sTCP:LISTEN
```

Both ports are served by `mihomo-da` (PID 86998) — that's mihomo (Clash Meta), your local proxy. Port 7890 = HTTP proxy, port 7891 = SOCKS5 proxy. Both are healthy.

### Step 4: Test proxy speed directly

```bash
curl -x socks5h://localhost:7891 -o /dev/null -w "speed: %{speed_download}\n" https://github.com
# → ~1 MB/s — proxy is fast

curl -x http://127.0.0.1:7890 -o /dev/null -w "speed: %{speed_download}\n" https://github.com
# → ~980 KB/s — also fast
```

**Conclusion:** The proxy itself is not the bottleneck. Both HTTP and SOCKS5 routes are fast for HTTPS traffic.

### Step 5: Test SSH auth speed

```bash
time ssh -T git@github.com
# → 3.6 seconds, authenticated successfully
```

SSH handshake is fine. The slowness is in the **data transfer phase** after auth, not the connection setup.

### Step 6: Identify the bottleneck

The chain is: `git fetch` → SSH → `ncat` → SOCKS5 proxy (7891) → mihomo → internet.

`ncat` (from nmap 7.98) is the weak link. It's designed as a network utility, not a high-throughput SSH tunnel proxy. For small packets (auth, handshake) it's fine. For sustained large transfers (git packfiles), it adds significant overhead — the 81 KiB/s vs 1 MB/s difference.

Compare: HTTPS goes through `git` → libcurl → HTTP proxy (7890) → mihomo → internet. No `ncat` in the chain. libcurl is optimized for bulk transfers.

### Step 7: Test HTTPS fetch

```bash
GIT_TRACE=1 git -C /Users/lzwjava/projects/Qwen2.5-Coder fetch --depth=1
# → 413 objects in ~77 seconds, completed successfully
```

Timestamps from the trace:
```
14:01:45.303  index-pack started (receiving data)
14:03:02.436  index-pack done
```

~77 seconds for 413 objects. The original SSH pull was fetching 2976 objects — that would have taken ~10+ minutes at 81 KiB/s.

---

## What Was Done

Switched all 5 Qwen repos from SSH to HTTPS:

```
Qwen2-Audio:    git@github.com → https://github.com/QwenLM/Qwen2-Audio.git
Qwen2.5-Coder:  git@github.com → https://github.com/QwenLM/Qwen2.5-Coder.git
Qwen2.5-Math:   git@github.com → https://github.com/QwenLM/Qwen2.5-Math.git
Qwen2.5-VL:     git@github.com → https://github.com/QwenLM/Qwen2.5-VL.git
Qwen3:          already HTTPS (no change)
```

Command used:
```bash
git -C /path/to/repo remote set-url origin https://github.com/QwenLM/RepoName.git
```

Auth works automatically because `git-credential-manager` is configured.

---

## Key Takeaways

1. **SSH proxy ≠ HTTP proxy in git.** `http.proxy` only affects HTTPS remotes. SSH remotes use `~/.ssh/config` ProxyCommand.
2. **`ncat` is slow for bulk SSH tunneling.** Fine for small exchanges, terrible for large packfile transfers. If you ever need SSH through a proxy, `connect` (from `brew install connect`) or `nc -X 5 -x localhost:7891` are faster alternatives.
3. **For large repos (model weights, datasets), prefer HTTPS** when you have a fast HTTP proxy. The libcurl path is optimized for bulk data; SSH through SOCKS5 adds overhead.
4. **Diagnostic commands to remember:**
   - `lsof -i :PORT -sTCP:LISTEN` — what's listening
   - `curl -x socks5h://localhost:PORT -o /dev/null -w "%{speed_download}" URL` — test proxy speed
   - `GIT_TRACE=1 git fetch` — see exactly where git spends time
   - `git config --global --list | grep proxy` — check proxy config
