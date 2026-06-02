---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GnuPG主目录文件详解
translated: true
type: note
---

这些文件和目录是 GnuPG（GPG）主目录（`~/.gnupg/`）的组成部分，用于存储加密、签名和身份验证相关的密钥及数据。GPG 是实现安全通信和数据保护的工具。以下是基于 GnuPG 2.1+ 标准行为的详细说明：

- **openpgp-revocs.d**：存放创建密钥对时生成的撤销证书（`.rev` 文件）的目录。当密钥泄露或不再需要时，可用这些证书撤销（作废）密钥以阻止后续使用。

- **private-keys-v1.d**：采用 GnuPG 2.1 引入的新密钥格式存储私钥的目录。每个密钥独立存为单独文件，以提升安全性和管理效率。请严格保护此目录——它如同您的数字保险库。

- **pubring.kbx**：新版 "keybox" 格式（`.kbx`）的公钥环文件。存储您导入的他人公钥，用于向对方加密消息或验证其签名。

- **pubring.kbx~**：`pubring.kbx` 的备份文件，由 GPG 在编辑或更新时自动创建。波浪符（`~`）后缀是 Linux 系统中常见的备份文件命名惯例。

- **trustdb.gpg**：信任数据库文件，记录您为公钥设置的信任等级（例如对自己的密钥标记为“绝对信任”，或根据签名为他人的密钥设置等级）。它帮助 GPG 判断密钥是否可信。

若您近期生成或导入了密钥，此目录结构属正常状态。请务必将整个 `~/.gnupg/` 目录安全备份，且切勿共享私钥。更多细节请参阅官方 GnuPG 文档。

[使用 GNU Privacy Guard](https://www.gnupg.org/documentation/manuals/gnupg.pdf)
[GnuPG 第二篇 - 创建与管理密钥](https://www.hacksanity.com/kb/gnupg-create-manage-keys/)
[Linux 系统备份与恢复 GPG 密钥指南](https://www.howtogeek.com/816878/how-to-back-up-and-restore-gpg-keys-on-linux/)
[GPG(1) 手册](https://www.gnupg.org/(en)/documentation/manuals/gnupg24/gpg.1.html)
