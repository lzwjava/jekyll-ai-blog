---
audio: false
generated: true
image: false
lang: en
layout: post
title: Honeypot Network for Security Study
translated: false
type: note
---

Question: If we don't use our home LAN, can we set up a separate home LAN — for example, using a second router in Guangzhou to host some computers that provide services to outsiders — in order to study or anticipate hacker attacks?

Answer:
Yes, this is a well-established security practice, generally called a **honeypot** or **honeynet** setup. The idea is to isolate a "decoy" network from your real home network so that any attack traffic stays contained and can be observed safely. Here's how it's typically structured:

**1. Physical/network separation**
- Use a second router (or a separate ISP line/SIM if possible) so the honeypot network has its own public IP and doesn't share a switch, VLAN, or gateway with your real home devices.
- If you must share one internet connection, put the second router **behind** the main one and set it to a different subnet, then use firewall rules to block any traffic from the honeypot subnet into your main LAN. This is the most important step — never let compromised honeypot machines have a path back to your real devices.

**2. What runs on the honeypot LAN**
- Old or spare computers, a Raspberry Pi, or (more commonly today) virtual machines/containers set up specifically to look like real services (web server, SSH, FTP, IoT device, etc.).
- Popular open-source honeypot tools: Cowrie (SSH/Telnet), Dionaea (malware capture), T-Pot (a whole honeypot platform bundling many sensors), or OPNsense/pfSense with an isolated DMZ port for routing.

**3. Monitoring/logging**
- Run packet capture (tcpdump/Wireshark) and centralized logging (e.g., an ELK stack or Graylog) on a monitoring machine that only receives one-way log traffic from the honeypot, so attackers can't reach it.
- Snapshot VMs regularly so you can revert instantly if a machine gets fully compromised.

**4. Legal/practical notes for doing this in Guangzhou (or anywhere in China)**
- Exposing services to the public internet on a residential ISP line may violate your ISP's terms of service, and some ISPs block inbound ports on home connections by default — you may need a business line or a cloud VPS instead.
- China's Cybersecurity Law and related regulations require you to keep basic security logs and cooperate with authorities if your network is used as a launch point for further attacks (even unintentionally, e.g., if a compromised honeypot gets used to attack a third party) — so the network isolation and monitoring steps above aren't just good practice, they reduce your liability exposure too.
- Many researchers instead run honeypots on a cheap **cloud VPS** (outside their home network entirely) specifically to avoid exposing their home IP/ISP connection to attack traffic. This is often simpler and safer than hosting from home.

If your real goal is just to protect your home network rather than run a research honeypot, a simpler and lower-risk approach is: keep IoT/guest devices on a separate router/VLAN from your main devices, enable your main router's built-in firewall/IDS features, and monitor logs — without exposing anything intentionally to the public internet.

References:
- [T-Pot: The All In One Honeypot Platform](https://github.com/telekom-security/tpotce)
- [Cowrie SSH/Telnet Honeypot](https://github.com/cowrie/cowrie)
- [OWASP Honeypot Project Overview](https://owasp.org/www-community/Honeypots)
