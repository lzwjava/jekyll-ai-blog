---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: TCP vs UDP Connection Differences
translated: false
type: note
---

You've got the right intuition! Let me clarify the key differences:

## TCP Connection

When a TCP connection is **established** (via the 3-way handshake), both sides maintain **state information** about each other:

**What each side stores:**
- **Remote IP address and port** (who am I talking to?)
- **Local IP address and port** (my endpoint)
- **Sequence numbers** (for ordering and reliability)
- **Window sizes** (for flow control)
- **Connection state** (ESTABLISHED, CLOSING, etc.)

So yes, "connected" means both client and server have allocated memory and resources to track this specific conversation. They know about each other and maintain this relationship until the connection is closed.

## UDP - No Connection

UDP is **connectionless**. There's no handshake, no stored state:

- The client just sends a packet to an IP:port
- The server receives it and processes it
- **Neither side maintains any relationship information**
- Each packet is independent
- Very lightweight - no memory overhead per "connection"

## The Key Difference

**TCP:** "Hello, I'm Client X. Let's talk. Here's my info, I have yours. We're now connected." → **Stateful**

**UDP:** "Here's a packet for address Y:port Z" → Fire and forget → **Stateless**

You're absolutely right that UDP is much more lightweight because there's no connection state to maintain, no buffers to manage, and no acknowledgments to track. The tradeoff is that TCP provides reliability, ordering, and flow control, while UDP provides speed and simplicity.
