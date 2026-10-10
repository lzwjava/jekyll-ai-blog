---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to Telephone Networks
translated: false
type: note
---

Question: What is an introduction to telephone networks (电话网)?

Answer:

## Telephone Networks (电话网) — Introduction

A **telephone network** (电话网) is an interconnected system of infrastructure and protocols that enables voice (and data) communication between users across local, national, and global distances. It is one of the oldest and most widespread communication networks in the world.

---

### Core Concepts

- **Switching** — the mechanism that connects two endpoints for a call
- **Circuit switching** — a dedicated path is reserved for the duration of a call (traditional PSTN)
- **Packet switching** — voice is broken into data packets and routed dynamically (VoIP/modern networks)
- **Duplex** — telephone calls are **full-duplex** (both parties can speak and listen simultaneously — unlike walkie-talkies)

---

### Types of Telephone Networks

| Type | Full Name | Description |
|------|-----------|-------------|
| **PSTN** | Public Switched Telephone Network | Traditional copper-wire landline network; the "plain old telephone system" |
| **PLMN** | Public Land Mobile Network | The backbone behind cellular/mobile networks (2G–5G) |
| **VoIP** | Voice over Internet Protocol | Voice carried over the internet (WhatsApp, Skype, Zoom) |
| **ISDN** | Integrated Services Digital Network | Early digital upgrade to PSTN; largely obsolete |
| **PBX** | Private Branch Exchange | Private internal telephone system (offices, hotels) |

---

### How a Traditional Call Works (PSTN)

```
Caller → Local Loop → Central Office (CO) → Trunk Lines → CO → Local Loop → Receiver
```

1. **Local loop** — the "last mile" copper wire from your home to the nearest exchange
2. **Central Office (CO)** — telephone exchange that routes calls locally
3. **Trunk lines** — high-capacity inter-exchange links (fiber, microwave, satellite)
4. **Circuit reservation** — a 64 Kbps channel is reserved end-to-end for the call duration

---

### Mobile Telephone Networks (移动电话网)

Modern cellular networks are the dominant form of telephone network:

| Generation | Era | Key Feature |
|------------|-----|-------------|
| **1G** | 1980s | Analog voice only |
| **2G (GSM/CDMA)** | 1990s | Digital voice, SMS, basic data |
| **3G (WCDMA/CDMA2000)** | 2000s | Mobile internet, video calls |
| **4G (LTE)** | 2010s | Broadband data, VoIP-native |
| **5G (NR)** | 2020s | Ultra-low latency, massive IoT, high bandwidth |

Cellular networks divide coverage into **cells**, each served by a **base station (基站)**. As you move, your call is handed off between cells seamlessly.

---

### VoIP — The Modern Shift

Most modern "phone calls" are now **VoIP** at some layer:

- Voice is digitized → compressed (codecs like G.711, Opus) → packetized → sent over IP
- Protocols: **SIP** (Session Initiation Protocol), **RTP** (Real-time Transport Protocol)
- Examples: WhatsApp calls, FaceTime, WeChat voice, enterprise Teams/Zoom
- Advantage: much cheaper, integrates with internet infrastructure
- Challenge: quality depends on network conditions (latency, jitter, packet loss)

---

### Key Components of a Telephone Network

| Component | Role |
|-----------|------|
| **Terminal / Handset** | End-user device (phone) |
| **Local Loop** | Connection from user to exchange |
| **Exchange / Switch** | Routes calls between subscribers |
| **Trunk / Backbone** | Long-distance high-capacity links |
| **Signaling System (SS7)** | Protocol for call setup, routing, billing on PSTN |
| **HLR/HSS** | Mobile network subscriber database |
| **SIM Card** | Identifies mobile subscriber on PLMN |

---

### Telephone Networks vs. Walkie-Talkies

| Feature | Telephone Network | Walkie-Talkie |
|---------|-------------------|---------------|
| Duplex | Full-duplex | Half-duplex |
| Infrastructure | Requires network | Direct radio, no infrastructure |
| Range | Global | Local (meters to tens of km) |
| Cost | Per-call or subscription | One-time hardware |
| Reliability in disasters | Depends on towers/grid | More resilient |

---

### Regulation

- In **Hong Kong**, telephone networks are regulated by **OFCA** (Office of the Communications Authority)
- Operators must hold a **Unified Carrier Licence (UCL)**
- Major HK operators: HKT (PCCW), SmarTone, China Mobile HK, 3HK

---

References:
- [ITU — Telecommunication Standardization](https://www.itu.int/en/ITU-T/Pages/default.aspx)
- [OFCA Hong Kong — Telecommunications](https://www.ofca.gov.hk/en/media_focus/telecommunications/)
- [Cisco — PSTN Overview](https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucme/pstn/index.html)
- [GSMA — Mobile Network Generations](https://www.gsma.com/technologies/)