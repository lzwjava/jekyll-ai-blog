---
audio: false
generated: true
image: false
lang: en
layout: post
title: "SMTP Explained: The Email Sending Protocol"
translated: false
type: note
---

Question: What is SMTP?

Answer:

SMTP (Simple Mail Transfer Protocol) is the standard communication protocol used for sending and routing email messages across the internet. Here's a breakdown:

**How it works:**

- SMTP is a push protocol — it handles the *sending* and *relaying* of emails from a client to a server, or between servers
- When you hit "Send," your email client connects to an SMTP server (usually on port 25, 587, or 465), authenticates, and hands off the message
- The SMTP server then routes the email to the recipient's mail server

**Key roles:**

- **Mail submission** — from your email client to your provider's server
- **Mail relay** — from server to server across the internet
- **Not for receiving** — SMTP only *sends*; receiving uses IMAP or POP3

**Common ports:**

| Port | Use |
| ------ | ----- |
| 25 | Server-to-server relay |
| 587 | Client submission (with STARTTLS) |
| 465 | Client submission (implicit TLS) |

**Brief history:**
Defined in RFC 821 (1982) by Jon Postel, later updated by RFC 5321 (2008), which remains the current standard.

References:

- [RFC 5321 – Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
- [SMTP – MDN Web Docs Glossary](https://developer.mozilla.org/en-US/docs/Glossary/SMTP)
- [How Email Works – Cloudflare Learning Center](https://www.cloudflare.com/learning/email-security/what-is-smtp/)
