---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Huawei VRP Basic Configuration View Identification
translated: false
type: note
---

Question: Which command view in Huawei VRP is used for basic configuration tasks?

Answer:

The correct answer is **B) System view**.

In Huawei's Versatile Routing Platform (VRP):

- **User view** (< >): This is the initial login view, primarily used for monitoring, basic display commands (e.g., `display version`, `ping`), and simple operational tasks. Configuration changes are not allowed here.
- **System view** ([ ]): This is the primary view for basic and global configuration tasks, such as creating VLANs, setting system parameters, configuring AAA, managing users, and entering other specific views (e.g., interface or protocol views).
- **Interface view**: Used for configuring parameters specific to individual interfaces (e.g., IP address on Ethernet ports).
- **Protocol view**: Used for configuring routing protocols (e.g., OSPF or BGP areas).

Basic configuration tasks (like hostname changes, VLAN creation, or management IP setup) are performed in the system view after entering it with the command `system-view`.

Option D is incorrect.
