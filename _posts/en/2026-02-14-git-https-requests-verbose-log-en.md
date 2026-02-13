---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Log Git HTTPS Requests Verbosely
translated: false
type: note
---

Question: When running git pull --rebase, how to log the HTTP and HTTPS requests?

Answer: 

Your example output shows an **SSH** connection (`Authenticated to github.com ([20.205.243.166]:22) using "publickey"`), **not** HTTP/HTTPS. GitHub uses SSH by default when your remote URL is in the `git@github.com:...` format.

To actually see HTTP/HTTPS traffic, you need to:

1. Make sure you're using an HTTPS remote (most common when you see password/PAT prompts)
2. Enable Git's built-in verbose logging for curl (which Git uses for http/https)

### Check your current remote URL

```bash
git remote -v
```

- If you see `git@github.com:...` → you're using **SSH**
- If you see `https://github.com/...` → you're using **HTTPS**

### Switch to HTTPS (if you want to log HTTP/HTTPS requests)

```bash
git remote set-url origin https://github.com/owner/repo.git
# or for GitHub with token: https://username:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/owner/repo.git
```

### Log HTTP/HTTPS requests (when using HTTPS remote)

Use one or more of these environment variables before the git command:

```bash
# Most useful & common combination – shows full curl verbose output (headers, TLS handshake, etc.)
GIT_CURL_VERBOSE=1 git pull --rebase

# Even more detailed (packet level + curl + general trace)
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_CURL_VERBOSE=1 git pull --rebase

# Save to file (very recommended)
GIT_CURL_VERBOSE=1 git pull --rebase 2>&1 | tee git-http.log

# Or maximum debugging
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_TRACE_CURL=1 GIT_CURL_VERBOSE=1 git pull --rebase 2>&1 | tee git-debug.log
```

### What each variable does

- `GIT_CURL_VERBOSE=1` → shows all curl verbose messages (like `curl -v`), including:
  - All request/response headers
  - TLS negotiation
  - Redirects
  - Sent/received data size
- `GIT_TRACE=1` → shows which git internal commands are run
- `GIT_TRACE_PACKET=1` → shows low-level smart-http protocol packets (sideband, flush, etc.)
- `GIT_TRACE_CURL=1` → (Git ≥ 2.9) even more curl-related trace info

### Quick one-liner examples

```bash
# Quick look at headers & TLS
GIT_CURL_VERBOSE=1 git pull --rebase

# Very detailed log saved to file
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_CURL_VERBOSE=1 git fetch --verbose 2>&1 | tee ~/git-network.log
```

### If you want to log SSH instead

For SSH protocol logging:

```bash
GIT_SSH_COMMAND="ssh -vvv" git pull --rebase
```

or even more verbose:

```bash
GIT_SSH_COMMAND="ssh -vvvv" git pull --rebase 2>&1 | tee ssh-debug.log
```

Use `GIT_CURL_VERBOSE=1` when your remote uses `https://` — that's the standard way to see HTTP and HTTPS requests made by Git.

References:  

- [Git Internals - Environment Variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
- [GitLab Docs - Troubleshooting Git (debug HTTPS)](https://docs.gitlab.com/topics/git/troubleshooting_git)
- [Stack Overflow - Debug git/git-shell problems (GIT_CURL_VERBOSE)](https://stackoverflow.com/questions/6178401/how-can-i-debug-git-git-shell-related-problems)