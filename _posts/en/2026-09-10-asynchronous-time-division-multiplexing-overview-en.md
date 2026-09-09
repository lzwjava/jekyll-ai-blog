---
audio: false
generated: true
image: false
lang: en
layout: post
title: Asynchronous Time Division Multiplexing Overview
translated: false
type: note
---

**Question:** What is Asynchronous Time Division Multiplexing (异步时分多路复用)?

**Answer:**

**Background — What is TDM?**

Time Division Multiplexing (TDM) is a technique where multiple data streams share a single communication channel by taking turns in time. The channel is divided into time slots, and each sender gets a turn.

**Synchronous TDM (the baseline)**

In Synchronous TDM, each time slot is pre-assigned to a fixed source. Slots are broadcast regardless of whether the sources actually have data to send, which wastes bandwidth when sources are idle.

**Asynchronous TDM (ATDM) — the improvement**

Asynchronous TDM, also called Statistical TDM, allocates time slots *dynamically* to data streams based on demand. A time slot is assigned only when the data stream has something to send, making it more flexible.

Key mechanics:
- In ATDM, if there are *n* input lines, the multiplexer scans all input lines and accepts data until a frame is filled. When the frame is filled, it is sent across the link. If senders don't have enough data to fill the frame, it is transmitted as partially filled.
- Since all sending devices can use any available slot, the receiver cannot identify data simply by counting slot positions — an addressing mechanism is required, supplying a unique address to each time slot.

**Key advantages over Synchronous TDM**

Time slots are used only when data needs to be sent, avoiding bandwidth wastage. Dynamic allocation allows more flexible use of available bandwidth, assigning more slots to data streams with higher demand.

**Real-world application**

Asynchronous Transfer Mode (ATM) — a major telecom switching technology — uses asynchronous time-division multiplexing to encode data into small, fixed-sized cells. ATM was widely deployed in backbone networks in the 1990s–2000s.

**Synchronous vs. Asynchronous TDM at a glance:**

| | Synchronous TDM | Asynchronous TDM |
|---|---|---|
| Slot assignment | Fixed, pre-assigned | Dynamic, on demand |
| Bandwidth waste | Yes (idle slots wasted) | No (slots always carry data) |
| Addressing needed | No | Yes (address per slot) |
| Also known as | — | Statistical TDM |
| Scalability | Limited to N devices = N slots | Can support more devices than slots |

---

**References:**
- [Difference between Synchronous TDM and Asynchronous TDM – GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/difference-between-synchronous-tdm-and-asynchronous-tdm/)
- [Asynchronous Time Division Multiplexing – TutorialsPoint](https://www.tutorialspoint.com/data_communication_computer_network/asynchronous_tdm.htm)
- [What is ATM? – Dialogic](https://www.dialogic.com/glossary/asynchronous-transfer-mode-atm)
