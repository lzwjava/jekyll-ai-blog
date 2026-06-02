---
audio: false
generated: true
image: false
lang: en
layout: post
title: FreeBSD Storage Firewall and Expert
translated: false
type: note
---

Question: What are TrueNAS, OPNsense, and Allan Jude?

Answer:

**TrueNAS** is a popular open-source storage operating system (originally known as FreeNAS) developed by iXsystems. It is designed primarily for **network-attached storage (NAS)** purposes and is built around the powerful **OpenZFS** filesystem, which provides excellent data integrity, self-healing capabilities, snapshots, replication, and RAID-like protection (RAID-Z). TrueNAS allows users to store, share, and protect data using protocols like SMB, NFS, iSCSI, and more. It also supports virtualization (VMs and containers), making it suitable for home labs, media servers, backups, and even enterprise environments. There are free community editions (TrueNAS CORE based on FreeBSD, and TrueNAS SCALE based on Linux) and paid enterprise versions with commercial support and hardware appliances.

**OPNsense** is a free, open-source **firewall and routing platform** based on **FreeBSD**. It was created in 2015 as a fork of pfSense (which itself originated from m0n0wall). OPNsense provides advanced network security features, including a stateful firewall, VPN support (IPsec, OpenVPN, WireGuard), intrusion detection/prevention (IDS/IPS), traffic shaping, proxy capabilities, and a modern, user-friendly web interface. It is widely used for home networks, small businesses, and enterprises that want a powerful, customizable, and regularly updated alternative to commercial firewalls.

**Allan Jude** is a prominent figure in the **FreeBSD** and **OpenZFS** communities. He is a FreeBSD developer, ZFS expert, co-founder of Klara Inc. (a company focused on FreeBSD and open-source consulting/support), and a well-known educator in the BSD world. He co-authored books like "FreeBSD Mastery: ZFS" and has been a long-time co-host of the **BSD Now** podcast (along with other shows). He frequently speaks at conferences, contributes to FreeBSD/ZFS development, and is respected for his deep knowledge of storage systems, FreeBSD internals, and related technologies. Many people in the FreeBSD ecosystem admire his work and contributions.

These three are closely connected to **FreeBSD** — TrueNAS and OPNsense are both built on FreeBSD, and Allan Jude is a key contributor and advocate in that community. That's likely why fans of FreeBSD often appreciate all three together.

References:

- [TrueNAS official site](https://www.truenas.com/)
- [TrueNAS Wikipedia](https://en.wikipedia.org/wiki/TrueNAS)
- [OPNsense official site](https://opnsense.org/)
- [OPNsense Wikipedia](https://en.wikipedia.org/wiki/OPNsense)
- [Allan Jude on BSD Now](https://www.bsdnow.tv/hosts/allanjude)
- [Allan Jude LinkedIn](https://ca.linkedin.com/in/allanjude)
