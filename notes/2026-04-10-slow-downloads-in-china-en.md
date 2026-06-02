---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slow Downloads in China
translated: false
type: note
---

Question: Why is the Camoufox download with "npx camoufox-js fetch" so extremely slow in China, showing only 0% after a long time like 1523 seconds?

Answer:

The download is extremely slow because **Camoufox** (a custom Firefox-based browser for automation and anti-detection) fetches a large binary file (~300-400 MB) from **foreign/international servers** (likely hosted on AWS, GitHub, Fastly CDN, or similar overseas infrastructure).

### Main Reasons Why It's Slow in China:
- **Great Firewall of China (GFW)**: All traffic going in or out of mainland China must pass through a small number of international gateways. The GFW applies **Deep Packet Inspection (DPI)**, which deliberately introduces **packet loss**, throttling, and extra latency on connections to non-Chinese servers. This makes large file downloads crawl at a tiny fraction of your normal speed.
- **Cross-border bandwidth congestion**: International links from China are heavily shared and often congested, especially for downloads from popular Western CDNs.
- **No China-optimized CDN**: Unlike big companies (e.g., some use Alibaba Cloud or Tencent CDN inside China), Camoufox's download source does not have fast mirrors inside mainland China. The progress bar staying at 0% for 25+ minutes (1523 seconds ≈ 25 minutes) is very typical for such blocked/throttled downloads.

This is the same reason why downloading Playwright, Puppeteer, Chrome/Firefox binaries, or any large file from GitHub/AWS is notoriously slow or unstable from China.

### Solutions (Try in This Order):

1. **Use a Good VPN** (Most Effective)
   - Connect to a **high-quality VPN** with servers optimized for China (e.g., ones with obfuscated protocols or China-specific nodes).
   - Popular options that often work well for large downloads: Astrill, ExpressVPN, or paid services known to bypass GFW throttling.
   - Run the fetch command **while the VPN is connected**.
   - Note: Free VPNs usually make it worse.

2. **Force a Clean Retry**
   ```bash
   npx camoufox-js remove   # or camoufox remove if using Python version
   npx camoufox-js fetch
   ```
   Partial downloads can get corrupted, making it even slower.

3. **Improve Local Network**
   - Switch to a different ISP (e.g., try China Mobile vs China Telecom vs China Unicom — some have slightly better international routing).
   - Use wired connection instead of Wi-Fi.
   - Close other bandwidth-heavy apps.

4. **Download Manually (Advanced Workaround)**
   - Run the command with verbose logging if possible to see the exact download URL.
   - Once you see the URL, download it manually using a download manager, browser with VPN, or tools like `aria2c` / `wget` with better resume support.
   - Then place the file in Camoufox's cache directory (check the tool's documentation for the exact path).

5. **Wait and Retry Later**
   - Sometimes international routes improve during off-peak hours (late night or early morning in China).

Unfortunately, there is no official China mirror for Camoufox yet, so the VPN route is the most reliable fix for users inside mainland China.

If the download still fails or stays at 0% even with a VPN, share the full output (including any error after it eventually fails) and I can help further.

References:
- https://www.mlytics.com/blog/why-your-website-is-slow-in-china-and-how-to-fix-it-2024-total-guide-for-better-web-app-performance-in-china/
- https://www.thoughtworks.com/insights/blog/user-experience/foreign-websites-slower-China
- https://github.com/platformio/platformio-core/issues/4656
- Camoufox documentation mentions ~300-400MB download and notes on slow connections
