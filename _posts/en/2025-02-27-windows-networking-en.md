---
audio: false
generated: true
lang: en
layout: post
title: Windows Networking Commands
translated: false
type: note
---

Let’s dive into some useful Windows networking commands you can run in the Command Prompt (CMD) to troubleshoot, gather info, or manage your network. I’ll explain a few popular ones like `getmac`, and throw in some others that might come in handy. You don’t need to be a tech wizard—these are pretty straightforward once you get the hang of them.

First, to use these commands, open Command Prompt: press `Windows Key + R`, type `cmd`, and hit Enter. Easy enough, right?

### 1. `getmac` - Find Your MAC Address
The `getmac` command shows the Media Access Control (MAC) address of your network adapters—those unique identifiers for your device on a network. Here’s how it works:

- Type `getmac` and press Enter.
- You’ll see a list of MAC addresses for each network adapter (like Ethernet or Wi-Fi).
- Add the `-v` switch (`getmac -v`) for verbose mode, which gives extra details like the adapter name and transport type (e.g., Ethernet or Wireless).

Example output might look like:
```
Physical Address    Transport Name
=================== ==========================================================
00-14-22-01-23-45   \Device\Tcpip_{12345678-ABCD-1234-EF56-7890ABCDEF12}
```
The “Physical Address” is your MAC. Useful for network troubleshooting or setting up MAC filtering on a router.

### 2. `ipconfig` - Check Your IP Configuration
This is a go-to command for network info:
- Type `ipconfig` and hit Enter to see basic details like your IP address, subnet mask, and default gateway.
- Use `ipconfig /all` for a full breakdown, including DNS servers, DHCP status, and—yep—your MAC address again.

It’s great for figuring out if your device is properly connected or if there’s an IP conflict.

### 3. `ping` - Test Connectivity
Want to check if you can reach another device or website?
- Type `ping [address]` (e.g., `ping google.com` or `ping 8.8.8.8`).
- It sends a few packets and tells you if they come back, plus how long it takes (in milliseconds).

If you get “Request timed out,” something’s blocking the connection—could be a firewall, a dead server, or your own network.

### 4. `tracert` - Trace the Route
Short for "trace route," this shows the path your data takes to a destination:
- Type `tracert [address]` (e.g., `tracert google.com`).
- It lists each hop (router or server) along the way, with response times.

Handy for spotting where a connection slows down or fails.

### 5. `netstat` - See Network Activity
This one’s for checking what’s happening on your network right now:
- Type `netstat -a` to see all active connections and listening ports.
- Add `-n` (`netstat -an`) to show IP addresses instead of hostnames—faster and more raw.

It’s like a window into what your computer’s talking to—useful for spotting suspicious activity.

### 6. `nslookup` - Dig Into DNS
If websites aren’t loading, this checks Domain Name System (DNS) resolution:
- Type `nslookup [domain]` (e.g., `nslookup google.com`).
- It returns the IP address tied to that domain, showing if your DNS is working.

### Tips to Make It Smoother
- Run CMD as Administrator (right-click Command Prompt > “Run as administrator”) if a command needs higher privileges.
- Combine commands with `|` (pipe) for filtering—e.g., `getmac | find "00-14"` to search for a specific MAC.
- If you’re stuck, type `[command] /?` (e.g., `ipconfig /?`) for help on that command.

These are your bread-and-butter tools for poking around a Windows network. Want to focus on one—like `getmac`—or try something specific? Let me know what you’re aiming for!
