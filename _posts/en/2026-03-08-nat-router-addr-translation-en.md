---
audio: false
generated: true
image: false
lang: en
layout: post
title: NAT Router Address Translation Process
translated: false
type: note
---

Question: In the diagram (Figure 32), Host A on a private network sends datagrams to Host B on the Internet. Please analyze why a NAT router is used, and identify the IP addresses at positions ①, ②, ③, and ④.

Answer:

## Why a NAT Router is Used

### Reason 1: Private IP Addresses Cannot Route on the Public Internet

Host A uses the private IP address **192.168.0.3**, which belongs to the `192.168.0.0/24` private address range. Private addresses (defined by RFC 1918) are:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

These addresses are **not routable on the public Internet** — routers on the Internet will drop packets with private source addresses.

### Reason 2: Address Translation is Necessary for External Communication

For Host A to communicate with Host B (213.18.2.4) on the Internet, its private address must be **translated into a globally routable public IP address**. This process is called **Network Address Translation (NAT)**.

### Reason 3: NAT Router Performs the Translation

The NAT router sits at the boundary between the private network and the Internet. It:

- Replaces the **private source address** with its own **public (global) IP address** (172.38.1.5) when forwarding packets outbound
- Reverses the translation for inbound reply packets, forwarding them back to Host A

---

## IP Addresses at Each Position

| Position | Direction | Field | IP Address | Explanation |
|----------|-----------|-------|------------|-------------|
| ① | Outgoing (inside private net) | Source IP | **192.168.0.3** | Host A's private address is the source |
| ② | Return (inside private net) | Destination IP | **192.168.0.3** | Reply packet must be delivered back to Host A |
| ③ | Outgoing (toward Internet) | Source IP | **172.38.1.5** | NAT router replaces private source with its public IP |
| ④ | Return (toward Internet) | Destination IP | **172.38.1.5** | Host B sends reply to the NAT router's public IP |

---

## Summary of NAT Translation Process

```
Host A (192.168.0.3) ──► NAT Router ──► Internet ──► Host B (213.18.2.4)
  Source: 192.168.0.3        Source becomes: 172.38.1.5
  Dest:   213.18.2.4         Dest remains:   213.18.2.4

Host A (192.168.0.3) ◄── NAT Router ◄── Internet ◄── Host B (213.18.2.4)
  Dest: 192.168.0.3          Dest becomes: 192.168.0.3
  Src:  213.18.2.4           Src remains:  213.18.2.4
```

The NAT router maintains a **translation table** to track which internal host corresponds to each active connection, enabling correct delivery of return packets.
