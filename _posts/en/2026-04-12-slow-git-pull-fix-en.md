---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slow Git Pull Through Proxy Fix
translated: false
type: note
---

Question: Is the Git pull speed of only 38.00 KiB/s on a DMIT.io Los Angeles node proxy correct, and is it considered slow?

Answer:

Yes, the speed shown in your `git pull` output (3.49 MiB received at **38.00 KiB/s**) is **very slow** for a modern VPS connection, especially on a DMIT Los Angeles node. Normal GitHub downloads over a decent connection should reach several MB/s (megabytes per second), not kilobytes. 38 KiB/s is roughly dial-up era performance and indicates a bottleneck.

### Why is it slow in this case?
Your setup is using a local **HTTP/HTTPS proxy** at `http://127.0.0.1:7890` (common with tools like Clash, V2Ray, or similar proxies). The output shows:

- Git successfully authenticates via SSH public key to GitHub.
- It then falls back to receiving objects over what appears to be an **HTTPS path** routed through the proxy.

Common reasons for this slowness on a DMIT LA node + proxy:

- **Proxy overhead and routing**: The proxy (running on your local machine or VPS) may have limited bandwidth, high latency, or poor routing to GitHub's CDN servers (which often resolve to Los Angeles-area IPs). Even though the VPS is in LA, the proxy can introduce extra hops, packet loss, or throttling.
- **Git protocol mismatch**: SSH authentication worked, but object transfer is likely using HTTPS through the proxy, which is frequently slower than native SSH for large transfers.
- **Known GitHub download issues**: GitHub clones/pulls can be slow due to CDN routing, congestion, or temporary problems. Many users report speeds dropping to 50-100 KiB/s in certain regions or through proxies/VPNs.
- **DMIT-specific factors**: While DMIT LA nodes generally offer good performance (especially Premium/CN2 GIA plans with high bandwidth to Asia), proxy usage can negate that advantage if the proxy itself is the weak link.

### Quick checks and fixes to try
1. **Test without proxy**:
   - Temporarily unset the proxy in your shell:
     ```
     unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
     ```
   - Then run `git pull` again and compare the speed.

2. **Force Git to use SSH fully** (often faster):
   - Change your remote to SSH if it's not already:
     ```
     git remote set-url origin git@github.com:username/repo.git
     ```
   - Ensure your SSH key is set up correctly.

3. **Increase Git buffer size** (helps with slow/unstable connections):
   ```
   git config --global http.postBuffer 524288000
   ```

4. **Use a shallow pull** if you don't need full history:
   ```
   git pull --depth=1
   ```

5. **Check proxy performance**:
   - Test general download speed through the proxy (e.g., `curl -x http://127.0.0.1:7890 -I https://github.com` or a speed test).
   - Try a different proxy endpoint or disable it temporarily.
   - If the proxy is for bypassing restrictions (e.g., from China), test direct connection or a different proxy location.

6. **Other diagnostics**:
   - Run `ping github.com` and `traceroute github.com` (or `mtr github.com`) from the VPS to check latency/packet loss.
   - Check current GitHub status for any ongoing issues.

In summary: **No, this speed is not right** — it's abnormally slow and worth troubleshooting. The DMIT LA node itself should support much higher throughput; the proxy or Git configuration is the most likely culprit here. Try the steps above and see if speeds improve to MB/s range.

References:
- GitHub community discussions on slow downloads (various reports of <100 KiB/s through proxies or bad routing)
- Stack Overflow threads on GitHub slow clones and proxy impacts
- General reports of Git HTTPS vs SSH speed differences
