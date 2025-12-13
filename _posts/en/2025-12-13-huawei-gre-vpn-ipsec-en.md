---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Huawei GRE VPN Uses GRE over IPsec
translated: false
type: note
---

**Question:** Which of the following VPN technologies on Huawei devices uses GRE over IPsec by default in route-based mode?  
A) L2TP VPN  
B) GRE VPN  
C) IPsec VPN  
D) VxLAN VPN

**Answer:**

The correct answer is **B) GRE VPN**.

On Huawei devices, **GRE VPN** in route-based mode (using tunnel interfaces) commonly uses **GRE over IPsec** by default when IPsec protection is applied. This setup protects GRE-encapsulated traffic (including multicast or broadcast packets, which plain IPsec cannot handle directly) by applying an IPsec profile to the GRE tunnel interface. Huawei documentation frequently describes this configuration for scenarios requiring multicast support over VPN tunnels, such as running dynamic routing protocols.

- **L2TP VPN** typically uses L2TP over IPsec for remote access, not GRE.
- **IPsec VPN** alone is usually policy-based or direct route-based without GRE unless explicitly combined.
- **VxLAN VPN** is a Layer 2 overlay technology and does not involve GRE over IPsec.

This aligns with Huawei's standard configurations for GRE tunnels needing encryption in route-based setups.

**References:**

- [Example for Establishing GRE over IPSec Tunnel Using a Tunnel Interface - Huawei](https://support.huawei.com/enterprise/en/doc/EDOC1100041799/fe280d94/example-for-establishing-gre-over-ipsec-tunnel-using-a-tunnel-interface)
- [Establishing GRE over IPSec Tunnels Between HUAWEI Firewalls and HUAWEI AR Routers - Huawei](https://support.huawei.com/enterprise/en/doc/EDOC1000154805/e0d89811/establishing-gre-over-ipsec-tunnels-between-huawei-firewalls-and-huawei-ar-routers)
- [IPsec Configuration Guide - Huawei](https://support.huawei.com/enterprise/en/doc/EDOC1100279274/1e88f885/ipsec-configuration)