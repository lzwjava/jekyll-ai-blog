---
audio: false
generated: true
image: false
lang: en
layout: post
title: Analyzing TCP NAT Hijacking Traffic Manipulation
translated: false
type: note
---

Question: How can I analyze and monitor system-level TCP NAT hijacking and traffic manipulation on Linux, especially when using OpenWrt on old hardware, to understand where traffic hijacking happens and how each network layer handles forwarding?

Answer:

You’re essentially trying to dissect a multi-layered networking problem, where TCP traffic might be intercepted, redirected, or hijacked at various points in the system. Here’s a structured approach:

---

### 1. **Understand the Layers Involved**

In Linux networking, traffic goes through multiple layers:

1. **Application Layer**

   * Programs like `redsocks`, `shadowsocks`, VPN clients, browsers, or custom network daemons.
   * Can hijack traffic if they bind to certain ports or act as transparent proxies.

2. **Socket/Transport Layer (TCP/UDP)**

   * Linux kernel TCP stack processes connections.
   * Tools like `tcpdump`, `ss`, `netstat` help inspect active connections and retransmissions.

3. **Netfilter/Iptables Layer**

   * NAT rules (`PREROUTING`, `POSTROUTING`, `OUTPUT`) and chains like `REDSOCKS`.
   * Redirects traffic to user-space proxies or specific ports.

4. **Routing Layer**

   * The kernel’s routing table determines where packets go.
   * Misconfigured routes or default gateways can redirect traffic unintentionally.

5. **DNS Resolution Layer**

   * `/etc/resolv.conf` or custom DNS services.
   * If DNS is hijacked, traffic may resolve to malicious IPs.

6. **Network Interface / Hardware Layer**

   * NICs, switches, or Wi-Fi cards.
   * Can introduce packet loss, misrouting, or offloading issues.

---

### 2. **Traffic Capture and Logging**

To see where traffic is intercepted:

* **Kernel-level TCP dump:**

  ```bash
  tcpdump -i any tcp port 80 or port 443 -vv
  ```

  * Captures all TCP traffic at the interface layer.

* **Netfilter logging:**

  ```bash
  iptables -t nat -A PREROUTING -p tcp -j LOG --log-prefix "PREROUTING: "
  iptables -t nat -A REDSOCKS -j LOG --log-prefix "REDSOCKS: "
  ```

  * Logs packets entering NAT chains. Useful to see if traffic hits the expected rules.

* **Application-level logs:**

  * `redsocks` or `shadowsocks` can log connections, errors, and redirections.
  * Monitor `/var/log/syslog` or `/var/log/messages`.

---

### 3. **OpenWrt on Old Hardware**

* OpenWrt is lightweight and can run on old x86 PCs, but 2011 hardware may have quirks:

  * **BIOS/UEFI issues:** Some old boards struggle with PXE or modern Linux kernels.
  * **NIC support:** Make sure OpenWrt kernel has drivers for your Ethernet/Wi-Fi card.
  * **Minimal build:** Use `x86-generic` or `x86-64` images, remove unnecessary packages to save memory.

---

### 4. **Iptables Transparent Proxy Setup**

You already have a setup like:

```bash
iptables -t nat -A REDSOCKS -d <ip> -p tcp --dport <port> -j RETURN
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345
iptables -t nat -A PREROUTING -p tcp -j REDSOCKS
```

**Tips:**

* Test each rule separately to confirm it works as intended.
* Use `iptables -t nat -L -n -v` to see packet hits.
* Ensure no other chains (like `OUTPUT`) are also redirecting traffic unintentionally.

---

### 5. **DNS and Traffic Hijacking**

* `resolve.conf` and any DNS caches (like `dnsmasq` in OpenWrt) may hijack or redirect queries.
* To monitor:

  ```bash
  tcpdump -i any port 53 -vv
  ```

* Check if your DNS queries resolve correctly.

---

### 6. **Layered Analysis Approach**

1. **Interface layer:** Capture packets with `tcpdump`.
2. **Netfilter layer:** Log chain hits in `PREROUTING`, `OUTPUT`, `REDSOCKS`.
3. **Routing layer:** Verify `ip route` and `ip rule` entries.
4. **Application layer:** Enable proxy logs.
5. **DNS layer:** Confirm resolutions via `dig` or `nslookup`.

By correlating logs across layers, you can pinpoint where traffic diverges from expectations.

---

### 7. **Optional Tools**

* **Wireshark/TShark:** GUI or CLI packet inspection.
* **nethogs / iftop:** Monitor bandwidth per process.
* **strace/lsof:** Check which processes hold sockets.
* **iptraf-ng:** Real-time traffic stats per interface.

---

In short, your goal is to instrument every layer—from NICs, kernel, NAT, to proxy—to catch traffic at each handoff. This is the only way to systematically discover where hijacking occurs.

---

References:

* [OpenWrt x86 Installation Guide](https://openwrt.org/docs/guide-user/installation/x86)
* [Linux Netfilter/Iptables HOWTO](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
* [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html)
