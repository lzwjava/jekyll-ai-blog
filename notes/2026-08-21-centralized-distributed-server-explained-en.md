---
audio: false
generated: true
image: false
lang: en
layout: post
title: Centralized-Distributed Server Explained
translated: false
type: note
---

Question: Why is the server that provides complete data and directory sharing for workstations on a LAN called a "集散服务器" (centralized-distributed server)?

Answer:

The term **集散** (jí sàn) combines two concepts:

- **集 (jí)** = to **collect / centralize** — the server *gathers* all data, files, and directory information into one place
- **散 (sàn)** = to **distribute / scatter** — the server then *distributes* that information out to all workstations on the LAN

So a **集散服务器** is a server that acts as a **central hub**: it centralizes storage and management of complete data and directory resources, then distributes access to all workstations on the network.

**Why the other options are wrong:**

| Option | Term | Why incorrect |
|--------|------|---------------|
| A | 联机 (online) | Refers to a device being *connected/online*, not a sharing architecture |
| B | 脱机 (offline) | Refers to operating *without* a network connection |
| D | 分时 (time-sharing) | Refers to *timesharing systems* where CPU time is divided among users, not full data sharing |

**In summary:** The 集散 model is specifically designed so one server holds *complete* data (not partial), and every workstation can access the full shared resources — matching exactly the definition in the question.

---

References:
- [LAN Server Types Overview](https://en.wikipedia.org/wiki/File_server)
- [Centralized vs Distributed Architecture](https://en.wikipedia.org/wiki/Distributed_computing)