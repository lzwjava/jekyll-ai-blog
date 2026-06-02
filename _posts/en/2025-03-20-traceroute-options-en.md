---
audio: false
generated: true
lang: en
layout: post
title: Traceroute Options
translated: false
type: note
---

Traceroute is a powerful tool for diagnosing network paths, and while its basic use is straightforward, it offers advanced options to customize its behavior. Below, I’ll outline common options and explain how to use traceroute in advanced ways, focusing on practical examples. The exact options depend on your operating system (e.g., Windows uses `tracert`, while Linux/macOS use `traceroute`), but I’ll cover the most widely applicable ones.

### Basic Usage
- **Linux/macOS**: `traceroute [destination]`
  - Example: `traceroute google.com`
- **Windows**: `tracert [destination]`
  - Example: `tracert google.com`

This shows the hops (routers) between you and the target, along with round-trip times (RTT) for each.

---

### Common Traceroute Options
Here’s a rundown of key options, primarily for the `traceroute` command on Unix-like systems (Linux/macOS). Windows `tracert` has fewer options but shares some concepts.

1. **`-n` (No DNS Lookup)**
   - Skips resolving IP addresses to hostnames, speeding up the process and showing raw IPs.
   - Use: `traceroute -n google.com`
   - Why: Useful when DNS resolution is slow or you only care about IPs.

2. **`-m [max_hops]` (Set Maximum Hops)**
   - Limits how many hops traceroute checks before giving up (default is often 30).
   - Use: `traceroute -m 15 google.com`
   - Why: Prevents endless runs if the target is unreachable or far away.

3. **`-q [nqueries]` (Number of Queries per Hop)**
   - Sets how many packets are sent per hop (default is 3). Each query shows a latency value.
   - Use: `traceroute -q 1 google.com`
   - Why: Reduces output clutter or speeds up the trace; increase it for more reliable latency data.

4. **`-w [waittime]` (Wait Time per Hop)**
   - Sets how long (in seconds) to wait for a response before marking a hop as timed out.
   - Use: `traceroute -w 2 google.com`
   - Why: Adjusts for slow networks or reduces delays on fast ones.

5. **`-p [port]` (Specify Port, UDP Mode)**
   - Sets the destination port for UDP-based traceroute (default is often 33434+).
   - Use: `traceroute -p 53 google.com`
   - Why: Targets specific services (e.g., DNS on port 53) or bypasses filters blocking ICMP.

6. **`-I` (Use ICMP Instead of UDP)**
   - Switches from UDP (default on many systems) to ICMP Echo Request packets.
   - Use: `traceroute -I google.com`
   - Why: Some networks block UDP but allow ICMP, improving visibility.

7. **`-T` (TCP Mode)**
   - Uses TCP packets instead of UDP or ICMP, often with SYN packets.
   - Use: `traceroute -T -p 80 google.com`
   - Why: Bypasses firewalls that block ICMP/UDP; great for tracing to web servers (port 80 = HTTP).

8. **`-f [first_ttl]` (Start at Specific TTL)**
   - Sets the initial TTL value, skipping earlier hops.
   - Use: `traceroute -f 5 google.com`
   - Why: Focuses on a specific part of the path, e.g., beyond your local network.

9. **`-g [gateway]` (Loose Source Routing)**
   - Forces packets through a specified gateway (if supported by the network).
   - Use: `traceroute -g 192.168.1.1 google.com`
   - Why: Tests specific routes or bypasses default routing.

10. **`-4` or `-6` (Force IPv4 or IPv6)**
    - Restricts traceroute to IPv4 or IPv6.
    - Use: `traceroute -6 google.com`
    - Why: Ensures you’re testing a specific protocol, useful for dual-stack networks.

---

### Windows `tracert` Options
Windows has fewer options, but here are the main ones:
- **`-d`**: No DNS lookups (like `-n`).
- **`-h [max_hops]`**: Max hops (like `-m`).
- **`-w [timeout]`**: Wait time in milliseconds (like `-w`).
- Example: `tracert -d -h 20 google.com`

---

### Advanced Usage Examples
Here’s how to combine options for specific purposes:

1. **Diagnose a Slow Connection**
   - Goal: Pinpoint where latency spikes.
   - Command: `traceroute -I -q 5 -w 1 google.com`
   - Why: ICMP for reliability, 5 queries for better latency stats, 1-second timeout to move quickly.

2. **Bypass Firewall Restrictions**
   - Goal: Trace to a web server blocked by ICMP filters.
   - Command: `traceroute -T -p 443 google.com`
   - Why: TCP on port 443 (HTTPS) mimics legitimate traffic, often allowed through firewalls.

3. **Test Beyond Your ISP**
   - Goal: Skip local hops to focus on external routing.
   - Command: `traceroute -f 3 -m 10 google.com`
   - Why: Starts at hop 3 (past your router/ISP), limits to 10 hops total.

4. **Compare IPv4 vs. IPv6 Paths**
   - Goal: See if protocol choice affects routing.
   - Commands:
     - `traceroute -4 google.com`
     - `traceroute -6 google.com`
   - Why: Identifies differences in network paths or performance.

5. **Silent, Fast Trace for Scripting**
   - Goal: Quick output for automation.
   - Command: `traceroute -n -q 1 -w 1 google.com > output.txt`
   - Why: No DNS, one query, short timeout, redirected to a file.

---

### Tips for Advanced Use
- **Combine with Other Tools**: Pair traceroute with `ping` (for latency) or `mtr` (real-time traceroute) for deeper insights.
- **Understand Network Context**: Firewalls, NAT, or VPNs can obscure hops (showing asterisks `*`)—adjust protocols (ICMP/TCP) to adapt.
- **Root Privileges**: On Unix systems, some options (e.g., TCP mode) may require `sudo` for raw socket access: `sudo traceroute -T google.com`.

Traceroute’s power lies in its flexibility. By tweaking options, you can tailor it to troubleshoot specific network issues, bypass restrictions, or analyze routing behavior in detail. Let me know if you want to dive deeper into a particular scenario!
