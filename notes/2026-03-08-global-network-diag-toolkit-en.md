---
audio: false
generated: true
image: false
lang: en
layout: post
title: Global Network Diagnostic Toolkit
translated: false
type: note
---

Question: What is ping.pe and what does it do?

Answer:

## Overview of ping.pe

**ping.pe** is described as the best Ping + MTR combination ever, plus a TCP port checker, DNS diagnostics with `dig`, and a real-time BGP looking glass — all accessible from multiple global locations.

It is a **free, browser-based network diagnostic platform** that requires no installation and is widely used by network engineers, system administrators, and developers.

---

## Core Features

### 1. Ping (Multi-location)

ping.pe allows users to perform ping tests from over 20 global nodes simultaneously. It provides visual representation of network performance using color-coded result matrices for easy interpretation. This is especially useful to determine if a server is reachable from various regions around the world.

### 2. MTR (My TraceRoute)

ping.pe is praised for its awesome MTR and graphs, as well as a built-in screenshot capability. MTR combines traditional `ping` and `traceroute` into a single diagnostic tool, showing each hop along the network path along with latency and packet loss per hop — in real time.

### 3. TCP Port Check

ping.pe lets you test whether a specific TCP port on a remote host is open and reachable. This is essential for troubleshooting firewalls, services like web servers, SSH, databases, and more.

### 4. DNS Lookup with `dig`

The `dig` (Domain Information Groper) feature allows users to query DNS records (A, AAAA, MX, TXT, CNAME, etc.) for any domain, helping diagnose DNS propagation issues or misconfiguration.

### 5. BGP Looking Glass (Real-time)

A BGP Looking Glass (LG) server acts as a user-friendly front-end for BGP-speaking routers. It sends read-only commands to selected BGP routers within a certain Autonomous System (AS) and displays the output on a web page.

A BGP Looking Glass provides information including AS path information, peering information, prefix information, next-hop information, and BGP community information. AS path information shows the path taken by BGP routes as they traverse different autonomous systems.

ping.pe's BGP Looking Glass is available at `bgp-lg.ping.pe` and allows users to inspect how internet traffic routes globally to any IP or prefix.

---

## Who Uses ping.pe?

- **Network administrators** troubleshooting connectivity or routing issues
- **Server/VPS owners** checking if their IPs are reachable from different parts of the world
- **Developers and DevOps engineers** diagnosing latency or DNS problems
- **Gamers and remote workers** verifying stable low-latency connections

---

## Key Advantages

| Feature | Benefit |
|---|---|
| No installation needed | Works directly in browser |
| Multi-location testing | Identifies regional network issues |
| MTR + Ping combined | Deep hop-by-hop diagnosis |
| BGP Looking Glass | Advanced routing visibility |
| Free to use | No account required |
| Results retained 24 hours | Easy sharing and reference |

---

## How to Use It

Simply go to **<https://ping.pe/>** and enter a domain name or IP address. The tool will automatically run ping and MTR tests from multiple global nodes and display the results in a color-coded table. You can also navigate to sub-tools for TCP port checks, DNS lookups, and BGP analysis.

References:

- [ping.pe - Official Site](https://ping.pe/)
- [ping.pe BGP Looking Glass](https://bgp-lg.ping.pe/)
- [Ping.pe Overview - coolexplore.com](https://www.coolexplore.com/en/item/ping-ip)
- [What BGP Looking Glass servers are - noction.com](https://www.noction.com/blog/bgp-looking-glass-servers)
- [BGP Looking Glass explained - vpsie.com](https://vpsie.com/knowledge-base/bgp-looking-glass-comprehensive-list/)
