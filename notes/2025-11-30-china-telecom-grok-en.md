---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: China Telecom to Grok Internet Path
translated: false
type: note
---

Here’s a simple step-by-step explanation of how your internet connection in China (using China Telecom as ISP) eventually reaches the Grok servers (which are outside China).

1. Your home device (phone/laptop) → WiFi router
   Your router is configured with PPPoE dial-up: it uses the username (something like `xxxxxx@189gd`) and password that China Telecom gave you to “dial” and get a public IP address.

2. Your router → China Telecom’s local access equipment
   - If you use FTTH (fiber to the home, most common now), your router (or the ONT optical modem) connects via fiber to the neighborhood OLT.
   - If you still use ADSL, it goes over the old copper telephone line.
   The PPPoE session terminates at China Telecom’s BRAS (Broadband Remote Access Server) in your city/province. This is the point where you are authenticated and get your public IPv4 address (or IPv6).

3. China Telecom provincial network → China Telecom national backbone (CN2 or 163)
   - Ordinary traffic usually goes over the cheaper 163 backbone (AS4134).
   - More expensive “CN2 GIA” (AS4809) is used by some business lines or when you buy “global access” packages, but most home users are on 163.

4. China Telecom’s international gateway (the Great Firewall)
   To leave China, all traffic must pass through one of the ~10 huge international gateways (mainly in Beijing, Shanghai, Guangzhou).
   Here the GFW (Great Firewall) inspects, filters, and sometimes blocks or throttles packets. This is why many overseas sites are slow or unreachable without a VPN.

5. From China Telecom gateway → overseas carriers
   After exiting China, typical routes for Grok/xAI traffic look like this (real traceroute example from a China Telecom line in Guangdong):

   ```
   China Telecom gateway (202.97.x.x or 59.43.x.x) in Guangzhou/Shanghai
   → China Telecom’s partner in Hong Kong or Los Angeles (e.g., Tata, NTT, Cogent)
   → Transit providers in the US (Cogent, Hurricane Electric, Level3/Belden, etc.)
   → Cloudflare (Grok is behind Cloudflare) edge node (usually Los Angeles, San Jose, or Seattle for China-origin traffic)
   → xAI’s origin servers (in the US, probably Oregon or Iowa data centers)
   ```

6. How you actually reach Grok smoothly
   Because Grok is blocked or extremely slow on normal China Telecom home lines (163 backbone + GFW throttling), most users in China do one of the following:

   - Use a VPN or V2Ray/Shadowsocks that exits in Hong Kong, Japan, Singapore, or the US → bypasses the GFW throttling, gets much lower latency (50-150 ms instead of 300-800 ms or timeout).
   - Use airport/IPLC/IEPL dedicated lines (some people buy “CN2 GIA” home broadband or enterprise lines that are less throttled).
   - Access via grok.com or x.com through Cloudflare’s China network (CDN nodes in mainland China), but currently Grok itself does not have mainland CDN nodes, so the final connection to the Grok backend still has to go out and come back, hence still slow/blocked without circumvention.

Summary (your traffic flow when everything works with a VPN):

You at home (Guangzhou)
→ China Telecom fiber → provincial BRAS
→ China Telecom backbone
→ Your VPN server (e.g., in Hong Kong or Japan)
→ Normal internet → Cloudflare → xAI Grok servers in USA
← response comes back the same way

Without a VPN or special line, the packet usually gets severely delayed or dropped at step 4 (international gateway), so you can’t use Grok normally on a standard China Telecom home connection. This is the reality for almost all overseas AI services (ChatGPT, Claude, Grok, etc.) from mainland China.
