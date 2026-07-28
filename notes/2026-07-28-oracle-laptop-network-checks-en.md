---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oracle Laptop Network Checks
translated: false
type: note
---

Port 1521 is closed on all visible devices on your network. This means we need to check a few things on the **Oracle laptop**.

Can you please do the following checks **on the Oracle laptop** and tell me the results?

### 1️⃣ What is its IP address?

Run this in **Command Prompt** on the Oracle laptop:

```cmd
ipconfig
```

Look for the `IPv4 Address` under your active network adapter (e.g., `192.168.1.xxx`)

### 2️⃣ Is the Oracle listener running?

Run this in **Command Prompt**:

```cmd
lsnrctl status
```

### 3️⃣ Is port 1521 open in the firewall?

Run this in **Command Prompt (as Administrator)**:

```cmd
netsh advfirewall firewall show rule name=all | find "1521"
```

OR to add the firewall rule if missing:

```cmd
netsh advfirewall firewall add rule name="Oracle 1521" dir=in action=allow protocol=TCP localport=1521
```

Once you tell me the IP and the listener status, I'll guide you through the rest (creating the database user and updating `jdbc.properties` on your dev machine).
