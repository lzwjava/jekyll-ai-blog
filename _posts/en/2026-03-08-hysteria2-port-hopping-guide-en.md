---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hysteria2 Port Hopping Setup Guide
translated: false
type: note
---

**Question:** How do you enable and configure Port Hopping in Hysteria2 to avoid UDP throttling and GFW blocking?

**Answer:**

## Hysteria2 Port Hopping — Complete Setup Guide

Port hopping is a powerful anti-censorship feature. Users in China sometimes report that their ISPs block or throttle persistent UDP connections, but these restrictions often only apply to the specific port being used. Port hopping works as a workaround by having the client randomly select one of the specified ports for the initial connection and periodically switch to a different port.

---

## How It Works (Architecture)

The Hysteria server does not have built-in support for listening on multiple ports, so you cannot use a multi-port format as the listening address on the server side. The recommended approach is to use iptables DNAT to redirect ports to the server's listening port.

So the setup has two parts:

- **Server side:** iptables DNAT rules to forward a port range → one real port
- **Client side:** multi-port address format + `hopInterval` config

---

## Step 1 — Server Side: Configure iptables DNAT

The server itself listens on a **single port** (e.g., `5353` or `443`). You use iptables to forward a wide port range to that port.

**Install iptables-persistent (to survive reboots):**

```bash
apt install iptables-persistent -y
```

**Add DNAT rules to forward UDP ports 20000–50000 → port 5353:**

```bash
# IPv4
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j DNAT --to-destination :5353

# IPv6
ip6tables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j DNAT --to-destination :5353
```

**Save rules permanently:**

```bash
sudo iptables-save > /etc/iptables/rules.v4
sudo ip6tables-save > /etc/iptables/rules.v6
sudo systemctl enable netfilter-persistent
sudo systemctl start netfilter-persistent
```

> You can use any port range (e.g., 20000–40000). Just make sure your VPS firewall/security group also allows UDP traffic on that range.

---

## Step 2 — Server Config (`/etc/hysteria/config.yaml`)

The server config remains simple — it listens on only **one port**:

```yaml
listen: :5353   # Single listening port

tls:
  cert: /etc/hysteria/server.crt
  key:  /etc/hysteria/server.key

auth:
  type: password
  password: YOUR_STRONG_PASSWORD

masquerade:
  type: proxy
  proxy:
    url: https://bing.com
    rewriteHost: true
```

---

## Step 3 — Client Side: Multi-Port Address Format

The Hysteria client supports a special multi-port address format. You can specify multiple individual ports, a range of ports, or a combination of both. There is no limit to the number of ports you can specify.

Examples:

```
example.com:1234,5678,9012          # Multiple individual ports
example.com:20000-50000             # A port range
example.com:1234,5000-6000,8000-9000  # Combination
```

---

## Step 4 — Client Config: Set `hopInterval`

The `hopInterval` option in the transport section controls the port hopping interval. This is only relevant if you're using a port hopping address.

```yaml
server: example.com:20000-50000   # Port hopping range

auth: YOUR_STRONG_PASSWORD

tls:
  sni: example.com
  insecure: false

transport:
  type: udp
  udp:
    hopInterval: 30s   # Switch to a new port every 30 seconds

socks5:
  listen: 127.0.0.1:1080

http:
  listen: 127.0.0.1:8080
```

> Recommended `hopInterval` values: `10s` to `60s`. Shorter intervals give stronger anti-fingerprinting but slightly more overhead.

---

## How the Hopping Works (Traffic Flow)

```
Client → random port in 20000-50000
         ↓ (iptables DNAT on server)
         → server port 5353
         ↓ (every hopInterval seconds)
Client hops to a different port in range → still maps to :5353
```

Assuming the server is reachable on all the ports you specified, the hopping process is transparent to the upper layers and should not cause any data loss or disconnection.

---

## Tips & Notes

| Item | Detail |
|------|--------|
| Port range size | Larger is better (e.g., 20000–50000) for anti-fingerprinting |
| Firewall | Open UDP for the entire range in your VPS provider's security group |
| hopInterval | `30s` is a good default; lower = harder to track, more overhead |
| IPv6 | Always add ip6tables rules alongside iptables rules |
| Reboot persistence | Required — use `netfilter-persistent` or equivalent |

---

**References:**

- [Hysteria2 Official Port Hopping Docs](https://v2.hysteria.network/docs/advanced/Port-Hopping/)
- [Hysteria2 Full Client Config](https://v2.hysteria.network/docs/advanced/Full-Client-Config/)
- [Hysteria2 Full Server Config](https://v2.hysteria.network/docs/advanced/Full-Server-Config/)
- [Geek Blog: Counter QoS Blocking with Hysteria2 Port Hopping](https://geekbb.xlog.app/dui-kang-QoS-zu-duan--xian-su-Hysteria2-duan-kou-tiao-yue-she-zhi)
- [SQYBI: Solving Hysteria2 Port Hopping on OpenWrt](https://sqybi.com/en-US/blog/solving-the-issue-openwrt-homeproxy-hysteria2-port-hopping/)
