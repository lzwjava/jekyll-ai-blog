---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Hubs Simple Repeaters in Networks
translated: false
type: note
---

A hub is a simple network device that operates at the **Physical Layer (Layer 1)** of the OSI model. Here's how it functions:

## Basic Operation

A hub is essentially a **multi-port repeater**. When a device connected to one port sends data (electrical signals), the hub receives those signals and repeats them out to all other ports simultaneously. It's completely dumb in that sense—it doesn't understand IP addresses, MAC addresses, or any higher-layer information. It just amplifies and forwards the electrical signals.

## Key Characteristics

**No intelligence**: A hub doesn't make any decisions about where data should go. If one computer sends data, it goes to every other port on the hub.

**Shared bandwidth**: All devices connected to a hub share the same bandwidth. If a hub has 4 ports with 100 Mbps capacity, each device doesn't get 100 Mbps—they all share that bandwidth, which decreases as more devices communicate.

**Collision domain**: All ports on a hub are in the same collision domain. If two devices transmit simultaneously, their signals collide. The hub can't prevent this because it has no intelligence to manage traffic.

## Why Switches are Better

This is why **switches** (which operate at Layer 2, the Data Link Layer) replaced hubs. Switches understand MAC addresses and can forward frames to specific ports rather than flooding all ports. This eliminates collisions, provides full bandwidth to each port, and creates separate collision domains.

In modern networks, hubs are essentially obsolete—you won't find them in use anymore. They've been replaced by switches in virtually all practical applications.