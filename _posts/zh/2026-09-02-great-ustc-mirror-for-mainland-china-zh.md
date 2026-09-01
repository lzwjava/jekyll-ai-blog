---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向中国大陆的中科大优秀镜像
translated: true
type: note
---

问题：**`mirrors.ustc.edu.cn` 是下载 Debian 及其他 Linux 发行版的好地方吗？**

回答：**是的——特别是当你从中国大陆下载时。** `mirrors.ustc.edu.cn` 是一个由中国科学技术大学（USTC）运营的非常优秀且信誉良好的镜像站。Debian 官方也将其列为官方镜像。（[USTC 开源软件镜像][1]）

具体到 Debian：

* **安装 ISO：** `debian-cd/`
* **APT 软件包：** `debian/`
* **安全仓库：** `debian-security/`
* 支持 **amd64、arm64、riscv64** 等架构
* 截至目前，**Debian 13 (trixie) 为稳定版**。（[USTC 开源软件镜像][2]）

例如，对于普通 64 位 PC：

```bash
https://mirrors.ustc.edu.cn/debian-cd/current/amd64/iso-cd/
```

如果安装期间机器可以联网，可以下载 `amd64-netinst.iso`；否则下载更大的 `amd64-CD-1.iso`。USTC 特别推荐这些路径。（[USTC 开源软件镜像][3]）

安装完成后，你可以使用：

```text
https://mirrors.ustc.edu.cn/debian/
```

作为 APT 镜像。USTC 提供了对应的 Debian 13 配置。（[USTC 开源软件镜像][2]）

**一点注意：** 对于安全更新，Debian 官方的 `deb.debian.org/debian-security` 仍然是个合理的选择，因为 USTC 指出其安全镜像可能存在同步延迟。（[USTC 开源软件镜像][4]）

所以，对于你在 Debian/Lubuntu 上的试验，在中国境内时我强烈建议使用 USTC。

参考资料：

* [USTC 开源软件镜像](https://mirrors.ustc.edu.cn/?utm_source=chatgpt.com)
* [Debian 镜像列表](https://www.debian.org/mirror/list?utm_source=chatgpt.com)
* [USTC Debian 镜像帮助](https://mirrors.ustc.edu.cn/help/debian.html?utm_source=chatgpt.com)

[1]: https://mirrors.ustc.edu.cn/?utm_source=chatgpt.com "USTC 开源软件镜像"
[2]: https://mirrors.ustc.edu.cn/help/debian.html?utm_source=chatgpt.com "Debian - USTC 镜像帮助"
[3]: https://mirrors.ustc.edu.cn/help/debian-cd.html?utm_source=chatgpt.com "Debian CD - USTC 镜像帮助"
[4]: https://mirrors.ustc.edu.cn/help/debian-security.html?utm_source=chatgpt.com "Debian 安全 - USTC 镜像帮助"