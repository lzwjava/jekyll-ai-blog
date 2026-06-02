---
audio: false
generated: true
image: false
lang: en
layout: post
title: Email Systems Missing User Agent
translated: false
type: note
---

**Question:** What is the missing component in the Internet email system, which consists of ________, mail servers, and mail sending/receiving protocols?

**Answer:**

The correct answer is **User Agent (用户代理 / UA)**.

---

## The Three Major Components of the Internet Email System

The Internet mail system has three major components: **user agents**, **mail servers**, and the **Simple Mail Transfer Protocol (SMTP)**.

---

### 1. User Agent (UA) — 用户代理

The first component of an electronic mail system is the **User Agent (UA)**. It provides service to the user to make the process of sending and receiving a message easier. A UA is a software package (program) that composes, reads, replies to, and forwards messages. It also handles local mailboxes on the user's computer.

A Mail User Agent (MUA), commonly known as an **email client**, is a software application that allows users to send, receive, and manage their emails. Examples of popular MUAs include Microsoft Outlook, Mozilla Thunderbird, and web-based services like Gmail and Yahoo Mail.

---

### 2. Mail Server (邮件服务器)

A **Mail Transfer Agent (MTA)**, also referred to as a mail server, is software that transfers electronic mail messages from one computer to another using the Simple Mail Transfer Protocol. Messages exchanged across networks are passed between mail servers, including any attached data files such as images, multimedia, or documents.

---

### 3. Mail Sending/Receiving Protocols (邮件发送/读取协议)

Email servers rely on standardized protocols: **SMTP** (Simple Mail Transfer Protocol) is used for sending and relaying outgoing email messages, **POP3** (Post Office Protocol version 3) is used for retrieving emails from a server, and **IMAP** (Internet Message Access Protocol) is another protocol for accessing and managing email on the server.

---

### Summary Table

| Component | Role |
|---|---|
| **User Agent (UA)** | Interface for composing, sending, and reading emails |
| **Mail Server** | Stores and transfers messages between senders and recipients |
| **Protocols (SMTP/POP3/IMAP)** | Rules governing how emails are sent and retrieved |

---

> **Key Point for Exam:** The blank specifically asks for the **first** of the three components. The answer is **用户代理 (User Agent)**. It is the client-side software that users directly interact with, sitting "in front of" the mail server and protocols.

**References:**

- [2.4 Electronic Mail in the Internet - ic.uff.br](http://www2.ic.uff.br/~michael/kr1999/2-application/2_04-smtp.htm)
- [Mail User Agent Overview - ScienceDirect](https://www.sciencedirect.com/topics/computer-science/mail-user-agent)
- [Email Server Explained - Mailtrap](https://mailtrap.io/blog/email-server/)
- [What is Mail User Agent (MUA)? - saleslovesmarketing.co](https://saleslovesmarketing.co/glossary/mail-user-agent/)
