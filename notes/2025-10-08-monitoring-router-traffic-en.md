---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Monitoring Router Network Traffic
translated: false
type: note
---

### Monitoring HTTP Requests and TCP Connections on 360 Wi-Fi 6 Router T7

The 360 T7 runs a customized Linux-based firmware (not fully OpenWrt out of the box), so monitoring capabilities are limited in the stock setup compared to a full Linux shell. With admin rights (via web UI), you can access basic logs. For deeper "hacking" like real-time HTTP request logging or TCP connection tracking, the best ethical approach is flashing OpenWrt (which is officially supported), enabling SSH, and using standard Linux tools. **Warning: Flashing custom firmware voids warranty and risks bricking—backup first and follow guides carefully. Only do this on your own device.**

#### 1. **Accessing Admin Rights on Stock Firmware**
   - Connect to the router's Wi-Fi or via Ethernet.
   - Open a browser and go to `http://ihome.360.cn` or `http://192.168.0.1` (default IP).
   - Login: Default username `admin`, password printed on the router label (often `admin` or a unique string like `360XXXXXX`—check the bottom sticker).
   - Once in, navigate to **System > Log** or **Security > Log** for basic system and traffic logs. This shows firewall blocks, connections, and some HTTP activity (e.g., blocked sites or intrusions), but not full HTTP request details.

   **Basic Monitoring via Web UI:**
   - **System Logs**: View recent events, including TCP connection attempts and errors. Export logs (may require the label password for decryption).
   - **Traffic Stats**: Under **Status > Network** or **Advanced > Traffic Monitor**, see bandwidth usage per device/IP, but not granular HTTP/TCP.
   - Limitations: No real-time HTTP payload inspection; logs are high-level and not exportable without auth.

#### 2. **Advanced Monitoring: Flash OpenWrt for Shell Access**
   The 360 T7 (MT7981B chipset) is supported in OpenWrt 23.05+ snapshots. Flashing gives full root shell access via SSH, where you can run tools like `tcpdump` for packet captures and `logread` for logs.

   **Steps to Flash OpenWrt (High-Level; Use Official Guide):**
   1. Download the factory image from OpenWrt downloads (search for "Qihoo 360T7 sysupgrade.bin" or factory image).
   2. Backup stock firmware: In web UI, go to **System > Backup** and download config/firmware.
   3. Upload via web UI: **System > Firmware Upgrade**, select the .bin file, and apply (router reboots into OpenWrt).
   4. Post-flash: Access web UI at `http://192.168.1.1` (LuCI interface), username `root`, no password initially—set one immediately via SSH or UI.
   5. Enable SSH: It's on by default on port 22. Connect from your PC: `ssh root@192.168.1.1` (use PuTTY on Windows).

   **Risk Mitigation**: If stuck, use TFTP recovery (hold reset during boot) or serial console (requires UART adapter).

#### 3. **Monitoring on OpenWrt (via SSH Shell)**
   Once SSH'd in as root, the router acts like a minimal Linux system. Install packages if needed via `opkg update && opkg install tcpdump` (built-in storage is 128MB, so keep it light).

   - **List All Current TCP Connections (Static View):**
     ```
     ss -tunap
     ```
     - Shows established/listening TCP sockets, ports, processes (e.g., `tcp ESTAB 0 0 192.168.1.1:80 192.168.1.100:54321 users:(("uhttpd",pid=1234,fd=3))`).
     - For real-time: `watch -n 1 'ss -tunap'`.

   - **Real-Time TCP Traffic Capture:**
     Install if needed: `opkg update && opkg install tcpdump`.
     ```
     tcpdump -i any tcp -n -v
     ```
     - `-i any`: All interfaces (br-lan for LAN, eth0.2 for WAN).
     - Filter HTTP: `tcpdump -i any tcp port 80 -n -v -A` (`-A` shows ASCII payload for HTTP headers/requests).
     - Save to file: `tcpdump -i any tcp -w /tmp/capture.pcap` (download via SCP: `scp root@192.168.1.1:/tmp/capture.pcap .`).
     - For HTTPS (port 443), note payloads are encrypted—use Wireshark offline for analysis.

   - **Monitor HTTP Request Logs:**
     - System logs (includes web server if using uhttpd): `logread | grep uhttpd` or `logread -f` for real-time.
     - Enable detailed HTTP logging: Edit `/etc/config/uhttpd` (web server config), add `option log_file '/var/log/uhttpd.log'`, then `/etc/init.d/uhttpd restart`. Tail: `tail -f /var/log/uhttpd.log` (shows GET/POST requests, IPs, URLs).
     - For full network HTTP: Use `tcpdump` as above, or install `ngrep` (`opkg install ngrep`): `ngrep -d any 'GET|POST|HTTP' -O /tmp/http.pcap`.

   - **Firewall/Connection Logs:**
     - Enable logging on rules: `uci set firewall.@rule[0].log='1'; uci commit; /etc/init.d/firewall restart`.
     - View: `logread | grep fw` (shows dropped/accepted TCP connections).

#### Tips for Ethical "Hacking"
- **Security**: After setup, change root password (`passwd`), disable password auth in `/etc/ssh/sshd_config` for key-only, and firewall SSH to LAN only.
- **Performance**: T7 has 256MB RAM—avoid heavy captures long-term to prevent OOM.
- **Revert to Stock**: Download official firmware from 360's site, upload via OpenWrt's sysupgrade (with `--force` if needed).
- Test in a safe environment; for GUI analysis, SCP .pcap to PC and open in Wireshark.

This gives comprehensive visibility. If stock UI suffices for basics, stick there to avoid flashing.

[OpenWrt Techdata: Qihoo 360T7](https://openwrt.org/toh/hwdata/qihoohardware/qihoohardware_360t7)
[360 T7U Manual (Logs Section)](https://ipc-pr-cdn.jia.360.cn/ipc-pr/luyouqiT7U.pdf)
[OpenWrt Logging Guide](https://openwrt.org/docs/guide-user/base-system/log.essentials)
[360 Forum: Log Export](https://bbs.360.cn/forum-7007-1.html)
