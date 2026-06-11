---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix myhostname resolution conflict
translated: false
type: note
---

Code reverted to simple version. Now please run this on 1.47:

```
sudo sed -i 's/ hosts myhostname//' /etc/nsswitch.conf
```

This removes `myhostname` from the hosts resolution chain. Currently `/etc/nsswitch.conf` has:

```
hosts: files mdns4_minimal [NOTFOUND=return] dns myhostname
```

The `myhostname` module returns IPv6 Tailscale addresses for hostname `xx`, which confuses Gloo's pair socket binding. Removing it makes `getent hosts xx` use only `/etc/hosts` (which has `192.168.1.28 xx`).

After that, verify with:

```
getent hosts xx
```

It should return `192.168.1.28 xx` instead of the Tailscale IPv6 addresses. Then I'll restart training.
