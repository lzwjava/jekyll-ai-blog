---
audio: false
generated: false
image: false
lang: en
layout: post
title: Cloud IPs, Network Interface and WiFi Optimization
translated: false
type: post
---

### Table of Contents

1. [Floating IPs in Hetzner Cloud](#floating-ips-in-hetzner-cloud)
   - IP Configuration Commands
   - Netplan Configuration Setup
   - Network Configuration Files

2. [Network Interface Management](#network-interface-management)
   - Deleting TUN Interfaces
   - Interface Status Monitoring
   - Network Troubleshooting

3. [LAN IP Scanner](#lan-ip-scanner)
   - Python Network Scanning Script
   - Multithreaded Host Discovery
   - Port Scanning Capabilities
   - Device Identification on Local Networks

4. [Bypassing Local IPs](#bypassing-local-ips)
   - Proxy Configuration for Local Networks
   - Subnet Mask Calculations
   - Network Range Planning

5. [SSH Connection using IPv6 Address](#ssh-connection-using-ipv6-address)
   - IPv6 SSH Configuration
   - SSH Config File Management
   - Proxy Command Setup for Different Address Types
   - Performance Optimization

6. [Improving Wifi Speed](#improving-wifi-speed)
   - Old vs New Modem Performance
   - Network Setup Configurations
   - Wired vs Wireless Bridge Modes
   - Troubleshooting Network Bottlenecks

7. [OpenWrt Reset](#openwrt-reset)
   - Web Interface Reset Methods
   - Command Line Reset Procedures
   - Factory Default Restoration

## Floating IPs in Hetzner Cloud

### IP

```bash
sudo ip addr add 78.47.144.0 dev eth0
```

### Netplan

```bash
touch /etc/netplan/60-floating-ip.yaml
nano /etc/netplan/60-floating-ip.yaml
```

```yaml
network:
   version: 2
   renderer: networkd
   ethernets:
     eth0:
       addresses:
       - 78.47.144.0/32
```

```bash
sudo netplan apply
```

---

## Network Interface Management

Delete the `tun` interface.

```bash

$ ipconfig

outline-tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.0.85.1  netmask 255.255.255.255  destination 10.0.85.1
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 208  bytes 8712 (8.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 385  bytes 23322 (23.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ sudo ip link delete outline-tun0

```

---

## LAN IP Scanner

This Python script scans a local network for active IP addresses. It uses the `ping` command to check if a host is reachable and employs multithreading to speed up the scanning process.  A semaphore limits the number of concurrent threads to avoid overwhelming the system. The script takes a network address (e.g., "192.168.1.0/24") as input and prints whether each IP address in the network is up or down.

This script helps identify devices on the network, such as a TP-LINK mesh router operating in wired bridge mode, by scanning for active IP addresses.

```python
import subprocess
import ipaddress
import threading
import os
import socket
import argparse

MAX_THREADS = 50  # Maximum number of threads to use

def is_host_up(host, port=None):
    """
    Checks if a host is up using ping or telnet.
    If port is specified, uses telnet to check if the port is open.
    Otherwise, uses ping.
    Returns True if the host is up, False otherwise.
    """
    if port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
            else:
                return False
        except socket.error as e:
            return False
        finally:
            sock.close()
    else:
        try:
            # -c 1: Send only 1 packet
            # -W 1: Wait 1 second for a response
            subprocess.check_output(["ping", "-c", "1", "-W", "1", host], timeout=1)
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            return False

def scan_ip(ip_str, up_ips, port=None):
    """
    Scans a single IP address and prints its status.
    """
    if is_host_up(ip_str, port):
        print(f"{ip_str} is up")
        up_ips.append(ip_str)
    else:
        print(f"{ip_str} is down")

def scan_network(network, port=None):
    """
    Scans a network for live hosts using threads, limiting the number of concurrent threads.
    """
    print(f"Scanning network: {network}")
    threads = []
    semaphore = threading.Semaphore(MAX_THREADS)  # Limit the number of concurrent threads
    up_ips = []

    def scan_ip_with_semaphore(ip_str):
        semaphore.acquire()
        try:
            scan_ip(ip_str, up_ips, port)
        finally:
            semaphore.release()

    for ip in ipaddress.IPv4Network(network):
        ip_str = str(ip)
        thread = threading.Thread(target=scan_ip_with_semaphore, args=(ip_str,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return up_ips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan a network for live hosts.")
    parser.add_argument("network", nargs='?', default="192.168.1.0/24", help="The network to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--port", type=int, help="The port to check (optional)")
    args = parser.parse_args()

    network_to_scan = args.network
    port_to_scan = args.port

    up_ips = scan_network(network_to_scan, port_to_scan)
    print("\nLive IPs:")
    for ip in up_ips:
        print(ip)


```

## Bypassing Local IPs

The script identifies active IP addresses. To ensure proper network communication, verify that proxy settings are configured to bypass these local IPs.

```bash
192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,127.0.0.1,localhost,*.local,timestamp.apple.com,sequoia.apple.com,seed-sequoia.siri.apple.com, 192.168.1.0/16
```

## Subnet Masks

My second machine is usually at 192.168.1.16.

So it works using the command below.

```bash
python scripts/ip_scan.py 192.168.1.0/27 -p 22
```

because 32 - 27 = 5, 2^5 = 32, so it will try `192.168.1.0` to `192.168.1.31`.

But it doesn't work when using `192.168.1.0/28`, because 2^4 = 16, so it will try `192.168.1.0` to `192.168.1.15`, which doesn't cover `192.168.1.16`.

---

## SSH connection using IPv6 address

I'm trying to connect to a machine in Hetzner Cloud using IPv6. `ssh 2a01:4f8:c17:2000::/64` doesn't work, but `ssh root@2a01:4f8:c17:2000::1` does.

The IPv6 address was copied from the Hetzner Cloud console.

The `~/.ssh/config` file can be configured to apply different proxy rules for IPv4 and IPv6 addresses. This setup allows you to specify a proxy command for IPv4 addresses while handling IPv6 addresses differently.

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host *.*.*.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
```

When running `ssh root@192.168.1.3`, the following output shows the SSH client applying configuration options from the `~/.ssh/config` file:

```bash
debug1: Reading configuration data /Users/lzwjava/.ssh/config
debug1: /Users/lzwjava/.ssh/config line 1: Applying options for 192.168.1.*
debug1: /Users/lzwjava/.ssh/config line 5: Applying options for *.*.*.*
debug2: add_identity_file: ignoring duplicate key ~/.ssh/id_rsa
debug1: /Users/lzwjava/.ssh/config line 10: Applying options for *
debug2: add_identity_file: ignoring duplicate key ~/.ssh/id_rsa
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug2: resolve_canonicalize: hostname 192.168.1.3 is address
debug3: expanded UserKnownHostsFile '~/.ssh/known_hosts' -> '/Users/lzwjava/.ssh/known_hosts'
debug3: expanded UserKnownHostsFile '~/.ssh/known_hosts2' -> '/Users/lzwjava/.ssh/known_hosts2'
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug3: channel_clear_timeouts: clearing
debug1: Executing proxy command: exec corkscrew localhost 7890 192.168.1.3 22
```

The SSH connection speed was noticeably slow, so I reverted to the following simpler configuration:

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
```

The issue arises when using IPv6 addresses with the `ProxyCommand corkscrew localhost 7890 %h %p` directive, as this proxy command may not handle IPv6 addresses correctly.

The configuration above is still not working. However, the one below is fine.

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host !192.*.*.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
```

---

## Improving Wifi Speed

### Old Modem Issues

In my parent's house, the modem is quite old, likely around 10 years old. The initial network setup was:

modem -> 3m wireless -> TP-Link AX3000 (wireless bridge mode) -> 2m, a wall, wireless -> Laptop

This resulted in a low download speed, with a Speedtest result of only 10 Mbps.

An improved setup involved using a wired connection:

modem -> 2m cable -> TP-Link AX3000 (wired bridge mode) -> 4m wireless, a wall -> Laptop

This improved the download speed to up to 90 Mbps.

### New Modem Performance

In my own house, the modem is new, and the TP-Link router performs well in wireless bridge mode. The network setup is:

modem -> 4m wireless -> TP-Link AX3000 (wireless bridge mode) -> 2m wireless -> Laptop

The network quality is good.

### Troubleshooting Tips

There isn't a single solution to improve Wi-Fi speed. A good approach is to use a cable to test each part of your network to identify bottlenecks. Compare speeds when using a wired connection versus Wi-Fi. Also, try connecting devices directly with a cable to see if that improves performance.

---

## OpenWrt Reset

### Resetting via the Web Interface

It's recommended to connect to the router via an ethernet cable. After a reset, the Wi-Fi SSID will revert to its default settings, which may not be what you expect.

### Resetting via Command Line (SSH)

You can reset OpenWrt to its default settings using the command line interface (SSH). Here's how:

1. Connect to your OpenWrt router via SSH.
2. Run the following command:

    ```bash
    root@OpenWrt:~# firstboot
    This will erase all settings and remove any installed packages. Are you sure? [N/y]
    y
    /dev/ubi0_1 is mounted as /overlay, only erasing files
    root@OpenWrt:~# reboot
    ```

3. The router will reboot with default settings.

**Explanation of the commands:**

- `firstboot`: This command initiates the reset process, erasing all configurations and installed packages.
- `reboot`: This command restarts the router, applying the reset.
