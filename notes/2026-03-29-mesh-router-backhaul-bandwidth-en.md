---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Mesh Router Backhaul and Bandwidth
translated: false
type: note
---

Question: Do mesh routers require wired connections, and what is the purpose of their antennas if multiple APs are consuming all the home bandwidth? How should I understand mesh routers?

Answer:

You’re essentially asking about how mesh Wi-Fi systems work and the role of wiring vs. wireless connections. Let’s break it down:

1. **Wired vs. Wireless backhaul**

   * Many mesh routers support both **wired (Ethernet) backhaul** and **wireless backhaul**.
   * **Wired backhaul** means the nodes are connected via Ethernet cables. This provides **maximum speed and reliability**, because traffic between nodes doesn’t compete with the Wi-Fi clients.
   * **Wireless backhaul** means nodes communicate over Wi-Fi. This is convenient because you don’t need cables, but the available bandwidth is **shared**: each hop between nodes reduces the total throughput. So if multiple APs are active, they can consume much of your home bandwidth, reducing performance.

2. **Role of antennas**

   * The antennas on mesh routers serve two purposes:

     1. Communicating with **client devices** (phones, laptops, smart home devices).
     2. Communicating with **other mesh nodes** (if wireless backhaul is used).
   * Even if you have a wired backhaul, antennas are still needed for clients. With wireless backhaul, the same antennas handle both node-to-node and device connections, which is why bandwidth can get “eaten up” faster.

3. **Bandwidth sharing in mesh networks**

   * In wireless backhaul setups, bandwidth is **split at each hop**. For example, if your main router gets 500 Mbps from the ISP, a node one hop away may only be able to provide 250–300 Mbps to clients because it has to relay traffic.
   * If multiple nodes are actively serving clients, total available bandwidth is divided among all devices and hops.

4. **Practical understanding**

   * **Wired mesh:** Connect nodes via Ethernet. Antennas only serve client devices. Maximum speed, minimal interference.
   * **Wireless mesh:** No Ethernet needed. Antennas serve both clients and nodes. Convenient but throughput decreases with distance and number of hops.
   * If your goal is to maintain high bandwidth across multiple APs, **wired backhaul is strongly recommended**.

So, in short: mesh routers **don’t strictly require wired connections**, but using wires allows antennas to focus on client coverage instead of node-to-node communication, preventing bandwidth loss. Multiple APs consuming all bandwidth is typical in a wireless backhaul scenario.

You can think of it like a **water pipe system**: if all the water has to flow through one pipe (wireless), the further you go and the more taps (APs) you open, the lower the flow at each tap. Adding Ethernet cables is like giving each tap its own pipe—full flow everywhere.
