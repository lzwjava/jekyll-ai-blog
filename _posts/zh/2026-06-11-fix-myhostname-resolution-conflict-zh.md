---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复myhostname解析冲突
translated: true
type: note
---

代码已回退至简单版本。请在1.47上执行以下命令：

```
sudo sed -i 's/ hosts myhostname//' /etc/nsswitch.conf
```

此操作将从主机名解析链中移除 `myhostname`。当前 `/etc/nsswitch.conf` 文件内容为：
```
hosts: files mdns4_minimal [NOTFOUND=return] dns myhostname
```

`myhostname` 模块会为主机名 `xx` 返回Tailscale的IPv6地址，这会导致Gloo的对等套接字绑定出现混乱。移除该模块后，`getent hosts xx` 将仅使用 `/etc/hosts` 文件（其中包含 `192.168.1.28 xx`）。

随后请通过以下命令验证：
```
getent hosts xx
```

应返回 `192.168.1.28 xx`，而非Tailscale的IPv6地址。之后我将重新启动训练。