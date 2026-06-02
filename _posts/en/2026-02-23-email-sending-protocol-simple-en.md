---
audio: false
generated: true
image: false
lang: en
layout: post
title: Email Sending Protocol Explained Simply
translated: false
type: note
---

Question: What protocol is used to send an email from a user agent to a mail server?

Answer:

The correct protocol used to send an email from a user agent (such as Outlook, Thunderbird, or a webmail interface acting as a client) to a mail server is **SMTP** (Simple Mail Transfer Protocol).

Here is a breakdown of the options provided:

*   **A. SNMP (Simple Network Management Protocol):** This protocol is used for managing and monitoring network devices like routers, switches, and servers. It is not involved in email transmission.
*   **B. SMTP (Simple Mail Transfer Protocol):** This is the standard protocol for sending emails. It handles the submission of an email from a user's client (User Agent) to the outgoing mail server, as well as the transfer of emails between mail servers.
*   **C. HTTP (Hypertext Transfer Protocol):** This is the foundation of data communication for the World Wide Web. While web-based email services (like Gmail or Yahoo Mail) use HTTP/HTTPS for the user to interact with their inbox in a browser, the actual process of handing the email off to the mail server for delivery typically relies on SMTP internally. In the context of standard email architecture questions, HTTP is not the primary protocol defined for mail submission between agents and servers.
*   **D. FTP (File Transfer Protocol):** This is used for transferring files between a client and a server on a computer network. It is not used for sending email messages.

Therefore, **SMTP** is the specific protocol designed for the task described in the question.

References:

- [RFC 5321 - Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
