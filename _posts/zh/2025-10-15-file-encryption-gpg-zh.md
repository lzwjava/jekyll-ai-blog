---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用GPG加密文件
translated: true
type: note
---

### 使用 GPG 密钥加密文件

您的 GPG 密钥列表显示与邮箱 `lzwjava@gmail.com` 关联的公钥（pub）指纹为 `982740390B5D33E90B6B6133892BC5A4789B71CD`。要使用此密钥加密文件（确保只有您能用私钥解密），请在终端中按以下步骤操作：

1. **进入目标文件所在目录**（例如文件为 `secret.txt`）：

   ```
   cd ~/path/to/your/file
   ```

2. **使用 `--encrypt` 选项加密文件**并指定接收者（您的邮箱或密钥ID）。这将生成加密的 `.gpg` 文件：

   - 使用邮箱地址（更简便）：

     ```
     gpg --encrypt --recipient lzwjava@gmail.com secret.txt
     ```

   - 使用完整密钥指纹：

     ```
     gpg --encrypt --recipient 982740390B5D33E90B6B6133892BC5A4789B71CD secret.txt
     ```

   操作将生成 `secret.txt.gpg` 加密文件，原始 `secret.txt` 文件保持不变。

3. **验证加密结果**（可选）：

   ```
   gpg --list-packets secret.txt.gpg
   ```

   此命令将显示加密数据包的详细信息。

### 文件解密操作（供后续参考）

如需解密（必须使用您的私钥和密码短语）：

```
gpg --decrypt secret.txt.gpg > secret.txt.decrypted
```

根据提示输入密码短语。

### 实用技巧

- **对称加密**（若无需接收者密钥，仅使用密码短语）：可使用 `gpg -c secret.txt`
- **加密并签名**（用于验证文件来源）：在加密命令中添加 `--sign` 参数，例如 `gpg --encrypt --sign --recipient lzwjava@gmail.com secret.txt`
- 若遇到错误（如密钥未受信任），可运行 `gpg --edit-key lzwjava@gmail.com` 后使用 `trust` 命令设置为终极信任
- 请定期备份 `~/.gnupg` 目录以确保密钥安全

更多详细信息请参阅 GPG 手册：[GPG 文档](https://www.gnupg.org/documentation/manpage.html)
