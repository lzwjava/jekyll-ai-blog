---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FTP 隐藏系统差异
translated: true
type: note
---

Question: 在异构网络中，使用 FTP 在任意计算机之间传输文件。这是由于 FTP ________ 了计算机之间的差异（细节）。

Answer:

**Answer: 屏蔽 (Shields / Hides)**

---

## 解释

### 什么是异构网络？

**Heterogeneous network** 指的是一种计算机可能在以下方面不同的环境：

- Operating systems（例如，Windows、Linux、macOS、Unix）
- Directory structures
- File naming conventions
- Character sets（例如，ASCII 与 EBCDIC）
- Underlying hardware architectures

### 为什么 FTP 可以在任意计算机之间传输文件？

FTP 连接涉及的系统是异构的——它们在 operating systems、directory structures、character sets 等方面不同。FTP **屏蔽** 了用户对这些差异的感知，并高效可靠地传输数据。

换句话说，FTP 充当一个 **abstraction layer**，隐藏（屏蔽 / shields）计算机之间所有这些底层技术差异，从而最终用户无需担心远程机器使用什么 OS 或文件系统。

### FTP 如何实现这一目标？

FTP 的设计允许跨异构系统的数据交换，支持文件传输、在远程主机上追加、重命名和删除文件及目录，**无论底层 architectures、operating systems、file systems 和 character sets 的差异**。

FTP 通过以下方式实现这一点：

1. 使用通用的 client-server 模型 **标准化传输过程**
2. **支持多种文件类型** —— ASCII、EBCDIC 和 binary (image) 格式
3. **使用两个独立的 TCP 连接** —— 一个用于控制命令（port 21），一个用于数据传输（port 20）

### 考试关键概念

空白处应填入 **屏蔽 (shield/hide)**。完整句子为：

> 异构网络采用FTP在任意计算机之间传送文件，这是因为FTP **屏蔽** 了各计算机之间的细节。

这意味着 FTP **屏蔽/隐藏**了不同计算机之间的差异（细节）——包括 OS 差异、文件系统差异和字符编码差异——从而允许在异构网络中任意两台机器之间无缝文件传输。

---

参考文献：

- [FTP in Computer Networks - GeeksforGeeks](https://www.geeksforgeeks.org/file-transfer-protocol-ftp/)
- [File Transfer Protocol - ScienceDirect](https://www.sciencedirect.com/topics/computer-science/file-transfer-protocol)
- [NFS vs FTP - Cloud Infrastructure Services](https://cloudinfrastructureservices.co.uk/nfs-vs-ftp-whats-the-difference/)
