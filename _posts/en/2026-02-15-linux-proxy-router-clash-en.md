---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Proxy Router With Clash Setup
translated: false
type: note
---

Question: Could I use one Ethernet port for internet input and a USB-to-Ethernet adapter for output to run a Clash service as a global proxy router in a home network setup on a Linux Mint laptop (likely an old ThinkPad from ~2010–2012)?

Answer: 

Yes, this is possible and is a quite common way to turn an old laptop into a simple wired proxy router using Clash.

### Typical working setup (most reliable method)

1. **Network interfaces**
   - eth0 (built-in Ethernet) → connect to your main modem/router (gets real internet)
   - eth1 (USB → Ethernet adapter) → connect to a switch or directly to other devices that should go through the proxy

2. **Basic traffic flow you want**
   ```
   Modem ── eth0 ── [Linux Mint laptop with Clash] ── eth1 ── your devices / switch
   ```

3. **What you need to configure on Linux Mint**

   **A. Enable IP forwarding**
   ```bash
   sudo sysctl -w net.ipv4.ip_forward=1
   # make permanent
   echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
   sudo sysctl -p
   ```

   **B. NAT / Masquerade outbound traffic (so clients can reach the internet through your laptop)**
   ```bash
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   # or using nftables (newer Mint versions)
   sudo nft add rule ip nat postrouting oifname "eth0" masquerade
   ```

   **C. Make sure the USB-Ethernet gets an IP in a different subnet**
   Two common approaches:

   **Option 1 – Simple static IP (recommended for beginners)**
   ```bash
   sudo nmcli con mod "Wired connection 2" ipv4.method manual ipv4.addresses 192.168.201.1/24 ipv4.gateway "" ipv4.dns ""
   sudo nmcli con up "Wired connection 2"
   ```
   (check connection name with `nmcli connection show`)

   **Option 2 – Install & run a tiny DHCP server on eth1**
   Most popular & easy on Mint/Ubuntu: `dnsmasq`
   ```bash
   sudo apt update
   sudo apt install dnsmasq
   ```
   Minimal config `/etc/dnsmasq.d/custom.conf`:
   ```
   interface=eth1
   dhcp-range=192.168.201.50,192.168.201.150,12h
   dhcp-option=3,192.168.201.1      # gateway = laptop itself
   dhcp-option=6,192.168.201.1      # DNS = laptop (will forward later)
   ```
   Then `sudo systemctl restart dnsmasq`

   **D. Route all client traffic through Clash**
   Most Clash implementations (Clash for Linux, Clash Meta / Mihomo, Clash Verge CLI, etc.) support two main modes:

   - **TUN mode** (preferred for full transparent proxy)
     - Start Clash with TUN enabled (`allow-lan: true`, `tun: enable`)
     - Make sure Clash creates the `utun` / `clash0` interface
     - Add policy routing so traffic coming from eth1 goes into Clash:
       ```bash
       ip rule add from 192.168.201.0/24 table 100
       ip route add default via 192.168.201.1 dev eth1 table 100
       # or simpler – many Clash packages do this automatically in TUN mode
       ```

   - **Redirect / TProxy mode** (iptables/nftables redirect)
     - Use Clash built-in redir-host or fake-ip + iptables REDIRECT or TPROXY rules
     - Most user-friendly way: many Clash Meta / Mihomo packages for Linux include helper scripts for this

   **E. Make clients use your laptop as gateway**
   - Connect devices to the eth1 network
   - They should get IP via DHCP (if you run dnsmasq)
   - Or manually set gateway = 192.168.201.1 and DNS = 192.168.201.1 (or 8.8.8.8 if you prefer)

### Quick summary – most stable combo in 2025/2026 on old hardware

- Clash Meta core (mihomo) or Clash Verge service in **TUN mode**
- Built-in eth0 = WAN (gets internet via DHCP from modem)
- USB-Ethernet = LAN (static 192.168.201.1/24 or dnsmasq)
- IP forwarding + simple masquerade on eth0
- Clients point gateway to laptop IP on 192.168.201.x subnet

### Things to watch out for on old ThinkPad + Linux Mint

- Very old kernel sometimes has poor USB-Ethernet driver stability → try different USB-Ethernet chip (AX88179, RTL8153 are usually best supported)
- Old hardware may struggle with very high throughput through Clash + encryption
- Use lightweight Clash core and avoid memory-hungry Clash Meta plugins if RAM ≤ 4 GB

This setup works well as a small home global proxy router.

References:  

- None required for this explanation (common Linux networking + Clash knowledge)