---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Avoiding Docker Daemon Proxy Loops
translated: false
type: note
---

### Why `"no-proxy": "localhost,127.0.0.1,.local"` is Crucial in Docker's `daemon.json`

When you configure Docker's daemon with proxy settings like `"http-proxy": "http://localhost:7890"` (common for tools like Clash running locally), the daemon applies these rules to **all** outgoing network traffic by default. This includes connections to external registries (e.g., `registry-1.docker.io` for pulling images like `hello-world`).

However, without the `no-proxy` directive, Docker daemon also tries to route **local connections**—such as the initial TCP handshake to your proxy server itself at `localhost:7890`—through the same proxy. This creates a classic **proxy loop**:

1. Docker needs to fetch an image from `registry-1.docker.io`.
2. It attempts to connect via the proxy at `localhost:7890`.
3. But to reach `localhost:7890`, the proxy settings kick in again, forcing Docker to... connect via the proxy at `localhost:7890`.
4. This infinite recursion fails at the TCP level because the proxy can't proxy a connection to itself (it leads to a self-referential loop with no resolution).
5. The connection aborts unexpectedly, resulting in the `proxyconnect tcp: EOF` error (EOF means "end of file," signaling a premature closure during the proxy negotiation/handshake).

Adding `"no-proxy": "localhost,127.0.0.1,.local"` explicitly tells the daemon to **bypass the proxy** for traffic destined to:
- `localhost` (your machine's loopback hostname),
- `127.0.0.1` (IPv4 loopback address),
- `.local` domains (common for mDNS/local network resolution).

This allows Docker to connect **directly** to the proxy server on localhost without looping through itself. Once connected, the proxy can then handle the external request to the Docker registry properly (e.g., via HTTP CONNECT for HTTPS traffic).

In short: It prevents the daemon from "proxying the proxy," ensuring local proxy access works while still routing internet-bound traffic (like image pulls) through it.

If your setup involves other local services (e.g., internal registries or containers communicating locally), extending `no-proxy` with those domains/IPs can prevent similar issues.

[Docker Daemon Proxy Configuration](https://docs.docker.com/engine/daemon/proxy/)
[Docker Proxy Settings Forum Discussion](https://forums.docker.com/t/proxy-settings-for-the-docker-daemon/132089)
[Docker Proxy Guide for Corporate Firewalls](https://www.datacamp.com/tutorial/docker-proxy)
