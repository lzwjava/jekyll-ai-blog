---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Clash DNS Resolution Warnings Explained
translated: false
type: note
---

**Question:** Why are there so many of these Clash logs: "[TCP] dial DIRECT (match DomainSuffix/local) 127.0.0.1:... --> lzwjava.local:59822 error: couldn't find ip"?

**Answer:**

These warning logs in Clash (likely Clash for Windows or a similar client like Clash Verge) indicate repeated failed attempts to resolve and connect to the hostname **lzwjava.local** on port 59822.

### Key Breakdown of the Log

- **DomainSuffix/local**: A rule in your Clash configuration matches domains ending in `.local` (common for local network/multicast DNS hosts) and routes them to **DIRECT** (bypassing proxy).
- **127.0.0.1:... --> lzwjava.local:59822**: An application on your local machine (localhost, using different source ports like 49245–49255) tries to connect to `lzwjava.local:59822`.
- **error: couldn't find ip**: Clash attempts DNS resolution for `lzwjava.local` but fails to get an IP address.

### Why This Happens

- `.local` domains use **mDNS (multicast DNS)**, typically handled by services like Avahi (Linux) or Bonjour (Windows/macOS).
- Clash's built-in DNS resolver does not support mDNS queries. When routing DIRECT for `.local`, it relies on standard DNS, which cannot resolve `lzwjava.local` → failure.
- No IP found → connection fails → warning logged.

### Why So Many Logs

- An application on your machine repeatedly tries to connect to `lzwjava.local:59822`.
- Port **59822** suggests a service like **IntelliJ IDEA** or another Java IDE (JetBrains products) in "remote development" or "thin client" mode, where the IDE frontend connects to a backend server on a remote host or VM using a `.local` hostname.
- The app likely polls or retries the connection frequently (e.g., every few seconds for heartbeat/status checks), producing multiple rapid attempts (11 in quick succession here).
- Common triggers: IDE checking server status, auto-reconnect attempts, or background sync.

### How to Fix or Reduce Logs

1. **Add Host Mapping** (Quick Fix):
   - Edit your system's `hosts` file:
     - Windows: `C:\Windows\System32\drivers\etc\hosts`
     - macOS/Linux: `/etc/hosts`
   - Add: `127.0.0.1 lzwjava.local` (or the actual IP if it's another device).
   - This bypasses DNS lookup.

2. **Change Clash Rules**:
   - Remove or modify the `DOMAIN-SUFFIX,.local,DIRECT` rule to avoid DIRECT routing for unresolved hosts.
   - Or add a specific rule like `DOMAIN,lzwjava.local,REJECT` to block it silently.

3. **Disable the Feature in the Application**:
   - If it's JetBrains IDE (e.g., IntelliJ), check settings for "Remote Development" or "Gateway" connections and disable/disconnect from the server named "lzwjava".

4. **Enable Enhanced DNS in Clash** (if using Fake-IP or TUN mode):
   - Some versions handle local resolutions better with proper DNS settings, but mDNS support is limited.

These logs are harmless warnings (not errors crashing Clash), but they spam if the app keeps retrying. Fixing the resolution or stopping the connection attempts will eliminate them.

**References:**

- [GitHub Issue: clash-verge-rev #467 - Similar DNS resolve failed for direct-routed domains](https://github.com/clash-verge-rev/clash-verge-rev/issues/467)
- [GitHub Issue: vernesong/OpenClash #4244 - DNS resolution issues in Clash](https://github.com/vernesong/OpenClash/issues/4244)
- [Clash Documentation: Rules and DNS Behavior](https://en.clash.wiki/configuration/rules.html)
