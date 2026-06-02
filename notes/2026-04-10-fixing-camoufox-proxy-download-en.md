---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Slow Camoufox Proxy Download
translated: false
type: note
---

Question: Why is the Camoufox download stuck at 0% with proxychains4 npx camoufox-js fetch showing 15659.0s remaining, and how do I install Hermes?

Answer:

The issue you're facing is that the Camoufox download is extremely slow (estimated ~4 hours or more at current speed) or completely stuck at 0% progress. This is very common when using **proxychains** because:

- Proxychains forces every connection through your proxy (SOCKS/Tor/etc.), which often makes large binary downloads painfully slow or unstable.
- Many CDNs and download hosts (like those serving Camoufox binaries) have poor performance or even block/abort connections coming from proxies/Tor.
- The progress bar is shown by the downloader inside npx camoufox-js, and it's not handling slow/unstable proxy connections well.

### Quick fixes to try (in order):

1. **Skip proxychains for the download** (recommended first step)
   Run the command without proxychains:
   ```
   npx camoufox-js fetch
   ```
   This lets the download use your normal internet connection, which is usually much faster.

2. If you really need the proxy for privacy:
   - Try a different/better proxy in your `/opt/homebrew/etc/proxychains.conf`
   - Use a faster proxy (residential or high-bandwidth one) instead of Tor if you're using Tor.
   - Increase the number of threads/chains in proxychains config if supported.

3. **Alternative installation methods for Hermes (assuming you want to install Hermes agent with Camoufox)**

   If the above still fails, try these steps:

   - Cancel the current stuck process (Ctrl+C)
   - Clear any partial download cache:
     ```
     rm -rf ~/.cache/camoufox* || true
     rm -rf /tmp/camoufox* || true
     ```
   - Then retry without proxy:
     ```
     npx camoufox-js fetch
     ```

   After successful fetch, continue with Hermes installation. Typically it would be something like:
   ```
   # After Camoufox is fetched
   npx camoufox-js install   # or whatever the Hermes install command is
   ```

   If you are following a specific Hermes installation guide, share the exact commands or GitHub repo link for more precise help.

4. **Other common causes & solutions**:
   - Low disk space → check with `df -h`
   - Network issues even without proxy → test normal speed with `curl -I https://example.com` or speedtest
   - Old npx cache → try `npx --yes camoufox-js fetch` or clear npm cache: `npm cache clean --force`
   - Antivirus/Firewall interfering (rare on macOS)

The "15659 seconds" (~4.35 hours) is the estimated time remaining based on current download speed. At 0% with such high ETA, it usually means the connection is either extremely throttled or barely moving.

**Best immediate action:**
Cancel it (`Ctrl+C`), remove proxychains from the command, and retry the fetch. It should complete in seconds or a couple of minutes on normal internet.

If it still fails, please provide:
- The exact Hermes installation guide you're following
- Your proxychains.conf content (hide sensitive parts)
- Any error messages after it eventually fails

That will help me give more targeted troubleshooting.
