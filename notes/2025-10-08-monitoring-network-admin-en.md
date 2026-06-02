---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Monitoring Network Activity with Admin Rights
translated: false
type: note
---

### Monitoring HTTP Requests and TCP Connections with Admin Rights

Assuming you're working on a Linux/Unix-like system (e.g., Ubuntu, CentOS) with root/admin privileges, you can monitor network activity ethically for troubleshooting, security auditing, or pentesting. **Important: Only do this on systems you own or have explicit permission for—unauthorized monitoring is illegal.** I'll focus on command-line tools, which are lightweight and don't require GUI.

#### 1. **Monitor All TCP Connections**
   Use built-in tools like `ss` (modern replacement for `netstat`) or `tcpdump` for real-time capture. These show active connections, ports, and processes.

   - **List all current TCP connections (static view):**
     ```
     sudo ss -tunap
     ```
     - `-t`: TCP only.
     - `-u`: UDP if needed (but you asked for TCP).
     - `-n`: Numeric ports (no DNS resolution).
     - `-a`: All states (established, listening, etc.).
     - `-p`: Show owning processes.
     Output example:
     ```
     tcp   ESTAB  0      0      192.168.1.10:80     10.0.0.5:54321    users:(("nginx",pid=1234,fd=5))
     ```
     For listening sockets only: `sudo ss -tlnp`.

   - **Real-time monitoring with watch:**
     ```
     watch -n 1 'sudo ss -tunap'
     ```
     Refreshes every second.

   - **Capture live TCP traffic (packet-level):**
     Install `tcpdump` if not present: `sudo apt update && sudo apt install tcpdump` (Debian/Ubuntu) or `sudo yum install tcpdump` (RHEL/CentOS).
     ```
     sudo tcpdump -i any tcp -n -v
     ```
     - `-i any`: All interfaces.
     - `-n`: No name resolution.
     - `-v`: Verbose.
     Add `port 80 or port 443` to filter HTTP/HTTPS: `sudo tcpdump -i any tcp port 80 or tcp port 443 -n -v -A` (`-A` for ASCII payload, to see HTTP headers).

     Save to file for later analysis: `sudo tcpdump -i any tcp -w capture.pcap`.

#### 2. **Monitor HTTP Request Logs**
   HTTP logs depend on your web server (Apache, Nginx, etc.). If no web server is running, use network capture (above) to inspect HTTP traffic. For server-specific logs:

   - **Apache (httpd):**
     Logs are typically in `/var/log/apache2/access.log` (Ubuntu) or `/var/log/httpd/access_log` (CentOS).
     ```
     sudo tail -f /var/log/apache2/access.log
     ```
     - Shows requests in real-time: IP, timestamp, method (GET/POST), URL, status code.
     Example line: `192.168.1.100 - - [08/Oct/2025:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234`.

     For all logs: `sudo grep "GET\|POST" /var/log/apache2/access.log | less`.

   - **Nginx:**
     Logs in `/var/log/nginx/access.log`.
     ```
     sudo tail -f /var/log/nginx/access.log
     ```
     Similar format to Apache.

   - **If no web server (general HTTP sniffing):**
     Use `tcpdump` as above with `-A` to dump HTTP payloads, or install `ngrep` for regex matching:
     ```
     sudo apt install ngrep  # Install if needed
     sudo ngrep -d any 'GET|POST|HTTP' -O http_capture.pcap
     ```
     This filters and logs HTTP methods.

   - **Advanced: Set up a transparent proxy for full logging.**
     Install Squid proxy: `sudo apt install squid`.
     Configure `/etc/squid/squid.conf` to log all HTTP (add `access_log /var/log/squid/access.log squid`).
     Redirect traffic via iptables: `sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128`.
     Then tail the Squid log: `sudo tail -f /var/log/squid/access.log`.

#### Tips for "Hacking" (Ethical Pentesting)
- **Combine tools:** Pipe `tcpdump` to `grep` for specific patterns, e.g., `sudo tcpdump -i any tcp port 80 -A | grep "User-Agent"`.
- **Visualize with Wireshark:** For GUI analysis, install Wireshark (`sudo apt install wireshark`), run as root, and open your `.pcap` file.
- **Security hardening:** After monitoring, clear logs if sensitive: `sudo truncate -s 0 /var/log/access.log`.
- **Cross-platform note:** On Windows (with admin), use `netstat -anob` for TCP and Event Viewer for logs. On macOS, `netstat -an` and `tcpdump`.

This setup gives you comprehensive visibility without external tools. Test in a VM first.

[Linux ss Command Man Page](https://man7.org/linux/man-pages/man8/ss.8.html)
[Tcpdump Tutorial](https://www.tcpdump.org/manpages/tcpdump.1.html)
[Apache Access Log Format](https://httpd.apache.org/docs/2.4/logs.html)
