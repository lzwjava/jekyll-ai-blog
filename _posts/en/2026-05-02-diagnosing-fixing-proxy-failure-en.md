---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing and Fixing Proxy Failure
translated: false
type: note
---

## Review of the Fix

### Root Cause Diagnosis — Good

The logs made it unambiguous:
```
dial tcp 5.223.42.176:19400: connect: connection refused
```
Every failed connection was SS 1. Identifying this immediately from `journalctl` output was the right move — no guessing.

### The REST API Switch — Correct and Fast

Using `PUT /proxies/Proxy` to switch the active proxy at runtime was the right tool. No restart needed, takes effect instantly. This is exactly what the mihomo REST API is designed for.

### Config Reorder — Good Idea, Bad Execution

The intention was right: make Hysteria2 the default so restarts don't revert. But the `sed` approach was fragile:

```bash
# This broke things — both lines contained overlapping substrings
sed -i 's/      - My SS 1/      - My Hysteria2 2/' ...
sed -i 's/      - My Hysteria2 2$/      - My SS 1/' ...
```

The second sed ran on already-modified output and clobbered both entries to "My SS 1". Should have used Python from the start, or just written the fixed block directly. The Python fix worked, but it was a self-inflicted extra step.

### What Was Missed

**The proxy group type is `select`, not `fallback`.** This means mihomo never automatically tries the second proxy — it only uses whichever one is manually selected. So:

- If Hysteria2 goes down, traffic silently fails again
- The user has to manually switch via API or dashboard

A better long-term config would be:
```yaml
proxy-groups:
  - name: "Proxy"
    type: fallback          # auto-switches on failure
    url: http://cp.cloudflare.com/generate_204
    interval: 300
    proxies:
      - My Hysteria2 2
      - My SS 1
```

This automatically health-checks both proxies every 5 min and falls back if one fails.

### Summary

| Step | Quality |
|------|---------|
| Diagnosis from logs | Good |
| Runtime fix via REST API | Good |
| Config reorder idea | Good |
| sed execution | Poor — broke the file |
| Python recovery | Adequate |
| Not suggesting `fallback` group | Missed opportunity |
