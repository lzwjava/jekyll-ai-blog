---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: How to Use the ARP Command
translated: false
type: note
---

Question: How to use the arp -a command?

Answer:

The `arp -a` command is used to display the contents of the ARP (Address Resolution Protocol) cache on your computer. The ARP cache is a table that maps IP addresses to physical (MAC) addresses of devices on your local network that your computer has recently communicated with. This is helpful for network troubleshooting, such as identifying devices, checking for duplicate IPs, or verifying MAC addresses.

### How to Use It

1. **Open a terminal or command prompt**:
   - On **Windows**: Search for "cmd" or "Command Prompt" (run as administrator for full access if needed).
   - On **Linux** or **macOS**: Open the Terminal.

2. **Run the command**:
   - Simply type `arp -a` and press Enter.

   Note: On Windows, the flag is `-a` (with a hyphen). On Linux/macOS, `-a` displays in an alternate (BSD-style) format, but it's commonly used and works the same way.

### Example Output

- **On Windows**:

  ```
  Interface: 192.168.1.100 --- 0x3
  Internet Address      Physical Address      Type
  192.168.1.1           aa-bb-cc-dd-ee-ff     dynamic
  192.168.1.10          11-22-33-44-55-66     dynamic
  ```

- **On Linux/macOS**:

  ```
  ? (192.168.1.1) at aa:bb:cc:dd:ee:ff [ether] on en0
  ? (192.168.1.10) at 11:22:33:44:55:66 [ether] on en0
  ```

### Explanation of Output

- **IP Address** (e.g., 192.168.1.1): The device's network address.
- **Physical/MAC Address**: The hardware address (unique identifier) of the device's network interface.
- **Type**: Usually "dynamic" (learned automatically) or "static" (manually added).
- **Interface**: The network adapter (e.g., Wi-Fi or Ethernet) on your computer.

### Additional Options

- To view entries for a specific IP: `arp -a <IP-address>` (Windows) or specify hostname on Unix-like systems.
- To view for a specific interface: Use `-N <interface-IP>` on Windows.

### Tips

- The cache is temporary and updates automatically.
- If the cache is empty, try pinging devices on your network first (e.g., `ping 192.168.1.1`) to populate it.
- For more details, run `arp /?` (Windows) or `man arp` (Linux/macOS).

This command works on Windows, Linux, and macOS with minor differences in syntax and output format.

References:

- [Microsoft Learn: arp command](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/arp)
- [GeeksforGeeks: arp command in Linux](https://www.geeksforgeeks.org/linux-unix/arp-command-in-linux-with-examples/)
- [Meridian Outpost: ARP Tutorial](https://www.meridianoutpost.com/resources/articles/command-line/arp.php)
