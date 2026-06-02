---
audio: false
generated: true
image: false
lang: en
layout: post
title: Telnet Proxy and macOS Behavior
translated: false
type: note
---

**Question:** How does Telnet work? Does it apply HTTP or HTTPS proxy settings on macOS? And compared to `ping` (which bypasses proxies), does `telnet` go through a proxy if one is configured?

---

**Answer:**

## How Telnet Works

Telnet is a client-server application protocol that provides access to virtual terminals of remote systems on local area networks or the Internet. It is a protocol for bidirectional 8-bit communications.

Telnet uses TCP as its underlying transport protocol. The client sends commands to the server, and the server responds with output, allowing the user to interact with the remote system's command-line interface. It primarily uses port 23 for communication.

Here's the connection flow step by step:

1. **You type:** `telnet hostname port`
2. The Telnet client transforms the characters into a universal character set called Network Virtual Terminal (NVT) characters and passes them to the local TCP/IP protocol stack. These NVT characters travel through the Internet and arrive at the TCP/IP stack at the remote computer.
3. The remote Telnet server converts those characters into a format understandable by the remote computer. The remote operating system receives them from a pseudo-terminal driver and passes them to the appropriate application program.

**Key characteristics:**
- Telnet is neither encrypted nor secure. Because it is a plain text protocol, anyone on the network can access usernames, passwords, and other private information typed during Telnet sessions.
- A Telnet client is one of the most useful tools available for any enterprise applications administrator. Because Telnet is a very simple protocol, the client can be used for purposes other than creating a connection to a remote Telnet server — in particular, for testing general TCP connectivity.

---

## Does `telnet` Use macOS HTTP/HTTPS Proxy Settings?

**No, `telnet` does NOT automatically use macOS HTTP or HTTPS proxy settings.**

Here's why:

**macOS system proxy settings** (configured in System Settings → Network → Proxies) define:
- Web Proxy (HTTP)
- Secure Web Proxy (HTTPS)
- SOCKS Proxy
- FTP Proxy

Mac OS X does a good job of juggling proxy configurations for graphical applications, but this functionality doesn't extend to command-line work in Terminal. Command-line tools like `git`, `npm`, `pip`, or `homebrew` do not automatically inherit the system proxy.

The macOS HTTP/HTTPS proxy is specifically designed for **HTTP protocol traffic**. Telnet establishes a **raw TCP connection** on any arbitrary port — it does not speak the HTTP protocol, so macOS has no basis to route it through an HTTP proxy.

Some graphical applications (GUI-based software) do not use the system's proxy settings. As a result, even if an intermediary server is configured at the network level, these programs may ignore it and require manual configuration. If an application does not support proxy configuration at all, special utilities such as Proxifier can be used to intercept traffic and route it through the configured proxy server.

---

## `ping` vs `telnet` Proxy Behavior — Compared

| Tool | Protocol | Uses macOS HTTP Proxy? | Uses macOS SOCKS Proxy? | Notes |
|---|---|---|---|---|
| `ping` | ICMP | ❌ No | ❌ No | ICMP operates at Layer 3; proxies work at Layer 4/7 |
| `telnet` | TCP (raw) | ❌ No | ❌ No (by default) | CLI tools don't auto-read macOS proxy |
| Safari / Chrome | HTTP/HTTPS | ✅ Yes | ✅ Yes | GUI apps respect system proxy |

**Why `ping` bypasses proxies:**
`ping` uses **ICMP** (Internet Control Message Protocol), which works at the network layer — below TCP. Proxies (HTTP, SOCKS) operate at the transport/application layer. There is simply no mechanism for a proxy to intercept ICMP traffic.

**Why `telnet` also bypasses proxies by default:**
`telnet` is a CLI tool. The macOS proxy system doesn't automatically configure the command-line network proxy. Unlike browsers, `telnet` makes a **direct TCP connection** and does not consult `HTTPEnable`, `HTTPSEnable`, or `SOCKSEnable` system settings on its own.

---

## How to Force `telnet` Through a Proxy

If you want `telnet` (or other CLI tools) to go through a proxy, you have these options:

**Option 1 — Use environment variables (for HTTP-aware CLI tools):**
```bash
export http_proxy="http://proxyhost:port"
export https_proxy="http://proxyhost:port"
```
Note: `telnet` itself ignores these, but other CLI tools like `curl` or `wget` will respect them.

**Option 2 — Use `nc` (netcat) with a SOCKS proxy:**
```bash
nc -x proxyhost:1080 -X 5 targethost targetport
```

**Option 3 — Use Proxifier or similar tools** to force all traffic from specific apps (including CLI tools) through a system SOCKS proxy.

**Option 4 — Read macOS proxy settings dynamically in a script:**
The `scutil --proxy` command allows access to system proxy configuration. You can use `awk` to parse its output and export `http_proxy` accordingly in your shell profile.

---

## Summary

- **Telnet** creates a raw TCP connection using the Telnet protocol; it sends and receives plain text with no encryption.
- **macOS HTTP/HTTPS proxy settings** only affect applications that explicitly implement proxy-awareness — mostly GUI browsers and some CLI tools that check environment variables.
- **Both `ping` and `telnet`** bypass the macOS system proxy by default — `ping` because ICMP cannot be proxied, and `telnet` because it is a raw TCP CLI tool that does not query macOS proxy settings.
- To route `telnet` through a proxy, you need a third-party tool like Proxifier, or use `nc` with SOCKS flags manually.

---

**References:**

- [Telnet - Wikipedia](https://en.wikipedia.org/wiki/Telnet)
- [Telnet Explained - ClouDNS](https://www.cloudns.net/blog/telnet-explained-what-is-it-and-how-it-works/)
- [Introduction to TELNET - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-to-telnet/)
- [Mac OS X Network Proxy Settings in Terminal – dmorgan.info](https://dmorgan.info/posts/mac-network-proxy-terminal/)
- [Guide to enable macOS Terminal to respect system proxy – GitHub Gist](https://gist.github.com/MuntashirAkon/fc6e7e85ada12fa1576dd0fe5ff8da8f)
- [MacOS Proxy Settings Guide](https://proxy-ipv4.com/en/blog/how-to-configure-macos-proxy-settings-correctly/)
