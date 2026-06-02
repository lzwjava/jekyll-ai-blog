---
audio: false
generated: true
image: false
lang: en
layout: post
title: NetWare The LAN Revolution Ends
translated: false
type: note
---

Novell NetWare is a foundational chapter in the history of network computing. It was a pioneering and dominant network operating system (NOS) developed by Novell, Inc., that enabled file sharing, printing, and other services for personal computers long before such capabilities were commonplace. For much of the 1980s and 1990s, it was the backbone of countless business and educational local area networks (LANs).

Here is a quick overview of its journey:

| **Aspect** | **Description** |
| :--- | :--- |
| **What it was** | A discontinued network operating system (NOS) developed by Novell, Inc., designed to provide file, print, and directory services for LANs . |
| **Developer** | Novell, Inc.  |
| **Initial Release** | 1983  |
| **Final Release** | Version 6.5 SP8 (May 6, 2009)  |
| **Key Protocols** | IPX/SPX (native), later added TCP/IP support natively in version 5 . |
| **Core Innovation** | Shifted from disk sharing to **file sharing**, introducing file-level access and locking for better efficiency and data integrity . |
| **Successor** | Open Enterprise Server (OES), which runs NetWare services on a SUSE Linux Enterprise Server kernel . |
| **Current Status** | Discontinued; general support ended in 2010, with extended support until the end of 2015 . |

### 📜 A Historical Powerhouse

- **Origins (Early 1980s)**: NetWare's story began in 1981 with a team of Brigham Young University students—Drew Major, Dale Neibaur, Kyle Powell, and later Mark Hurst—working on a consulting project. They initially aimed to create a disk-sharing system for CP/M but pivoted to building a file-sharing system for the then-new IBM-compatible PC. To test their creation, they even wrote a text-mode game called **Snipes**, which is recognized as one of the first network applications for a personal computer .
- **The File-Sharing Revolution**: NetWare's fundamental innovation was its shift from the prevalent "disk sharing" model to true **file sharing**. Instead of treating network storage as a remote disk drive, the NetWare server intelligently managed file access, locking, and data integrity at the file level. This approach, inspired by mainframe and minicomputer systems, was far more efficient and reliable than its competitors' offerings .
- **Hardware Independence and Performance**: A key to its success was its hardware independence. Unlike some rivals, NetWare could run on any Intel-based PC, supporting a wide range of network cards and hard drives . It was also renowned for its exceptional performance, often outperforming competitors by a significant margin due to its optimized kernel and efficient disk caching .

### 🏗️ Core Architecture and Key Features

- **Architecture**: NetWare was built around a dedicated server running a specialized multitasking kernel. Client workstations (initially running DOS) used a small Terminate-and-Stay-Resident (TSR) program to communicate with the server and map network drives as if they were local . The system's core components included:
    - **File Server Kernel**: Managed file systems, security, and client requests via the **NetWare Core Protocol (NCP)** .
    - **Workstation Shell**: Resided on client machines to redirect local requests to the network server .
    - **Communication Protocols**: Initially relied on the **IPX/SPX** protocol stack, which was derived from Xerox's XNS .
- **Innovative Features**: NetWare consistently introduced advanced features that set it apart:
    - **System Fault Tolerance (SFT)**: Provided robust data protection through read-after-write verification, disk mirroring (SFT II), and disk duplexing, ensuring high reliability .
    - **NetWare Directory Services (NDS)**: Introduced in version 4.x (1993), NDS was a revolutionary global directory service that allowed administrators to manage users, groups, and resources (like servers and printers) across the entire network from a single point. This was a major leap ahead of the flat "bindery" system used in earlier versions and was a precursor to directory services like Microsoft's Active Directory .
    - **Modularity (NLMs)**: Version 3.x introduced **NetWare Loadable Modules (NLMs)** , allowing administrators to dynamically load and unload services like anti-virus software, backup agents, and database support without rebooting the server .

### 📈 The Rise, Dominance, and Decline

- **Market Dominance**: By the early to mid-1990s, NetWare was the undisputed leader in the network operating system market, at one point holding over **70% market share** . Its performance, reliability, and advanced features made it the default choice for PC-based networking in businesses and schools worldwide .
- **Challenges and Decline**: Several factors contributed to its eventual decline:
    - **The Rise of Windows NT**: Microsoft's Windows NT offered a compelling alternative. It provided file and print services (a subset of NetWare's capabilities) but also functioned as an application server, email server, and even a desktop operating system. This vertical integration and a familiar Windows interface made it attractive .
    - **The TCP/IP Shift**: As the internet boomed, TCP/IP became the universal networking protocol. NetWare was late to fully embrace it, having been built natively on its own IPX/SPX protocol. While version 5.0 (1998) introduced native TCP/IP support, it was a significant transition that came relatively late .
- **Legacy and Successor**: Novell eventually transitioned its services to the Linux platform. The successor to NetWare, **Open Enterprise Server (OES)** , was released in 2005. OES allows all the services that were once hosted by NetWare to run on a SUSE Linux Enterprise Server kernel, marking the end of the line for the original NetWare kernel. The final version of NetWare, 6.5 SP8, was released in 2009, with support officially ending in 2015 .

In summary, NetWare was more than just a product; it was the engine that powered the first generation of large-scale PC networks. Its pioneering concepts in file sharing, directory services, and system fault tolerance laid the groundwork for modern network operating systems, leaving an indelible mark on the IT world.

I hope this comprehensive introduction gives you a clear picture of NetWare's significance. Are you interested in a more detailed look at a specific version or its technical protocols like NDS?
