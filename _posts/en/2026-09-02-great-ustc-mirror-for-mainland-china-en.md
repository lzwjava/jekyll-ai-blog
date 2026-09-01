---
audio: false
generated: true
image: false
lang: en
layout: post
title: Great USTC Mirror for Mainland China
translated: false
type: note
---

Question: **Is `mirrors.ustc.edu.cn` a good place to download Debian and other Linux distributions?**

Answer: **Yes — especially if you're downloading from mainland China.** `mirrors.ustc.edu.cn` is a very good, reputable mirror operated by the University of Science and Technology of China (USTC). Debian itself lists it as an official mirror. ([USTC Open Source Software Mirror][1])

For Debian specifically:

* **Installer ISOs:** `debian-cd/`
* **APT packages:** `debian/`
* **Security repository:** `debian-security/`
* Supports **amd64, arm64, riscv64**, etc.
* As of now, **Debian 13 (trixie) is Stable**. ([USTC Open Source Software Mirror][2])

For example, for a normal 64-bit PC:

```bash
https://mirrors.ustc.edu.cn/debian-cd/current/amd64/iso-cd/
```

You can download the `amd64-netinst.iso` if the machine has Internet access during installation, or the larger `amd64-CD-1.iso`. USTC specifically recommends these paths. ([USTC Open Source Software Mirror][3])

And after installation, you can use:

```text
https://mirrors.ustc.edu.cn/debian/
```

as your APT mirror. USTC provides the corresponding Debian 13 configuration. ([USTC Open Source Software Mirror][2])

**One nuance:** for security updates, Debian's official `deb.debian.org/debian-security` is still a reasonable choice because USTC notes that its security mirror can have synchronization delay. ([USTC Open Source Software Mirror][4])

So for your Debian/Lubuntu experiments, I'd absolutely use USTC when you're in China.

References:

* [USTC Open Source Software Mirror](https://mirrors.ustc.edu.cn/?utm_source=chatgpt.com)
* [Debian Mirror List](https://www.debian.org/mirror/list?utm_source=chatgpt.com)
* [USTC Debian Mirror Help](https://mirrors.ustc.edu.cn/help/debian.html?utm_source=chatgpt.com)

[1]: https://mirrors.ustc.edu.cn/?utm_source=chatgpt.com "USTC Open Source Software Mirror"
[2]: https://mirrors.ustc.edu.cn/help/debian.html?utm_source=chatgpt.com "Debian - USTC Mirror Help"
[3]: https://mirrors.ustc.edu.cn/help/debian-cd.html?utm_source=chatgpt.com "Debian CD - USTC Mirror Help"
[4]: https://mirrors.ustc.edu.cn/help/debian-security.html?utm_source=chatgpt.com "Debian Security - USTC Mirror Help"
