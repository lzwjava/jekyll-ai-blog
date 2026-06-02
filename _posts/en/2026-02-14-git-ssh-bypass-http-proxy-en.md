---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Git SSH Bypasses HTTP Proxies Completely
translated: false
type: note
---

Question: When running GIT_SSH_COMMAND="ssh -vvv" git pull --rebase using SSH, does it bypass the system's HTTP & HTTPS proxy settings like export HTTP_PROXY and macOS network proxy settings in System Settings?

Answer:

**Yes, it bypasses them completely.**

### Why this happens

- Git has two completely different transport protocols:
  - **HTTPS** protocol (`https://github.com/...` URLs) → Git uses libcurl internally → respects standard proxy environment variables (`http_proxy`, `https_proxy`, `HTTP_PROXY`, `HTTPS_PROXY`, `all_proxy`) and macOS system network proxy settings (which curl usually honors via macOS APIs or environment variables)
  - **SSH** protocol (`git@github.com:...` or `ssh://git@github.com/...` URLs) → Git simply runs the `ssh` command (or the one specified via `GIT_SSH_COMMAND` / `core.sshCommand`) → **SSH client never looks at HTTP/HTTPS proxy variables**

`ssh` (OpenSSH) does **not** read or use `HTTP_PROXY`, `HTTPS_PROXY`, or macOS system HTTP/HTTPS proxy settings for its own connections. Those variables are only meaningful to HTTP/HTTPS-speaking clients (like curl, git over https, wget, etc.).

### Summary table

| Protocol used by Git | Uses HTTP_PROXY / HTTPS_PROXY? | Uses macOS System Settings HTTP proxy? | Controlled by          |
|----------------------|--------------------------------|----------------------------------------|------------------------|
| HTTPS                | Yes                            | Yes (via curl / system integration)    | env vars + git config http.proxy |
| SSH                  | No                             | No                                     | ssh config (~/.ssh/config) + GIT_SSH_COMMAND |

### How to make SSH go through a proxy (if needed)

You must configure the **SSH client** itself to use a proxy — common methods:

1. **HTTP CONNECT proxy** (most corporate HTTP proxies)

   ```bash
   # In ~/.ssh/config
   Host github.com
       ProxyCommand connect -H proxy.example.com:8080 %h %p
   ```

   (requires `connect` tool or similar — install via brew install connect or similar)

2. **SOCKS5 proxy** (common with tools like Shadowsocks, v2ray, Clash, etc.)

   ```bash
   # In ~/.ssh/config
   Host github.com
       ProxyCommand nc -x 127.0.0.1:1080 %h %p
   ```

   or

   ```bash
   GIT_SSH_COMMAND="ssh -o ProxyCommand='nc -x 127.0.0.1:1080 %h %p'" git pull --rebase
   ```

3. **Jump host / bastion** (ProxyJump)

   ```bash
   GIT_SSH_COMMAND="ssh -J user@bastion.example.com" git pull --rebase
   ```

4. **SSH over HTTPS port 443** (GitHub supports this)
   - Change remote to `ssh://git@ssh.github.com:443/user/repo.git`
   - This still uses SSH protocol (not HTTP), but travels over TCP/443 — may bypass some firewalls, but **still does not use HTTP_PROXY**.

### Quick check what protocol you're using

```bash
git remote -v
```

- `git@github.com:...` or `ssh://` → SSH (ignores HTTP proxies)
- `https://github.com/...` → HTTPS (uses HTTP/HTTPS proxies)

So when you run `GIT_SSH_COMMAND="ssh -vvv" git pull --rebase` and see SSH authentication / port 22 traffic, you're using the SSH protocol — HTTP/HTTPS proxy settings (including macOS system ones) are completely ignored.

References:

- [Git - Environment Variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
- [Configure Git to use a proxy (HTTPS or SSH+GIT)](https://gist.github.com/ozbillwang/005bd1dfc597a2f3a00148834ad3e551)
- [Use Proxy for Git/GitHub](https://gist.github.com/coin8086/7228b177221f6db913933021ac33bb92)
- [How do I pull from a Git repository through an HTTP proxy?](https://stackoverflow.com/questions/128035/how-do-i-pull-from-a-git-repository-through-an-http-proxy)
