---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debugging iPad USB Tethering Failure
translated: false
type: note
---

**Question:** Given the iPad USB tethering setup through a Linux laptop with Clash TUN proxy (DHCP working, NAT active, DNS configured), why is the iPad still unable to connect to the internet, and how do I systematically debug and fix it?

**Answer:**

Based on your setup summary, everything *looks* correct on paper — but there are several common failure points that are easy to miss. Here is a structured diagnostic approach from Layer 2 up to Layer 7.

---

## Step 1: Verify the Absolute Basics First

Run these on the **Linux laptop** to confirm the current live state (config on disk ≠ config in memory):

```bash
# 1. Is IP forwarding actually ON right now?
cat /proc/sys/net/ipv4/ip_forward
# Must return 1, not 0

# 2. What does iptables FORWARD chain look like?
sudo iptables -L FORWARD -v -n

# 3. Is the NAT MASQUERADE rule actually loaded?
sudo iptables -t nat -L POSTROUTING -v -n

# 4. Confirm interface names (may have changed!)
ip link show
# Note: your USB interface (enx00e04c362f89) and WAN interface names
```

If `ip_forward` is `0`, that alone kills everything — fix it immediately:

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

---

## Step 2: Check If Traffic Is Actually Being Forwarded

Use `tcpdump` to watch both interfaces simultaneously. Open **two terminals**:

```bash
# Terminal 1 — watch USB interface (traffic FROM iPad)
sudo tcpdump -i enx00e04c362f89 -n not arp

# Terminal 2 — watch WAN interface (traffic going OUT)
sudo tcpdump -i eth0 -n host 8.8.8.8
# (replace eth0 with your actual WAN interface)
```

Then from the iPad, try visiting any website. You should see:

- **Terminal 1:** packets from `192.168.201.136` arriving
- **Terminal 2:** those same packets appearing on the WAN side with the laptop's IP as source

If packets appear in Terminal 1 but **NOT** Terminal 2 → forwarding is broken (UFW/iptables issue).
If packets appear in **neither** → iPad is not sending traffic at all (check default gateway on iPad).

---

## Step 3: Verify iPad's Network Settings

On the iPad, go to **Settings → Wi-Fi** (or in this case the USB network). Check:

- **IP Address:** Should be `192.168.201.x`
- **Subnet Mask:** `255.255.255.0`
- **Router/Gateway:** Must be `192.168.201.1` ← **this is the most common failure point**
- **DNS:** Should be `192.168.201.1`

If the **Router field is blank or wrong**, the iPad doesn't know where to send traffic. This can happen if dnsmasq's DHCP is not sending the `option:router` correctly.

Verify dnsmasq config:

```bash
# Check dnsmasq is actually sending gateway option
grep -E "dhcp-option|gateway|router" /etc/dnsmasq.conf
# Should have something like:
# dhcp-option=3,192.168.201.1   ← gateway
# dhcp-option=6,192.168.201.1   ← DNS
```

**Force iPad to renew DHCP lease:** On iPad, toggle Airplane Mode ON → OFF, or go to the network settings and tap "Renew Lease".

---

## Step 4: Test With a Simple Bypass (Isolate Clash as the Problem)

To determine whether Clash TUN is the problem or the NAT/routing is the problem, **temporarily bypass Clash** with a direct NAT rule:

```bash
# Add a direct MASQUERADE bypassing Clash, using your WAN interface
sudo iptables -t nat -A POSTROUTING -s 192.168.201.0/24 -o <WAN_INTERFACE> -j MASQUERADE
sudo iptables -A FORWARD -i enx00e04c362f89 -o <WAN_INTERFACE> -j ACCEPT
sudo iptables -A FORWARD -i <WAN_INTERFACE> -o enx00e04c362f89 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Replace `<WAN_INTERFACE>` with your actual WAN interface (e.g., `eth0`, `wlan0`, `enp3s0`).

Now test on iPad: can you load `http://1.1.1.1`? (IP only, no DNS needed.)

- **If YES** → NAT/forwarding works; **Clash TUN is the problem**
- **If NO** → The issue is at the lower routing/forwarding layer

---

## Step 5: Fix Clash TUN-Specific Issues

If Clash is the bottleneck, check these:

### 5a. Confirm Clash TUN interface is up

```bash
ip link show | grep -i tun
# Should show a tun interface like "utun" or "Meta" etc.
ip addr show <tun_interface>
```

### 5b. Verify Clash is listening as DNS server

```bash
# Clash DNS should be listening on 192.168.201.1:53
sudo ss -ulnp | grep 53
# Or:
sudo netstat -ulnp | grep 53
```

### 5c. Test DNS manually from the laptop (simulating iPad)

```bash
# Query Clash DNS directly — should return fake-IP (198.18.x.x) for proxy domains
dig google.com @192.168.201.1

# If it returns a real IP instead of 198.18.x.x, fake-IP mode is not working
```

### 5d. Check Clash config for TUN auto-route

In your Clash `config.yaml`, the TUN section must have:

```yaml
tun:
  enable: true
  stack: system   # or "gvisor"
  auto-route: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
```

If `auto-route: true` is missing, Clash won't set up routes for forwarded traffic.

---

## Step 6: UFW Rule Order Problem (Very Common)

`sudo ufw default allow routed` sets the **default**, but UFW may have explicit DENY rules earlier in the chain that override it. Check:

```bash
sudo ufw status verbose
sudo iptables -L FORWARD -v -n --line-numbers
```

If you see any `DROP` or `REJECT` rules for your subnets, insert an explicit ACCEPT rule **before** them:

```bash
sudo iptables -I FORWARD 1 -i enx00e04c362f89 -j ACCEPT
sudo iptables -I FORWARD 2 -o enx00e04c362f89 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

---

## Step 7: Quick Full-Stack Test Sequence

Once you think it's fixed, run this sequence from iPad or by simulating from the laptop:

```bash
# From laptop, simulate iPad traffic using its IP:
# Test 1: Can we reach the gateway?
ping -I enx00e04c362f89 192.168.201.1

# Test 2: Can we reach a raw IP on the internet (no DNS needed)?
curl --interface enx00e04c362f89 http://1.1.1.1

# Test 3: DNS via Clash
nslookup google.com 192.168.201.1
# Should return 198.18.x.x (fake-IP) for proxy-destined domains

# Test 4: Full proxy path
curl --interface enx00e04c362f89 https://api.ipify.org
# Should return your proxy's exit IP
```

---

## Most Likely Root Cause Summary

Based on the history, the **most probable remaining issues** are one of:

| # | Likely Cause | How to Confirm |
|---|---|---|
| 1 | iPad didn't renew DHCP (still using old DNS/gateway) | Check iPad's network settings manually |
| 2 | Clash `auto-route: true` missing — TUN not capturing forwarded packets | Check Clash config |
| 3 | UFW has an explicit FORWARD DROP rule earlier in chain overriding `allow routed` | `sudo iptables -L FORWARD -n --line-numbers` |
| 4 | WAN interface name mismatch in MASQUERADE rule | `ip link show` to verify |
| 5 | `ip_forward` is 0 after reboot (not persisted in sysctl.conf) | `cat /proc/sys/net/ipv4/ip_forward` |

Start with Step 2 (tcpdump) — it will immediately tell you exactly where the packet is being lost, which eliminates half the possibilities at once.
