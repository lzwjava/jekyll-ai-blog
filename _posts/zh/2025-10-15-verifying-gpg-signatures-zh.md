---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 验证GPG数字签名
translated: true
type: note
---

### 验证 GPG 签名

GnuPG（GPG）允许您验证数字签名，以确保文件或消息未被篡改且来自声称的发送者。验证需要您的密钥环中包含签名者的公钥。以下是常见场景的步骤和命令。

#### 前提条件

1. **安装 GPG**：确保系统已安装 GnuPG（例如，在基于 Debian 的系统上使用 `apt install gnupg`，在 macOS 上使用 `brew install gnupg`）。
2. **导入签名者的公钥**：您需要签名文件的人或实体的公钥。从密钥服务器或文件下载后导入：

   ```
   gpg --import public-key.asc
   ```

   （将 `public-key.asc` 替换为实际的密钥文件。如果来自密钥服务器，使用 `gpg --keyserver keyserver.ubuntu.com --recv-keys KEYID`，其中 `KEYID` 是密钥的指纹或 ID。）

#### 验证步骤

具体命令取决于签名创建的方式（例如，内联在文件中或分离式）。

1. **验证分离式签名**（常见于软件发布等文件；签名位于单独的 `.sig` 文件中）：

   ```
   gpg --verify signature.sig original-file
   ```

   - 验证成功时的示例输出：

     ```
     gpg: 签名建立于 [日期]，使用 [密钥类型] 密钥 ID [KEYID]
     gpg: 来自“[姓名] <email@example.com>”的良好签名
     ```

   - 如果密钥未被信任，可能会看到警告，如“此密钥未经过受信任签名的认证！”您可以使用 `gpg --edit-key KEYID` 然后输入 `trust` 调整信任级别。

2. **验证内联签名文件**（签名嵌入在文件中，通常为二进制格式）：
   - 仅检查签名：

     ```
     gpg --verify signed-file
     ```

   - 验证并提取原始内容：

     ```
     gpg --output original-file --decrypt signed-file
     ```

     如果文件已加密，会提示输入密码；仅验证签名时，仅进行验证。

3. **验证明文签名消息**（人类可读文本附带 ASCII 编码签名，常见于电子邮件或 README 文件）：

   ```
   gpg --verify clearsigned-file.txt
   ```

   输出将显示签名状态，且不更改文件内容。

#### 故障排除

- **“无公钥”错误**：按上述方法导入密钥。
- **不良签名**：文件可能已被篡改——请重新下载。
- **密钥有效性**：使用 `gpg --list-keys` 检查密钥详情，或验证指纹是否与官方来源匹配。
- 对于批量验证或脚本处理，添加 `--batch --exit-on-status-write-error`。

有关签名或高级选项的更多详情，请参阅官方手册。

[制作和验证签名 - GnuPG 手册](https://www.gnupg.org/gph/en/manual/x135.html)
