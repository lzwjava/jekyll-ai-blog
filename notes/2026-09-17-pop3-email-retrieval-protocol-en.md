---
audio: false
generated: true
image: false
lang: en
layout: post
title: POP3 Email Retrieval Protocol
translated: false
type: note
---

Question: What is POP3?

Answer: **POP3 (Post Office Protocol version 3)** is a protocol used by an email client to **retrieve emails from a mail server**.

The simplest mental model:

```text
                    Internet
                       │
                       ▼
┌──────────────┐   POP3   ┌────────────────┐
│ Email client │ ◄──────── │  Mail server   │
│ Thunderbird  │           │  inbox         │
│ Outlook      │           │                │
└──────────────┘           └────────────────┘
```

### How POP3 works

Suppose you have:

```text
alice@example.com
```

and open an email client.

1. Client connects to the mail server.
2. It authenticates with username/password.
3. It asks: **"What messages are in my mailbox?"**
4. Server sends the messages.
5. Client typically **downloads them locally**.
6. Depending on configuration, the server may delete the downloaded messages.

The important idea is:

> **POP3 is primarily a download protocol.**

### POP3 vs IMAP

This is the important distinction:

|                          | POP3                  | IMAP              |
| ------------------------ | --------------------- | ----------------- |
| Main purpose             | Download mail         | Synchronize mail  |
| Mail stored locally      | Usually               | Usually cached    |
| Mail remains on server   | Optional              | Yes               |
| Folders synchronized     | No                    | Yes               |
| Read/unread state synced | No                    | Yes               |
| Multiple devices         | Poor fit              | Excellent         |
| Typical modern usage     | Legacy/simple clients | Most modern email |

For example, with POP3:

```text
Mail server
    │
    │ download
    ▼
Laptop
```

Your phone may not know what happened on the laptop.

With IMAP:

```text
                 ┌── Laptop
                 │
Mail server ◄────┼── Phone
                 │
                 └── Desktop
```

All devices synchronize against the same server-side mailbox.

### POP3 ports

Common configurations:

```text
POP3       TCP 110
POP3S      TCP 995  ← POP3 over TLS
```

Modern deployments generally use **995/TLS** rather than unencrypted port 110.

### Protocol-level example

A simplified POP3 session looks like:

```text
S: +OK POP3 server ready
C: USER alice@example.com
S: +OK
C: PASS <PASSWORD>
S: +OK logged in

C: STAT
S: +OK 3 18234

C: LIST
S: +OK
S: 1 5234
S: 2 8123
S: 3 4877

C: RETR 1
S: +OK
S: <email contents>

C: QUIT
S: +OK goodbye
```

The protocol is therefore quite simple: **TCP connection → authentication → inspect messages → retrieve messages → quit**.

One useful way to remember the email protocols:

```text
SMTP  = send mail
POP3  = download mail
IMAP  = synchronize/read mail
```

I can also walk through **SMTP + POP3 + IMAP as a complete end-to-end email delivery system**, including DNS MX records and the actual TCP connections.
