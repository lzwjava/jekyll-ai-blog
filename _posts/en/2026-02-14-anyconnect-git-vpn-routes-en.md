---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AnyConnect Routes Git Over VPN
translated: false
type: note
---

Question: Does software like Cisco AnyConnect on macOS force git pull over SSH to go through the VPN/proxy? And if I use Cisco AnyConnect, do I not need to set HTTP/HTTPS proxy in environment variables or System Settings?

Answer:

**Yes — in most corporate setups, Cisco AnyConnect forces your `git pull` over SSH to go through the VPN tunnel.**
This happens because AnyConnect typically modifies your macOS routing table to send **all** (or most) outbound traffic through the corporate VPN — including SSH traffic on TCP port 22 to github.com or other git hosts.

### Key points about Cisco AnyConnect behavior on macOS

- **Full tunnel (most common in enterprises)**:
  The VPN server pushes a policy (often "tunnel-all" or "full tunnel") that changes your default route.
  → **All internet traffic** — including SSH to github.com (port 22), git over HTTPS (port 443), browsers, etc. — goes through the VPN tunnel.
  → Your `git pull` (SSH) automatically uses the VPN path without any extra configuration.

- **Split tunnel (less common, but possible)**:
  Only specific corporate IP ranges/subnets go through the VPN; everything else (like github.com) goes directly out your normal internet connection.
  → In this case, SSH to public git hosts **bypasses** the VPN (same as when VPN is off).

Most companies use **full tunnel** for security/compliance reasons (to force all traffic through corporate firewall, proxy, inspection, DLP, etc.). So in practice: **yes, your SSH-based git pull will go through the VPN** when AnyConnect is connected.

### Do you still need to set HTTP_PROXY / HTTPS_PROXY env vars or macOS System Settings proxy?

**No — you usually do NOT need them when using AnyConnect (especially in full-tunnel mode).**

- AnyConnect **does not** use or require the standard `http_proxy`/`https_proxy` environment variables for its own operation (it's an SSL VPN tunnel, not an HTTP proxy).
- For **git over HTTPS** (`https://github.com/...`):
  → Traffic already goes through the VPN tunnel → the corporate network's upstream proxy (if any) is applied transparently by the corporate firewall/router.
  → You **don't** set `HTTP_PROXY` yourself; the company handles proxying inside the tunnel.

- For **git over SSH** (`git@github.com:...`):
  → SSH is **not** HTTP-based → it ignores `HTTP_PROXY`/`HTTPS_PROXY` completely anyway.
  → But because the VPN routes all traffic, SSH packets still travel through the corporate VPN → any corporate SSH inspection/proxy/jump-host (rare) would apply transparently.

- macOS System Settings → Network → Proxies:
  → AnyConnect often **overrides** or **ignores** these settings while connected (especially in full-tunnel mode).
  → Many users report that proxy settings in System Preferences get bypassed or changed by AnyConnect.

**Bottom line**
When Cisco AnyConnect is connected (especially full-tunnel corporate VPN):

- You **don't** need to manually set `export HTTP_PROXY` / `HTTPS_PROXY` or configure proxies in System Settings for git (SSH or HTTPS) to work.
- Everything is routed through the VPN automatically → corporate network handles any required proxying/firewall rules.

If your git pull still fails/slows down:

- Check if it's full-tunnel vs split-tunnel (ask IT or run `netstat -nr` / `route get github.com` before/after connecting).
- Corporate proxies sometimes break SSH → switch to HTTPS remote (`git remote set-url origin https://github.com/...`) if allowed.
- VPN MTU/fragmentation issues can slow git → try `git config --global http.postBuffer 524288000` (for HTTPS) or lower MTU.

References:

- [Cisco AnyConnect Administrator Guide - Proxy & Tunnel Policies](https://www.cisco.com/c/en/us/td/docs/security/vpn_client/anyconnect/Cisco-Secure-Client-5/admin/guide/b-cisco-secure-client-admin-guide-5-1/m_configure_vpn_access-noth.html)
- [Apple Discussions - Cisco AnyConnect routes all traffic](https://discussions.apple.com/thread/253565623)
- [Super User - Cisco AnyConnect forces all traffic](https://superuser.com/questions/284709/how-to-allow-local-lan-access-while-connected-to-cisco-vpn)
- [Cisco Community - AnyConnect Split vs Full Tunnel](https://community.cisco.com/t5/security-knowledge-base/anyconnect-split-tunneling-local-lan-access-split-tunneling/ta-p/4050866)
