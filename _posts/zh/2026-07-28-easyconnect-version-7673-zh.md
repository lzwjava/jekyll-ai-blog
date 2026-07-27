---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EasyConnect 版本 7.6.7.3
translated: true
type: note
---

问题：**`EasyConnect_x64_7_6_7_3.deb` — 这个 Ubuntu 客户端是什么版本？**

答案：

这个文件名已经说明了版本：

```text
EasyConnect_x64_7_6_7_3.deb
              | | | |
              | | | └── 补丁/构建号：3
              | | └──── 次版本号：7
              | └────── 主版本号：6
              └──────── 产品分支：7
```

因此它是：

```text
EasyConnect 7.6.7.3
```

或者深信服命名方式：

```text
M7.6.7.3
```

这是 **Linux x86_64 (amd64) 客户端**。包名中的 `x64` 表示：

```
CPU 架构：x86_64 / amd64
包格式：   Debian (.deb)
操作系统： 基于 Ubuntu/Debian 的 Linux
版本：     7.6.7.3
```

同一个客户端通常可以从深信服 Linux 7.6.7 包路径下载。([深信服社区][1])

---

针对你的情况：

* 联想小新 14 + Windows 11：

```text
CPU: Intel/AMD x86_64
操作系统：Windows 11 x64
```

你**不应该安装这个 `.deb`**。

请使用：

```text
EasyConnect_x64_7_6_7_xxx.exe
```

用于 Windows。

Ubuntu 的 `.deb` 仅适用于：

```text
Ubuntu Desktop x86_64
```

例如：

```bash
sudo dpkg -i EasyConnect_x64_7_6_7_3.deb
```

将其安装在 Ubuntu 上。([2048 AI][2])

---

实际上，这还给了我们关于你网关的另一个线索：

如果你的 VPN 门户提供：

```text
EasyConnect_x64_7_6_7_3.deb
```

这强烈表明你的深信服 SSL VPN 网关很可能属于 **M7.6.7 系列**，因为这是所提供的 Linux 客户端分支。([深信服社区][3])

因此，对于 Windows 11，匹配的客户端很可能是：

```text
EasyConnect M7.6.7+
Windows x64
```

而不是较旧的 M6.9–M7.6.6R1 包。

[1]: https://bbs.sangfor.com.cn/forum.php?mod=viewthread&tid=293841&utm_source=chatgpt.com "深信服社区-专业、开放、共享"
[2]: https://2048ai.net/681da2bea5baf817cf49e4a8.html?utm_source=chatgpt.com "Ubuntu20.04版本安装easyconnect及兼容性问题解决_linux_天寒心亦热-2048 AI社区"
[3]: https://bbs.sangfor.com.cn/forum.php?mod=viewthread&page=1&tid=214299&utm_source=chatgpt.com "深信服社区-专业、开放、共享"