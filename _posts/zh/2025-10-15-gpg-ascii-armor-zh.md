---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPG ASCII封装格式详解
translated: true
type: note
---

在GPG（GNU Privacy Guard）中，“armor”指的是ASCII封装格式，这种格式将二进制的OpenPGP数据（如加密文件、签名或密钥）编码为人类可读的文本形式。这种编码方式适用于通过纯文本渠道（如电子邮件）传输数据而不会损坏内容——其原理类似于uuencode或base64编码，但额外增加了头部标识（例如“-----BEGIN PGP MESSAGE-----”）和完整性校验码。

您可以在执行加密（`gpg -a -e file.txt`）或密钥导出（`gpg --armor --export keyid`）等命令时，通过`--armor`（或`-a`）选项启用此功能。启用后，命令输出将采用这种封装文本格式而非原始二进制数据。

## 参考文档

- [GnuPG中armor选项的作用是什么？](https://unix.stackexchange.com/questions/623375/what-is-the-armored-option-for-in-gnupg)
- [密钥交换 - GnuPG](https://www.gnupg.org/gph/en/manual/x56.html)
- [第13章 ASCII封装 - OpenPGP技术笔记](https://openpgp.dev/book/armor.html)
- [GPG输入与输出（GNU Privacy Guard使用指南）](https://www.gnupg.org/documentation/manuals/gnupg/GPG-Input-and-Output.html)
