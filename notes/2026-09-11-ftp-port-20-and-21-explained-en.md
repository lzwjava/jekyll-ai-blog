---
audio: false
generated: true
image: false
lang: en
layout: post
title: FTP Port 20 and 21 Explained
translated: false
type: note
---

Question: In FTP, is port 20 used for data transfer and port 21 for control?

Answer: Yes, that's correct — but with a small nuance worth knowing:

- **Port 21** — Control connection. This is always used to send FTP commands and receive responses (e.g., login credentials, directory navigation commands).
- **Port 20** — Data connection, but **only in Active Mode**. When the client is in active mode, the server initiates the data connection back to the client using port 20.

In **Passive Mode** (PASV), which is more common today because it works better through firewalls and NAT, the data connection uses a **random ephemeral port** negotiated between client and server — port 20 is not involved.

So:
| Mode | Control Port | Data Port |
|------|-------------|-----------|
| Active | 21 | 20 |
| Passive | 21 | Random (1024–65535) |

References:
- [RFC 959 – File Transfer Protocol](https://www.rfc-editor.org/rfc/rfc959)
- [FTP Active vs Passive Mode – IBM Docs](https://www.ibm.com/docs/en/i/7.5?topic=protocols-ftp)