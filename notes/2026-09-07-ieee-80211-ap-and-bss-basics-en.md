---
audio: false
generated: true
image: false
lang: en
layout: post
title: IEEE 802.11 AP and BSS Basics
translated: false
type: note
---

Question: What is IEEE 802.11, and what do **AP** and **BSS** mean inside it?

Answer:

![Image](https://images.openai.com/static-rsc-4/KcIG_5yF_R-LD25uBILzsHTVW43IiTtMr1PEEfEmusAltZirbSxGF0ssAZ3CHzEQ1YDCIQv4evt6e6iDu2ZbfeG-vEzSYVC6qlwUfeNs-MzIf5kBl75VzZy-2VAqRCIMzRyjhVsd_TQiZPYGndpYz4t3RFSwqVmFkewc4g08o285ukzlLHl7XMN6o6mWBNYv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/-Oz1bUvPSyg4jLrGlOMye4zjvflr2-y956_drl1s7RJfanWOM53cdQlp-GoS_F7uSaEGMPQr3sB3ZmmD7fBnI1U50vl4V-WTlR-qVDFexkFQzG3pQmtLEd9AkTTQaN0rvCbIkyPC7bu5xr085D91nWQndeE_vf4tJfIC7tzgrhE0VLpDzZyMJ634GFOam2PQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Z1orJ7tqK_urZ7vm_5713Qq_p3hiJ3diAjFJQJr1eYDycL8Tlp0cw17J9oZBhCM-kuanDnojpUkpEHf3asmaOlncpJR6CYIl-UYd6oRwSCg29BHbxLXTs3JwgaNgKOof2WSqp-67pOBMyKcUQRPTbKj70UutsLNQ0m_P4BiF5Sr-4Vxs3PU-PJBceJK6DsiE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tDB7KP1-eug-yIqCMIDkZqmifbTVqg7vah90dvA9fAAStmi5Dw_Xi3SwT0IgXrDkVSSTBAmIVaZ--sgvprTmkvyyPcxHdEM9STlhqbpFHnlVCUfotjQ0mcV40M8-ofhq_TfNzlFWLUovwDFENcgKSmgowSRi5yXRwOxLDEV7vjgiP_DNcvrpAJXyjuARiJId?purpose=fullsize)

### 1. What is 802.11?

**IEEE 802.11 is the family of standards that defines Wi-Fi.**

Think of it as the specification for how wireless devices communicate at the **MAC + PHY layers**:

```text
Application
    │
TCP / UDP
    │
IP
    │
802.11 MAC        ← Wi-Fi protocol
    │
802.11 PHY        ← radio: 2.4 / 5 / 6 GHz, modulation, coding
    │
   RF
```

Ethernet is mainly **IEEE 802.3**.

Wi-Fi is mainly **IEEE 802.11**.

Different generations correspond to amendments:

```text
802.11b  → 2.4 GHz
802.11a  → 5 GHz
802.11g  → 2.4 GHz
802.11n  → Wi-Fi 4
802.11ac → Wi-Fi 5
802.11ax → Wi-Fi 6 / 6E
802.11be → Wi-Fi 7
```

The important thing is that **802.11 is not just "the radio frequency."** It defines things such as:

* MAC addresses
* Wi-Fi frames
* association/authentication
* AP behavior
* channel access
* retransmission
* beacon frames
* encryption/security mechanisms
* PHY modulation/coding

---

# 2. What is a STA?

Before AP/BSS, there is another important term:

**STA = Station**

A STA is basically a Wi-Fi device participating in an 802.11 network.

For example:

```text
             Wi-Fi
               │
       ┌───────┴───────┐
       │               │
    Laptop           Phone
      STA              STA
```

Your laptop's Wi-Fi card is a **STA**.

Your phone's Wi-Fi card is another **STA**.

An AP also contains a wireless station interface conceptually, but in normal 802.11 terminology we distinguish the AP from ordinary client STAs.

---

# 3. What is an AP?

**AP = Access Point**

An AP is the device that provides access to a wireless network.

For example:

```text
                 Internet
                    │
                 Router
                    │
              ┌─────┴─────┐
              │     AP    │
              └─────┬─────┘
                    │
          ~~~~~~~~~ Wi-Fi ~~~~~~~~~
             │          │
          Laptop       Phone
           STA          STA
```

A home Wi-Fi router is usually doing several jobs simultaneously:

```text
┌───────────────────────────────┐
│ Home router                   │
│                               │
│  AP                           │
│  DHCP server                  │
│  NAT                          │
│  Ethernet switch              │
│  Firewall                     │
│  Router                       │
└───────────────────────────────┘
```

But **802.11 AP specifically means the Wi-Fi-side role**.

---

# 4. What is a BSS?

This is the key concept.

**BSS = Basic Service Set**

A BSS is essentially **one 802.11 wireless network cell**, centered around an AP in infrastructure mode.

For example:

```text
                    BSS
        ┌─────────────────────────┐
        │                         │
        │       AP                │
        │        ●                │
        │      / | \              │
        │     /  |  \             │
        │    ●   ●   ●            │
        │   STA STA STA            │
        │                         │
        └─────────────────────────┘
```

So:

```text
BSS
 ├── AP
 ├── STA
 ├── STA
 └── STA
```

The AP and its associated stations form a **BSS**.

The AP has a special identifier called the **BSSID**:

```text
BSSID = MAC address identifying the BSS
```

Typically the BSSID is the MAC address of the AP's wireless interface.

---

# 5. SSID vs BSSID

This distinction is extremely important.

Suppose your router broadcasts:

```text
SSID = MyWiFi
```

Your laptop might see:

```text
SSID       BSSID               Channel
------------------------------------------------
MyWiFi     AA:BB:CC:11:22:33   36
```

**SSID** is the human-facing network name.

**BSSID** identifies a particular BSS.

Think:

```text
SSID
  │
  │ "MyWiFi"
  │
  ├──────── BSS #1
  │          BSSID = AA:BB:CC:11:22:33
  │
  └──────── BSS #2
             BSSID = AA:BB:CC:44:55:66
```

This becomes important when you have multiple APs.

---

# 6. Multiple APs → ESS

Imagine a company has three APs:

```text
              SSID = CompanyWiFi

        AP1              AP2              AP3
         ●                ●                ●
       / | \            / | \            / | \
      STA STA          STA STA          STA STA
```

Each AP normally creates its own **BSS**:

```text
BSS1                BSS2                BSS3
 ┌─────┐              ┌─────┐              ┌─────┐
 │ AP1 │              │ AP2 │              │ AP3 │
 │ STAs│              │ STAs│              │ STAs│
 └─────┘              └─────┘              └─────┘
```

But they can all advertise the same SSID:

```text
             SSID = CompanyWiFi

BSS1              BSS2              BSS3
 AP1                AP2                AP3
```

Together, these BSSes can form an:

**ESS = Extended Service Set**

```text
                 ESS
 ┌──────────────────────────────────────────┐
 │                                          │
 │   BSS1       BSS2        BSS3            │
 │    AP1        AP2         AP3            │
 │     ●          ●           ●             │
 │                                          │
 └──────────────────────────────────────────┘
```

This is how large Wi-Fi networks work.

You walk around a building:

```text
        AP1                 AP2                 AP3
         ●                   ●                   ●
       )))))               )))))               )))))
          \                  |                  /
           \                 |                 /
            ─────── Ethernet / LAN ───────────
```

Your laptop can move:

```text
STA
 │
 ├── associated with AP1
 │
 │       walking →
 │
 ├── roam to AP2
 │
 │       walking →
 │
 └── roam to AP3
```

The **SSID can remain `CompanyWiFi`**, while the STA changes which **BSSID/AP** it is associated with.

---

# 7. The hierarchy

The easiest mental model is:

```text
802.11
 │
 └── ESS
      │
      ├── BSS
      │    ├── AP
      │    ├── STA
      │    ├── STA
      │    └── STA
      │
      ├── BSS
      │    ├── AP
      │    └── STAs
      │
      └── BSS
           ├── AP
           └── STAs
```

And:

```text
SSID  → logical/human network name
BSSID → specific BSS/AP identity
BSS   → one Wi-Fi cell
ESS   → collection of interconnected BSSes
STA   → Wi-Fi client/device
AP    → device providing the wireless access point
```

### The most useful distinction

If you are debugging Wi-Fi at packet level, remember:

```text
                 "What network?"
                      │
                     SSID
                      │
                 "Which AP?"
                      │
                    BSSID
                      │
                 "Which client?"
                      │
                  STA MAC
```

And an 802.11 packet will often contain addresses that let you determine **who is transmitting, who is receiving, which AP/BSS is involved, and how the frame is being forwarded**.

That leads naturally into the really interesting part of 802.11: **the 3-address/4-address frame format, Beacon → Probe → Authentication → Association → Data**, which makes the AP/BSS concepts concrete at packet level. I can walk through that next with actual 802.11 frame examples.
