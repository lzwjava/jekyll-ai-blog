---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Arch Linux ISO 验证 GPG 密钥
translated: true
type: note
---

你的密钥环中存有这枚 GPG 密钥（属于 Pierre Schmitz，指纹为 `3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C`），因为这是 Arch Linux 开发者用于对 ISO 镜像进行密码学签名的官方密钥，可确保下载内容真实未经篡改。

当你在 macOS 上准备 Arch Linux 安装启动盘时（很可能遵循了 Arch 官方维基指南），标准验证流程包含两个步骤：

1. 下载 ISO 文件及其对应的 `.sig` 签名文件
2. 导入相关开发者的 GPG 密钥（本例中为 Pierre Schmitz 的密钥，他是近期 ISO 的主要签署者之一），并通过 `gpg --verify archlinux-YYYY.MM.DD-x86_64.iso.sig` 此类命令验证签名

你很可能执行过 `gpg --keyserver hkps://keys.openpgp.org --recv-keys 3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C` 这样的命令来获取并导入密钥，这使其永久保存在本地 GPG 密钥环中，因此会出现在 `gpg --list-keys` 的列表里。

该密钥完全无害——GPG 密钥仅是用于验证的公开数据——许多 Arch 用户在验证 ISO 后都会保留若干此类密钥。若需删除可运行：

```
gpg --delete-key 3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C
```

（系统将提示确认；此操作仅删除公钥，不影响已完成的验证签名）

[Arch Linux ISO 下载页面](https://archlinux.org/download/)
[Arch 维基：在 Mac 上安装 Arch Linux](https://wiki.archlinux.org/title/Install_Arch_Linux_on_Mac)
[Pierre Schmitz 的 GPG 密钥](https://pierre-schmitz.com/gpg-keys/)
