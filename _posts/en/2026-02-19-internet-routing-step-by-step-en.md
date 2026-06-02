---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Internet Routing Works Step by Step
translated: false
type: note
---

Great question! You’re touching on the core of how the internet routes traffic from your device to a destination like `google.com`. Here’s a step-by-step breakdown of how routing works, using your `traceroute` example:

---

### 1. **DNS Resolution**
- When you type `google.com`, your device first queries a **DNS server** to resolve the domain name to an IP address (e.g., `142.250.73.78`).
- This IP is the final destination for your packets.

---

### 2. **Local Routing Table**
- Your device checks its **local routing table** to decide where to send the packet next.
- For most home networks, the default route is your **home router** (e.g., `192.168.1.1`).
- Your device sends the packet to `192.168.1.1` because it’s the **default gateway** for all non-local traffic.

---

### 3. **Router Forwarding**
- Your home router (`192.168.1.1`) receives the packet and checks its own routing table.
- It knows that for any IP not in your local network, it should forward the packet to your **ISP’s router** (the next hop).
- The ISP’s router is usually the first external IP you see in `traceroute` (e.g., `14.147.135.206`).

---

### 4. **ISP and Beyond**
- Your ISP’s router receives the packet and checks its **routing table**.
- ISPs use **Border Gateway Protocol (BGP)** to exchange routing information with other ISPs and networks.
- BGP dynamically updates routing tables to reflect the best path to each destination IP.
- Each router along the path repeats this process: it looks up the destination IP in its routing table and forwards the packet to the next hop.

---

### 5. **Dynamic Routing Updates**
- Routing tables are **not static**. They are updated dynamically using protocols like:
  - **BGP** (for inter-network routing, e.g., between ISPs)
  - **OSPF** or **RIP** (for intra-network routing, e.g., within an ISP’s network)
- If a link fails or a better path is found, BGP/OSPF updates the tables and reroutes traffic.

---

### 6. **Traceroute in Action**
- Each line in your `traceroute` output represents a router (hop) that forwarded your packet.
- The `*` means the router didn’t respond (common for security reasons).
- The IP addresses you see are the interfaces of routers that responded.

---

### 7. **Proxy Note**
- Your output shows a proxy (`127.0.0.1:7890`). This means your traffic is being routed through a local proxy before reaching the internet.
- The proxy may alter the path or hide some hops, but the fundamental routing process remains the same.

---

### **Summary Table: How Routing Works**

Routing Process


| Step                | Action                                                                 |
|---------------------|------------------------------------------------------------------------|
| DNS Resolution      | `google.com` → `142.250.73.78`                                        |
| Local Device        | Sends packet to default gateway (`192.168.1.1`)                       |
| Home Router         | Forwards to ISP’s router (`14.147.135.206`)                           |
| ISP Router          | Uses BGP/OSPF to forward to next hop                                  |
| Destination Network | Final routers deliver packet to `142.250.73.78`                       |

---

### **Key Points**
- **Routing tables** are like maps for routers, telling them where to send packets next.
- **BGP** is the protocol that keeps the internet’s routing tables up-to-date.
- **Traceroute** shows the path your packet takes, hop by hop.

Would you like a deeper dive into any specific part, like BGP or how ISPs manage routing?
