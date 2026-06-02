---
audio: false
generated: true
image: false
lang: en
layout: post
title: Detecting GFW Blocked Server IPs
translated: false
type: note
---

Question: When an IP on a cloud server is blocked by the GFW in China, how can we detect it, and how can we test its delay or latency from many places around the world? What tools or sites are used for this?

Answer:

The **Great Firewall of China (GFW)** is China's internet censorship system that can block access to specific IP addresses (or domains) from within mainland China. When a cloud server IP gets blocked by the GFW, users inside China typically cannot reach the server (connections time out, get reset, or fail), while the server remains accessible from the rest of the world. Blocking is often IP-based, so all services on that IP may be affected.

### How to Detect If an IP Is Blocked by the GFW
You cannot reliably detect the block from outside China alone, because the GFW acts on traffic entering or leaving China. The most effective way is to test **reachability and response from locations inside or near China**:

- Use online **China Firewall Test** tools that simulate access from multiple Chinese cities (e.g., Beijing, Shanghai, Guangzhou, Shenzhen). These tools attempt to connect to your domain or IP from servers located behind the GFW.
  - Recommended sites:
    - https://www.chinafirewalltest.com/ (powered by ViewDNS.info)
    - https://www.websitepulse.com/tools/china-firewall-test (tests from Shanghai, Beijing, Guangzhou, and Hong Kong for comparison)
    - https://en.greatfire.org/analyzer (GreatFire Analyzer – supports IP and domain checks)
    - https://www.comparitech.com/privacy-security-tools/blockedinchina/
    - https://www.dotcom-tools.com/china-firewall-test (multiple mainland China locations)

- For direct IP testing, use **multi-location ping tools that include probes in China**. If pings or connections from Chinese probes fail (high packet loss, timeouts, or no response) while succeeding from other global locations, it strongly indicates a GFW block.
  - A commonly recommended tool for this is **ping.pe**, which has test locations inside China.

Other signs of GFW blocking:
- Connections from China fail with TCP resets or timeouts, but work fine elsewhere.
- The block may be partial (some cities affected) or evolve over time.

Note: GFW blocking is not something your cloud provider controls, and it can happen to VPN/proxy servers or sites with certain content.

### How to Test Delay (Latency) from Many Places Worldwide
To measure latency (ping/delay), packet loss, and reachability from dozens or hundreds of global locations, use **free multi-location ping or latency test websites**. These tools run tests in parallel from servers around the world and display results in a table (min/avg/max latency, packet loss).

Popular and reliable tools include:
- **https://tools.keycdn.com/ping** — Pings from many global locations in parallel.
- **https://globalping.io/** — Free platform for ping, traceroute, HTTP, and DNS tests from thousands of probes worldwide (very flexible).
- **https://www.uptrends.com/tools/ping-test** — Tests from 40+ checkpoints with traceroute data.
- **https://ping.pe** — Simple simultaneous pings from global locations, including China (useful for GFW detection).
- **https://hostingchecker.com/tools/ping/** — Quick ping from 10+ locations.
- **https://wondernetwork.com/pings** — Global ping statistics between major cities.
- Others worth trying: Bunny Tools latency test, LocaPing, or Meter.net world ping test.

**How to use these tools**:
1. Enter your server's IP address (or domain name).
2. Run the test — results show latency from each location.
3. Look for patterns: Normal low latency worldwide but very high latency, packet loss, or complete failure from Chinese locations usually means GFW blocking.

For more advanced diagnosis, some tools also provide traceroute to see where the connection drops.

### Additional Tips
- Combine both types of tests: First check China-specific firewall testers, then confirm with global latency tools that include Chinese probes.
- If the IP is blocked, common workarounds (not always reliable long-term) include changing the IP, using a different cloud provider/region, or advanced proxy/VPN techniques — but these may still get detected over time.
- Tests are real-time and free, but results can vary slightly due to routing or temporary network issues.

These methods give you a clear picture of whether the IP is blocked specifically by the GFW and how the server's performance looks globally.

References:
- https://www.chinafirewalltest.com/
- https://www.websitepulse.com/tools/china-firewall-test
- https://en.greatfire.org/analyzer
- https://tools.keycdn.com/ping
- https://globalping.io/
- https://www.iozoom.com/client/knowledgebase/127/China-Great-Firewall-GFW-block.html
