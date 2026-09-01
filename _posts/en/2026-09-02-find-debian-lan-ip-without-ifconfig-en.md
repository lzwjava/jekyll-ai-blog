---
audio: false
generated: true
image: false
lang: en
layout: post
title: Find Debian LAN IP without ifconfig
translated: false
type: note
---

Question: How do you find the Debian machine's LAN IP when `ifconfig` isn't installed?

Answer: On modern Debian, just use the built-in `ip` command. You **don't need `ifconfig`**.

```bash
ip addr
```

Look for something like:

```text
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.1.123/24
```

Your LAN IP is:

```text
192.168.1.123
```

### Even simpler

```bash
hostname -I
```

Example:

```text
192.168.1.123
```

For your SSH setup, this is probably all you need:

```bash
hostname -I
```

Then from another computer:

```bash
ssh your_username@192.168.1.123
```

### If `hostname -I` gives nothing

Check the interfaces:

```bash
ip link
```

and routes:

```bash
ip route
```

A typical connected Debian machine will show:

```text
default via 192.168.1.1 dev enp3s0
192.168.1.0/24 dev enp3s0 src 192.168.1.123
```

The `src` address is your LAN IP.

If you specifically want `ifconfig`, install it with:

```bash
sudo apt install net-tools
```

but I'd recommend **learning/using `ip` instead**. `ifconfig` is the older interface; `ip` is the modern Linux networking tool.
