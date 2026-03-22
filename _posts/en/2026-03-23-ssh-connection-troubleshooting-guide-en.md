---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Connection Troubleshooting Methodology Guide
translated: false
type: note
---

I'll create a diagnostic guide showing the step-by-step methodology I used to identify the root cause.

## SSH Connection Troubleshooting Methodology

Here's the systematic approach I used to diagnose your SSH issue:

### Step 1: Check Proxy Configuration

**Command:**
```bash
env | grep -i proxy
```

**What it reveals:**
- All proxy-related environment variables
- Whether HTTP_PROXY, HTTPS_PROXY, ALL_PROXY are set
- What NO_PROXY excludes

**Your results:**
```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=http://127.0.0.1:7890
NO_PROXY=localhost,127.0.0.1,.example.com,::1
```

**Interpretation:** Proxy is active, but NO_PROXY doesn't include 192.168.* ranges (initial suspicion).

---

### Step 2: Verify Proxy Service is Running

**Command:**
```bash
lsof -i :7890
```

**What it reveals:**
- Whether anything is listening on the proxy port
- What process owns the proxy connection

**Your results:**
```
node       1870 lzwjava   19u  IPv4 ... TCP localhost:55717->localhost:7890 (ESTABLISHED)
AMPLibrar  2729 lzwjava   13u  IPv4 ... TCP localhost:55704->localhost:7890 (ESTABLISHED)
```

**Interpretation:** Proxy service is definitely running and accepting connections.

---

### Step 3: Test Basic Network Connectivity

**Command:**
```bash
ping -c 3 192.168.2.1
```

**What it reveals:**
- Whether the host is reachable at the network layer (ICMP)
- Round-trip time and packet loss

**Your results:**
```
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 6.923/7.855/9.023/0.874 ms
```

**Interpretation:** Network connectivity exists, but ICMP ≠ TCP (ping uses different protocol).

---

### Step 4: Test SSH Without Proxy Variables

**Command:**
```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY ssh -o ConnectTimeout=5 root@192.168.2.1 exit
```

**What it reveals:**
- Whether removing proxy variables fixes the issue
- If the problem is proxy-related or something else

**Your results:**
```
ssh: connect to host 192.168.2.1 port 22: Operation timed out
```

**Interpretation:** ⚠️ **Critical finding** - SSH still fails without proxy! This disproves the proxy theory.

---

### Step 5: Check SSH Configuration

**Command:**
```bash
cat ~/.ssh/config
```

**What it reveals:**
- Whether SSH has proxy commands configured
- Host-specific connection rules

**Your results:**
```
Host !192.168.*.*
    ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

**Interpretation:** The `!` negation means "use proxy for everything EXCEPT 192.168.*.*" - so 192.168.2.1 should NOT use the proxy anyway.

---

### Step 6: Test Port 22 Directly

**Command:**
```bash
nc -zv -w 3 192.168.2.1 22
```

**What it reveals:**
- Whether port 22 is open and accepting connections
- Bypasses SSH entirely to test raw TCP connectivity

**Your results:**
```
192.168.2.1 22 (ssh): Operation timed out
```

**Interpretation:** Port 22 is not reachable - this is a network/firewall issue, not SSH or proxy.

---

### Step 7: Check Local Network Configuration

**Command:**
```bash
ifconfig | grep -A 2 "inet 192.168"
```

**What it reveals:**
- What subnet your Mac is on
- Your local IP address

**Your results:**
```
inet 192.168.1.37 netmask 0xffffff00 broadcast 192.168.1.255
```

**Interpretation:** You're on 192.168.1.0/24, but the router is on 192.168.2.0/24 - **different subnets!**

---

### Step 8: Check ARP Table

**Command:**
```bash
arp -n 192.168.2.1
```

**What it reveals:**
- Whether your Mac has communicated directly with the router at Layer 2
- If the router is on the same physical network segment

**Your results:**
```
192.168.2.1 (192.168.2.1) -- no entry
```

**Interpretation:** No ARP entry = no direct Layer 2 communication = router is not on the same network segment.

---

### Step 9: Check Routing Table

**Command:**
```bash
route -n get 192.168.2.1
```

**What it reveals:**
- How your Mac routes traffic to 192.168.2.1
- What gateway it uses

**Your results:**
```
route to: 192.168.2.1
destination: 192.168.2.1
    gateway: 192.168.1.1
  interface: en0
```

**Interpretation:** Traffic to 192.168.2.1 goes through gateway 192.168.1.1, not directly.

---

## Diagnostic Decision Tree

```
SSH to 192.168.2.1 fails
│
├─ Check proxy env vars → Set to 127.0.0.1:7890
│  └─ Hypothesis: Proxy is blocking SSH
│     │
│     ├─ Test SSH without proxy → Still fails ❌
│     │  └─ Proxy theory disproven
│     │
│     └─ Check SSH config → Proxy excluded for 192.168.*.*
│        └─ Confirms proxy is not the issue
│
├─ Test port 22 with netcat → Times out
│  └─ Port 22 is unreachable (not just SSH)
│
├─ Check local network → 192.168.1.37/24
│  └─ Different subnet than router (192.168.2.1)
│
├─ Check ARP table → No entry
│  └─ No direct Layer 2 connectivity
│
└─ Check routing → Goes through gateway 192.168.1.1
   └─ **Conclusion: Network segmentation issue**
      - Ping works (ICMP routed through gateway)
      - SSH blocked (firewall/routing rule on gateway)
```

---

## Key Diagnostic Principles

1. **Test at each layer:**
   - Layer 3 (Network): `ping`
   - Layer 4 (Transport): `nc -zv`
   - Layer 7 (Application): `ssh`

2. **Isolate variables:**
   - Remove proxy vars to test if proxy is the issue
   - Use `nc` to bypass SSH and test raw TCP

3. **Check configuration:**
   - Environment variables (`env`)
   - SSH config (`~/.ssh/config`)
   - Network interfaces (`ifconfig`)

4. **Verify assumptions:**
   - "Ping works" doesn't mean SSH will work
   - Same IP range (192.168.*) doesn't mean same subnet

5. **Look for evidence:**
   - ARP table shows Layer 2 connectivity
   - Routing table shows how traffic flows
   - `lsof` shows what's actually listening

---

## The Smoking Gun

The combination of:
- ✅ Ping works (ICMP routed)
- ❌ SSH fails even without proxy
- ❌ Port 22 unreachable via netcat
- ❌ No ARP entry
- ⚠️ Different subnets (192.168.1.x vs 192.168.2.x)
- ⚠️ Traffic routed through gateway

**Proves:** This is a network segmentation/firewall issue, not a proxy issue.