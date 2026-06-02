---
audio: false
generated: true
image: false
lang: en
layout: post
title: DNS Server Failure and Configuration Block
translated: false
type: note
---

The conversation revolved around persistent, severe network connectivity issues on the server (`lzw-server`).

Here is a summary of the events:

1. **The Problem:** Initial requests to check `weibo.com` via `ping` failed with a "Temporary failure in name resolution," and subsequent TCP connection attempts to various external services timed out (`i/o timeout`).
2. **Diagnosis:** We investigated DNS resolution using `nslookup`, which confirmed the local DNS server (`127.0.0.53`) was actively **refusing** the queries. This indicated a local network configuration problem, not a website outage.
3. **Root Cause:** The configuration file (`/etc/resolv.conf`) was managed by `systemd-resolved`, pointing to the local stub resolver.
4. **Proposed Solution:** We determined the fix would likely involve changing the nameserver in `/etc/resolv.conf` to your gateway (`192.168.1.1`) to force external DNS lookups.
5. **Roadblock:** Attempts to modify this file using `exec` (even with elevated privileges) failed with **"Permission denied,"** as the service aggressively manages the file.
6. **Next Steps:** The final advice was that if the file *were* changed, the DNS resolver service (`systemd-resolved`) would need to be restarted for the changes to take effect.

**In short: The server is having a fundamental problem resolving domain names because its internal DNS service is rejecting requests, and we were blocked from fixing the configuration due to file permission restrictions.**
