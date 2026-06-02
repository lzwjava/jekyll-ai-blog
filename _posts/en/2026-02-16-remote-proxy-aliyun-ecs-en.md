---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Proxy Setup on Aliyun ECS
translated: false
type: note
---

Question: What if I use one server in Aliyun CN in China, so that on my personal laptop I don't need to set up this, and use that as an HTTP or HTTPS proxy, or SOCKS?

Answer:

Yes, this is a common and practical setup: run **Clash** (or a similar proxy tool) on your Aliyun ECS server in mainland China, then configure your laptop to use that server as a remote proxy (via HTTP/HTTPS or SOCKS5). This way, the complex rule-based routing logic (like the one in your log) lives only on the server, and your laptop stays clean — you just set a single proxy address in system settings, browser, or applications.

### Key Advantages of This Approach

- Laptop becomes very simple: no Clash/Verge installation, no subscription management, no TUN/virtual network adapter, no background service eating resources.
- All smart routing (Apple direct, GitHub/Singapore node, Google node, etc.) happens on the server.
- You can still achieve domain-based or rule-based splitting if needed (by keeping rules on server).
- Works for both HTTP/HTTPS proxy and SOCKS5.

### How to Implement It (Recommended Path)

1. **Choose Clash mode on the server**
   - Use **Clash in mixed-port mode** (most common and easiest).
   - In your `config.yaml` on the server, enable:

     ```yaml
     mixed-port: 7890          # both HTTP and SOCKS5 listen on same port
     allow-lan: true           # very important — allows connections from your laptop
     bind-address: "0.0.0.0"   # listen on all interfaces (or your public IP)
     ```

   - Keep your existing rules/proxies/groups as they are (the ones from your log).
   - Start Clash normally (systemd service recommended for always-on).

   → After this, the server exposes:
   - HTTP/HTTPS proxy at `http://your-aliyun-ip:7890`
   - SOCKS5 proxy at `socks5://your-aliyun-ip:7890`

2. **Security (very important on public cloud)**
   - **Do not expose 7890 directly to the whole internet** — high risk of abuse/scanning.
   - Best options (choose one):
     - **Authentication** — set `authentication` in config:

       ```yaml
       authentication:
         - "username:strongpassword"
       ```

       Then use `http://username:strongpassword@your-ip:7890` on laptop.
     - **IP whitelist** — use Aliyun security group to allow only your home/public IP to port 7890.
     - **SSH tunnel** (simplest & very secure, no port open):
       - On laptop: `ssh -D 10801 -N user@your-aliyun-ip`
       - Then set laptop SOCKS5 proxy to `127.0.0.1:10801`
     - **Reverse tunnel** or **frp/intra** if you want to avoid opening any port.

3. **On your laptop — configuration**
   - **Simplest** — system-wide proxy (macOS/Windows):
     - HTTP/HTTPS proxy: `your-aliyun-ip:7890` (with auth if set)
     - SOCKS proxy: same address/port
   - Or per-app (recommended to avoid breaking domestic services):
     - Browser extensions: Proxy SwitchyOmega / SwitchySharp → set rules or PAC
     - Use a lightweight client like **Proxifier** (Windows) or **Proxie** (macOS) to route only foreign domains/apps through the remote proxy.
   - If you still want rule-based splitting on laptop → you can use a very simple Clash/Verge config on laptop with only one outbound: the remote Aliyun server as `socks5` or `http` proxy, and minimal rules (or even Global mode).

4. **Alternative lightweight servers (if you don't want full Clash on VPS)**
   If Clash feels too heavy on the server or you only need basic forwarding:
   - **sing-box** or **hysteria2** server mode (very popular in 2025–2026)
   - **tinyproxy** or **squid** — pure HTTP proxy (no SOCKS, no rules)
   - **3proxy** or **gost** — small binary, supports HTTP + SOCKS5 + auth
   - But if you like your current rule logic (Apple direct, GitHub node, etc.), stick with Clash.

### Potential Downsides / Things to Watch

- Latency: every packet goes laptop → Aliyun → target → Aliyun → laptop (adds ~10–60 ms depending on your location).
- Bandwidth & cost: Aliyun mainland outbound traffic can be expensive if you watch a lot of YouTube/Netflix.
- Stability: Clash on server needs to be monitored (restart on crash, log rotation).
- Domestic sites: if you use system proxy, Aliyun → domestic site → Aliyun → you creates hairpinning and slows things down. → Better to use rule mode on server + selective proxy on laptop.
- Aliyun detection: heavy proxy traffic from mainland ECS sometimes gets QoS-limited or flagged — choose low-profile usage.

In short: yes — this is one of the cleanest ways to remove complexity from your daily laptop while keeping smart routing. Most people who do this either:

- Run full Clash + auth + security group restriction, or
- Use SSH dynamic forwarding (-D) for zero-configuration security.

If you tell me more about your laptop OS and whether you prefer max simplicity or still want some rules locally, I can give more exact steps.

References:

- [Clash official documentation on mixed-port and allow-lan](https://github.com/Dreamacro/clash/wiki/configuration)
- [Common setups for Clash on VPS as remote proxy](https://medium.com/@royso/clash-unlocking-restricted-network-and-streaming-services-4d4c1a034d8e)
- [Security group and proxy auth recommendations from community guides](https://blog.csdn.net/YUNZHUJI4613/article/details/147579676)
