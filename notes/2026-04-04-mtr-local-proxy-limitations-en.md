---
audio: false
generated: true
image: false
lang: en
layout: post
title: MTR Through Local Proxy Limitations
translated: false
type: note
---

Question: Can we run MTR through a local proxy like Mihomo or Clash on port 7890 etc.?

Answer:

### Short Answer
**No, not directly and not reliably.**  

MTR (and the underlying `traceroute` + `ping` tools it uses) operates at a low network level using **ICMP** (for ping) and **UDP** or **ICMP** (for traceroute). Most local proxies like **Clash**, **Mihomo**, or similar tools primarily handle **TCP** (and sometimes UDP) traffic through **SOCKS5** or **HTTP** proxies. They do not natively support or forward raw **ICMP** packets in a way that standard command-line tools like `mtr` can use.

### Why It Usually Doesn't Work
- **Protocol Limitation**:  
  - Ping/MTR sends **ICMP Echo Request** packets.  
  - SOCKS5 proxies (the mixed-port 7890/7891/7892 in Mihomo/Clash) are designed for TCP/UDP connections, not raw ICMP.  
  - HTTP proxies are even more limited (Layer 7 only).

- **No Built-in Proxy Support in MTR**:  
  MTR does not have options like `--proxy`, `-x`, or environment variables (`http_proxy`, `all_proxy`) that work for it. Setting `all_proxy=socks5://127.0.0.1:7890` will be ignored by MTR because it bypasses the standard libc socket calls that respect those variables.

- **Common Result**:  
  When you try `mtr example.com` while the proxy is active (especially in TUN/redirect mode), MTR either:
  - Shows the local proxy as the only hop, or
  - Fails completely with high loss or "no route", or
  - Ignores the proxy and goes direct.

### Possible Workarounds (Limited Success)
Here are the realistic options, ranked from easiest to most complex:

1. **Use TUN Mode in Mihomo/Clash (Best for most users)**  
   Enable **TUN mode** (virtual network interface) in your Clash/Mihomo client.  
   This intercepts **all** traffic at the system level, including ICMP in many cases.  
   - Then run normal `mtr google.com`.  
   - Result: MTR traffic goes through the selected proxy node (if your rules allow it).  
   - Limitation: ICMP support in TUN mode varies by platform (better on Linux/macOS with proper setup; Windows is trickier). DNS resolution may also be affected if fake-IP is enabled.

2. **Set Rules to DIRECT for MTR**  
   In Mihomo/Clash config, add a rule so MTR's traffic bypasses the proxy:  
   - By process name: `PROCESS-NAME,mtr,DIRECT`  
   - Or by destination: specific domains/IPs set to DIRECT.  
   This lets you run MTR normally without proxy interference, but it does **not** route MTR *through* the proxy.

3. **Use Proxy-Aware Alternatives**  
   - **tcptraceroute** or **traceroute -T** (TCP-based traceroute) — these can sometimes work better with SOCKS5 if you wrap them with `proxychains` or `tsocks`.  
   - **proxychains-ng** (or `proxychains4`):  
     Install it, configure with your local SOCKS5 port (e.g., 7890), then run:  
     `proxychains mtr google.com`  
     Success rate: Low for ICMP-based MTR, better for TCP variants.  
   - **hping3** or custom scripts for ICMP over TCP tunnels (advanced, not recommended for daily use).

4. **Run MTR on a Remote Server**  
   SSH into a VPS that routes through your desired proxy/VPN, then run MTR there. This is often the cleanest way to test routing *through* a specific proxy path.

5. **Advanced Setup (Linux only)**  
   Use `redir`/`iptables` + `socat` or tools like `iproxy` to forward ICMP, but this is fragile and not worth it for most people.

### Recommendation
- For quick diagnostics of your **actual** network path (including the proxy effect), enable **TUN mode** and test MTR.  
- To see the path **inside** the proxy network, run MTR from a machine/VPS that is already behind the proxy.  
- If you only need latency/loss to the final destination (not hop-by-hop), use `ping` wrapped with `proxychains` or just test via curl/wget which respect the proxy.

In practice, most network engineers run MTR **without** the local proxy active when they want accurate hop-by-hop information, or they use it in TUN mode for a "proxied view".

If you tell me your operating system (Linux, macOS, Windows) and exact Mihomo/Clash setup (TUN enabled? mixed-port or SOCKS-only?), I can give more precise commands.

References:  
- None