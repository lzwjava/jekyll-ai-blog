---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPG加密收件人详解
translated: true
type: note
---

### 理解 GPG 命令与"收件人"提示

您正在运行的命令是使用 GnuPG (GPG) 加密文件 (`inputfile.txt`)：

```
gpg --homedir /path/to/custom/dir -e -r recipient@example.com --encrypt inputfile.txt
```

- `--homedir /path/to/custom/dir`：使用自定义目录作为 GPG 的密钥环和配置目录（替代默认的 `~/.gnupg`）。
- `-e`（或 `--encrypt`）：指示 GPG 加密文件。
- `-r recipient@example.com`：指定**收件人**（您为其加密的个人或实体）。这应该是他们的电子邮件、姓名或来自其公钥的密钥 ID。
- `--encrypt inputfile.txt`：要加密的文件（输出将为 `inputfile.txt.gpg`）。

#### 这里的"收件人"是什么意思？

在 GPG 加密中：

- **收件人**是*将接收并解密*文件的人。您使用*他们的公钥*加密文件，因此只有他们（使用其私钥）才能解密它。
- 它不是"发件人"（您），因为加密是为了保护*收件人*的数据。您作为发件人的角色更多是关于签名（如果您添加 `-s` 进行签名），但这里只是纯加密。

您说得对，这是为了"发送"安全数据，但术语侧重于收件人，因为这是其密钥保护的对象。可以将其想象成用别人的挂锁锁住一个盒子——只有他们才能打开它。

#### 为什么会出现错误："您没有指定用户 ID。（您可以使用 '-r'）"以及提示？

出现此交互式提示的原因是：

1. GPG 在您的密钥环（在自定义 homedir 中）中找不到与 `recipient@example.com` 匹配的公钥。
2. 虽然提供了 `-r` 标志，但它无法解析为有效的密钥，因此 GPG 回退到要求您手动输入用户 ID。

提示是：

```
当前收件人：
输入用户 ID。以空行结束：
```

- **用户 ID** 是指收件人的完整标识符，例如 `John Doe <recipient@example.com>` 或其密钥指纹/ID（例如 `ABCDEF123456`）。
- 如果需要，逐行输入（例如，姓名、电子邮件、注释），然后按两次 Enter（空行）完成。

#### 如何解决此问题

1. **首先导入收件人的公钥**（最常见的问题）：
   - 请收件人将其公钥发送给您（通过 `gpg --export -a their@email.com` 导出）。
   - 导入它：`gpg --homedir /path/to/custom/dir --import their-public-key.asc`。
   - 然后重新运行您的命令。

2. **如果密钥已导入但不匹配**：
   - 列出密钥：`gpg --homedir /path/to/custom/dir --list-keys`。
   - 在 `-r` 中使用其中确切的用户 ID（例如 `-r "John Doe <recipient@example.com>"`）。

3. **在提示符处**（作为快速解决方法）：
   - 输入完整的用户 ID，例如：

     ```
     John Doe
     recipient@example.com

     ```

     （空行结束输入。）

#### 为什么是"收件人"而不是"发件人"？

- 加密是*非对称的*：公钥（任何人都可以加密）→ 私钥（只有所有者可以解密）。
- 发件人（您）使用收件人的**公钥**加密。
- 如果您想证明您是发件人，请添加签名：`gpg ... -e -r recipient@example.com -s --encrypt inputfile.txt`（使用*您的*私钥进行签名）。
- "收件人"是标准的 GPG 术语——它与谁发送无关，而是与谁接收/解密有关。将其称为"发件人"会引起混淆，因为发件人不需要密钥进行加密（仅用于签名）。

如果这不能解决问题，请分享 `--list-keys` 的输出（隐去敏感信息），我可以帮助调试！

#### 参考资料

- [GPG 加密基础](https://www.gnupg.org/documentation/manuals/gnupg/Encrypting-and-Decrypting.html)
- [GPG 手册页](https://www.gnupg.org/documentation/manuals/gnupg/gpg.html)
