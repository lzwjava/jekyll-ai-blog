---
audio: false
generated: true
image: false
lang: en
layout: post
title: Access Point in WLAN Explained
translated: false
type: note
---

Question: What is **AP** in WLAN?

Answer: **AP = Access Point**.

In a **WLAN (Wireless Local Area Network)**, an AP is the device that provides wireless network access to client devices such as laptops, phones, and IoT devices.

![Image](https://images.openai.com/static-rsc-4/YY6PR6JuI4SX1sMEYq16h7U6Zcyk3V8SFSVAgcGS8CzJdlGAYFFsac8CRYwDV-ZHQS6mqL6HeuG03jHSvnHhHiL01BcGjbs7YWGsuvfKl3pXpIgPgXJ_CnFD2kMpCnqkPljO7HG46LElcseZI6kUKLYhJrxJ5DLTvzvYcTKlEoRrrfaYYccfRRBw5ai8eIa4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/nnYycuDlbYHarHoMMm0WG2PgJU-9SJNcJE7GzdlQAkl35kv0L3LXR5ucMvs9FxpEq0P6nRF_TOiBNu8kK1ZrtJcGeOrwDbB9kz78tmZEgradykb65lwCoyHMjEr-ApADZeQWWLWOaWwACPD959jK6vVhAdu6huBodWfPHNqNFcZtzT9xxPVzP870dvs6bcq8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Qpy9yH-pJ7FpD4HSmM2fwoMm5lIMucRFOLJvU7rTMDy4qlwhBjUZ2YxaFmX2rbeCc69IthceNQKzlEKcP9fSB1Z0H5qeQ1ldeSTvVBt1exV8gXY7KKJ8u_lqeflC7PkLRw6j6FmBd1fYb_qsMDMJL0Y0Dl2yZsGKM2ZHVQX2pOXrO9FFU5r36fRoOGfFM1OV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Kt5R1VHBq-zsCnuA3oL6hybFB55bFhCipku1VhGxkh4VtiUzqarfsFKnYz8JPVDWc4OS3TDdLhNpe-VAjDbTBum5z0ozeZJcnBiotSN8glVdXvNu7a-3MVlm0QF6lGCdkQe1q261sZNrHJaE13jJYJsj2TOlf2ojR85eCnphN8_n-0ED3Gy8HJhxknR9fJ6V?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hb-JnYBEWxdG_S5e5Ghf6B6SVqMDwhUjBGc7Y5JTk-oRTj3lLz0TMs4wy3CcRCZ_WwpfV2gz3LOQm5ASh58WJFYR7vf-ws2dzGGbf1BL27o9UHJx1wRAbFXRdSoKerixJYdIwm8VBX6ydFTG96zDXLcLc_lErEuvlHBgGAk6-9_J8JgSlnnYS_oXg39QF_Iu?purpose=fullsize)

### Basic topology

```text
             Internet
                 |
              Router
                 |
          Ethernet / LAN
                 |
          +--------------+
          |      AP      |
          | Access Point |
          +--------------+
           /      |      \
          /       |       \
      Laptop    Phone    IoT device
       Wi-Fi     Wi-Fi      Wi-Fi
```

The AP essentially **bridges wireless 802.11 traffic to the wired LAN**.

For example:

```text
Laptop
   |
   | 802.11 / Wi-Fi
   v
  AP
   |
   | Ethernet / 802.3
   v
Switch
   |
   v
Router / Internet
```

### What does an AP actually do?

At a simplified level, an AP:

1. **Transmits Wi-Fi frames** over radio.
2. **Receives Wi-Fi frames** from clients.
3. Associates/authenticates wireless stations.
4. Bridges traffic between the wireless network and wired Ethernet.
5. Advertises an **SSID**, such as `MyWiFi`.
6. Handles Wi-Fi mechanisms such as channel access, encryption, and retransmission.

A useful distinction:

| Term       | Meaning                                      |
| ---------- | -------------------------------------------- |
| **WLAN**   | The wireless LAN/network                     |
| **AP**     | Access Point providing wireless connectivity |
| **STA**    | Wireless client/station, e.g. your laptop    |
| **SSID**   | Human-readable Wi-Fi network name            |
| **802.11** | IEEE protocol family underlying Wi-Fi        |

So when your laptop connects to:

```text
SSID: MyHomeWiFi
       ↓
      AP
       ↓
   Ethernet LAN
       ↓
    Router
       ↓
   Internet
```

the laptop is typically a **STA**, while the Wi-Fi device it associates with is the **AP**.

One subtle point: a modern home "Wi-Fi router" often combines **three things in one box**:

```text
Wi-Fi AP + Ethernet switch + IP router/NAT
```

So **AP ≠ router**. An AP specifically provides the wireless 802.11 access/bridge function.
