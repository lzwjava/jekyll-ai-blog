---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: DHCP Logs for Router WAN Interface
translated: false
type: note
---

### Understanding the DHCP Log Entries in 360 Wi-Fi Router T7

This log snippet from your 360 T7 router (likely extracted from the **System > Log** section in the web UI) shows the router's WAN interface acting as a DHCP client to obtain and renew its public IP address from your ISP's DHCP server. DHCP (Dynamic Host Configuration Protocol) is the standard protocol for automatically assigning IP addresses on networks. The router periodically requests or renews an IP lease to maintain internet connectivity—typically every 12-24 hours, depending on your ISP's lease time.

These entries are **normal and indicate healthy operation**, not an error. They represent the standard DORA process (Discover, Offer, Request, ACK) for initial IP assignment, followed by lease renewals. Here's a breakdown of each line in chronological order (note: the timestamps are in reverse order in your log, but I've reordered them for clarity; dates are in YYYY/MM/DD-HH:MM:SS format):

| Log ID | Timestamp          | Message                  | Explanation |
|--------|--------------------|--------------------------|-------------|
| 148   | 2025/09/19-03:44:57 | Sending DHCP discover   | The router broadcasts a **DHCP Discover** message on the WAN side to locate an available DHCP server (your ISP's). This is the first step when the lease expires or the router reboots. (It retries quickly at the next line.) |
| 147   | 2025/09/19-03:45:00 | Sending DHCP discover   | A retry of the Discover message (common if no immediate response; routers send 2-4 retries with exponential backoff). |
| 146   | 2025/09/19-03:45:02 | DHCP offer Received     | The ISP's DHCP server responds with a **DHCP Offer**, proposing an available IP address, subnet mask, gateway, DNS servers, and lease duration (e.g., 24 hours). |
| 145   | 2025/09/19-03:45:02 | Sending DHCP request    | The router sends a **DHCP Request** to accept the offered IP and formally ask the server to assign it (broadcast so other servers can withdraw their offers if any). |
| 144   | 2025/09/19-03:45:02 | DHCP ACK received       | The server sends a **DHCP ACK** (Acknowledge), confirming the IP assignment. The router now has a valid WAN IP and can connect to the internet. This completes the initial lease acquisition (~5 seconds total here). |
| 143   | 2025/09/19-15:45:02 | Sending DHCP renew      | ~12 hours later (halfway through a typical 24-hour lease), the router proactively sends a **DHCP Renew** (a unicast Request to the known server) to extend the lease without full rediscovery. |
| 142   | 2025/09/19-15:45:02 | DHCP ACK received       | The server acknowledges the renewal—lease extended seamlessly. |
| 141   | 2025/09/20-03:45:02 | Sending DHCP renew      | Another renewal ~12 hours later (now into the next day). If no ACK follows (not shown here), it might escalate to a full rebind or rediscover. |

#### Why This Happens
- **Lease Cycle**: ISPs set lease times (e.g., 24 hours). At 50% elapsed, the client renews to avoid downtime. If renewal fails at 87.5%, it rebinds (broadcast Request); at 100%, it restarts the full DORA process.
- **In 360 T7 Context**: This is logged under WAN connection events. The T7 uses a lightweight DHCP client (likely udhcpc-based) in its firmware, which generates these exact messages. No issues unless you see failures like "DHCP NAK received" (IP rejected) or repeated Discovers without ACKs (could indicate ISP problems or cable issues).
- **Troubleshooting Tips**:
  - If internet drops around these times, check WAN status in the UI (**Status > WAN**) for IP changes or errors.
  - Export full logs via UI for patterns.
  - To force a renew: Release/renew WAN in **Network > WAN** or reboot.

This is routine behavior—your router is just keeping its "internet ticket" valid.

[Understanding DHCP Basics (Microsoft)](https://learn.microsoft.com/en-us/windows-server/troubleshoot/dynamic-host-configuration-protocol-basics)
[DHCP Process Overview (Netmanias)](https://www.netmanias.com/en/post/techdocs/5998/dhcp-network-protocol/understanding-the-basic-operations-of-dhcp)
