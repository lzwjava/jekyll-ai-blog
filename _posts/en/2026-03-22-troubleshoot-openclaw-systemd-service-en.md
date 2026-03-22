---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshoot Failed Openclaw Systemd Service
translated: false
type: note
---

Question: How can I find out why the `openclaw-gateway.service` systemd user service failed?

Answer:

The service shows `status=1/FAILURE` but the log is truncated. Here are the ways to dig deeper:

## 1. Check Full Journal Logs (Most Useful)

```bash
journalctl --user -u openclaw-gateway.service -n 100 --no-pager
```

Or follow live as it restarts:
```bash
journalctl --user -u openclaw-gateway.service -f
```

## 2. Check Logs Since Last Boot

```bash
journalctl --user -u openclaw-gateway.service -b
```

## 3. See the Full Error With Verbose Output

```bash
journalctl --user -u openclaw-gateway.service -n 50 --no-pager -o verbose
```

## 4. Run the Binary Directly to See Raw Error

Since it's a Node.js process, run it manually to capture stderr:

```bash
/usr/bin/node /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js gateway --host 0.0.0.0 2>&1
```

This will print the exact error to your terminal without systemd swallowing it.

## 5. Check If Node or the Module Has Issues

```bash
# Check node is working
node --version

# Check if the module exists
ls /home/lzw/.npm-global/lib/node_modules/openclaw/dist/index.js

# Check for missing dependencies
cd /home/lzw/.npm-global/lib/node_modules/openclaw && npm ls 2>&1 | grep "missing\|UNMET"
```

## Quick Diagnosis Summary

| Symptom | Likely Cause |
|---|---|
| `MODULE_NOT_FOUND` | Missing npm dependency |
| `EADDRINUSE` | Port already in use |
| `EACCES` | Permission denied on port/file |
| `SyntaxError` | Node.js version incompatible |
| `ENOENT` | Config file or path not found |

**Start with `journalctl --user -u openclaw-gateway.service -n 100 --no-pager`** — that will almost always show you the exact error message from Node.js.