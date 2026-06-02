---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPG加密选项详解
translated: true
type: note
---

### GPG 选项解析

`gpg` 命令（GNU Privacy Guard）是一款用于加密、解密和密钥管理的工具。以下将详细说明您提到的几个常用于向特定接收者加密文件的组合选项：

- **`--homedir <目录>`**：指定 GnuPG 主目录（默认为 `~/.gnupg`）。该目录用于存储密钥环、配置文件及其他数据。此选项会覆盖 `GNUPGHOME` 环境变量，适用于将 GPG 操作隔离至自定义路径的场景（例如多配置管理或安全隔离）。该参数必须通过命令行提供。

- **`-e`（或 `--encrypt`）**：使用非对称加密技术对输入数据进行加密。这是非对称加密的主要模式，数据会通过接收者的公钥进行加密。该选项可与其他功能（如签名）组合使用。

- **`-r <用户标识>`（或 `--recipient <用户标识>`）**：指定加密操作的接收者。`<用户标识>` 可以是密钥ID、邮箱或与公钥关联的名称。GPG 将使用对应的公钥加密数据。支持指定多个接收者以实现群组加密。

#### 使用示例

典型组合命令示例如下：

```
gpg --homedir /自定义目录路径 -e -r recipient@example.com 输入文件.txt
```

此命令将使用 `/自定义目录路径` 中的密钥为 `recipient@example.com` 加密 `输入文件.txt`，并生成 `输入文件.txt.gpg` 加密文件。

如需完整说明，请运行 `gpg --help` 或查阅手册页面。

[ArchWiki: GnuPG](https://wiki.archlinux.org/title/GnuPG)
[GPG 速查手册](https://irtfweb.ifa.hawaii.edu/~lockhart/gpg/)
[Linux 中的 GPG 命令](https://www.tutorialspoint.com/unix_commands/gpg.htm)
