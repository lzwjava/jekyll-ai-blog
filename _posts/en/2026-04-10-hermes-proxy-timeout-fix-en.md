---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Proxy Network Timeout Fix
translated: false
type: note
---

Question: Why did I get this TypeError: terminated with ETIMEDOUT when running start_proxy in hermes-agent on Node.js v25.3.0?

Answer:

This error is a network timeout issue that occurred inside Node.js's HTTP/HTTPS client (using the undici library) while your `hermes-agent` was trying to make an outgoing request.

### What happened:
- The code tried to fetch something over the network (likely an HTTPS request).
- The connection was established, but then the read operation timed out (`read ETIMEDOUT`).
- Node.js's `undici` fetch implementation detected the abort/timeout and threw `TypeError: terminated`.
- The root cause is `Error: read ETIMEDOUT` with errno -60 (which is a common macOS timeout error).

### Common reasons for this in `hermes-agent start_proxy`:
1. **Network connectivity problems** — Your internet connection dropped momentarily, or there's high latency/packet loss.
2. **Proxy or firewall interference** — Since you're running `start_proxy`, hermes-agent is probably trying to connect through a proxy, to a proxy, or to some remote service. Firewalls, corporate proxies, or VPNs often cause timeouts.
3. **Target server is slow or unreachable** — The remote endpoint hermes-agent is contacting (for example, a configuration server, authentication service, or upstream proxy) is not responding quickly enough.
4. **DNS resolution or routing issues** — Especially common on macOS when switching networks or using certain Wi-Fi setups.
5. **Timeout settings too low** — hermes-agent or Node.js might have a short default timeout for requests.
6. **macOS-specific networking quirks** — The errno -60 and the TLS socket close point to a system-level socket timeout, which happens more frequently on macOS with certain network configurations.

### How to fix it:
- Check your internet connection and try again.
- If you're behind a corporate/VPN/proxy network, try disabling the VPN temporarily or check proxy settings in hermes-agent.
- Run `start_proxy` with more verbose logging if the tool supports it (e.g., `DEBUG=* start_proxy` or any `--verbose` flag) to see exactly which URL is being requested and timing out.
- Increase network timeout if hermes-agent has a configuration option for it.
- Restart your router/modem or switch to a different network (mobile hotspot) to test.
- Update Node.js or check if there's a newer version of `hermes-agent`.
- As a quick test: run `curl https://www.google.com` (or the suspected target domain) in terminal to verify basic connectivity.

If the error keeps happening, share:
- The full command you ran (`start_proxy` with any arguments?)
- Any output before the error
- What `hermes-agent` is supposed to do (is it a custom tool, open-source project, or internal?)
- Your network setup (home, office, VPN?)

That will help narrow it down further.

References:
- None (error analysis based on standard Node.js/undici behavior)
