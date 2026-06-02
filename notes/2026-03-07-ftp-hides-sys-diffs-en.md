---
audio: false
generated: true
image: false
lang: en
layout: post
title: FTP Hides System Differences
translated: false
type: note
---

Question: In a heterogeneous network, FTP is used to transfer files between any computers. This is because FTP ________ the differences (details) between computers.

Answer:

**Answer: 屏蔽 (Shields / Hides)**

---

## Explanation

### What is a Heterogeneous Network?

A **heterogeneous network** refers to an environment where computers may differ in:

- Operating systems (e.g., Windows, Linux, macOS, Unix)
- Directory structures
- File naming conventions
- Character sets (e.g., ASCII vs. EBCDIC)
- Underlying hardware architectures

### Why Can FTP Transfer Files Across Any Computer?

The systems involved in FTP connections are heterogeneous — they differ in operating systems, directory structures, character sets, etc. FTP **shields** the user from these differences and transfers data efficiently and reliably.

In other words, FTP acts as an **abstraction layer** that hides (shields / 屏蔽) all these underlying technical differences between computers, so that the end user does not need to worry about what OS or file system the remote machine is using.

### How Does FTP Achieve This?

FTP's design enables data exchange across heterogeneous systems, supporting file transfers, appending, renaming, and deleting files and directories on remote hosts, **regardless of differences in underlying architectures, operating systems, file systems, and character sets**.

FTP does this by:

1. **Standardizing the transfer process** using a universal client-server model
2. **Supporting multiple file types** — ASCII, EBCDIC, and binary (image) formats
3. **Using two separate TCP connections** — one for control commands (port 21), and one for data transfer (port 20)

### Key Concept for the Exam

The blank should be filled with **屏蔽 (shield/hide)**. The full sentence reads:

> 异构网络采用FTP在任意计算机之间传送文件，这是因为FTP **屏蔽** 了各计算机之间的细节。

This means FTP **shields/hides** the differences (details) between different computers — including OS differences, file system differences, and character encoding differences — allowing seamless file transfer across any two machines in a heterogeneous network.

---

References:

- [FTP in Computer Networks - GeeksforGeeks](https://www.geeksforgeeks.org/file-transfer-protocol-ftp/)
- [File Transfer Protocol - ScienceDirect](https://www.sciencedirect.com/topics/computer-science/file-transfer-protocol)
- [NFS vs FTP - Cloud Infrastructure Services](https://cloudinfrastructureservices.co.uk/nfs-vs-ftp-whats-the-difference/)
