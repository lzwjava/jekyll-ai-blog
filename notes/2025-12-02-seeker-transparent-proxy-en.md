---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: "Seeker: Transparent Proxy Tool"
translated: false
type: note
---

Question: What is the GitHub repository https://github.com/gfreezy/seeker about?

Answer:
The GitHub repository [gfreezy/seeker](https://github.com/gfreezy/seeker) is an open-source tool written primarily in Go that implements a transparent proxy using a TUN virtual network interface. It enables seamless routing of network traffic (TCP, UDP, and ICMP/pings) through proxies like Shadowsocks, SOCKS5, or HTTP on macOS and Linux systems. The project emulates Surge's enhanced mode for local traffic interception and gateway mode for proxying devices on a local area network (LAN).

### Key Features
- **Transparent Proxying**: Intercepts and routes traffic via TUN without needing to configure individual applications.
- **Proxy Support**: Prioritizes SOCKS5, then Shadowsocks, then HTTP (note: HTTP only supports TCP CONNECT, no UDP).
- **Rule Engine**: Uses Clash-compatible rules (e.g., DOMAIN, DOMAIN-SUFFIX, IP-CIDR) with actions like PROXY, DIRECT, REJECT, or PROBE.
- **DNS Handling**: Automatically starts a local DNS server (127.0.0.1) and restores it on exit; supports Fake-IP resolution for ICMP pings.
- **Remote Configuration**: Loads configs from subscription URLs (Base64-encoded) or encrypted YAML files (using ChaCha20-IETF).
- **Optimization**: Server switching based on thresholds, failure protection, and timeouts for connections/reads/writes.
- **Gateway Mode**: Proxies entire LAN traffic by setting DNS to 0.0.0.0:53 and adjusting device gateways.

### Installation
Download pre-built binaries from the [releases page](https://github.com/gfreezy/seeker/releases) for macOS or Linux, then make executable:
```
chmod +x seeker-osx  # macOS
chmod +x seeker-linux  # Linux
```
To build from source:
```
git clone https://github.com/gfreezy/seeker.git
cd seeker
OPENSSL_STATIC=yes cargo build --release
```
The binary will be in `target/release/seeker`.

### Usage Example
Run with a local YAML config (requires sudo for TUN setup):
```
sudo seeker --config path/to/config.yml
```
For a remote encrypted config:
```
sudo seeker --config-url https://example.com/encrypted-config.txt --key mypassword
```
Generate an encrypted config:
```
seeker --config config.yml --encrypt --key mypassword > encrypted-config.txt
```
A sample config is available [here](https://github.com/gfreezy/seeker/blob/master/sample_config.yml), supporting native server formats or Clash-style `proxies`.

### Warnings
- Avoid TUN IP conflicts with your network; no duplicate TUN names.
- In SOCKS5/HTTP modes, add direct domains to the config to prevent loops.
- On macOS, allow unsigned binaries in System Preferences > Security & Privacy.
- Ubuntu users may need to resolve DNS issues (e.g., disable systemd-resolved if using dnsmasq).
- Licensed under Apache-2.0 or MIT.

This tool is useful for users needing a lightweight, rule-based proxy setup similar to commercial apps like Surge or Clash, especially in censored network environments.

*[GitHub - gfreezy/seeker](https://github.com/gfreezy/seeker)*
