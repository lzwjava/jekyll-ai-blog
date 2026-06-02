---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 安全导出 GPG 私钥
translated: true
type: note
---

### 以 ASCII 装甲格式导出 GPG 私钥

GPG（GNU Privacy Guard）支持以 ASCII 装甲格式导出私钥，将其保存为人类可读的 `.asc` 文件（非二进制格式）。这种格式便于备份、传输或在其他设备上导入。

**重要警告：** 私钥包含敏感信息。仅在必要时导出，存储或传输时请加密输出文件，使用后立即删除导出文件以避免意外泄露。切勿公开分享私钥。

#### 基本命令结构
要导出特定用户 ID（与密钥关联的邮箱或名称）的私钥，请使用：

```
gpg --export-secret-keys --armor [密钥标识] > 文件名.asc
```

- `密钥标识`：密钥指纹、短标识、邮箱或名称。可通过 `gpg --list-secret-keys` 查看密钥列表。
- `--armor`：以装甲（ASCII）格式输出，替代二进制格式。
- `> 文件名.asc`：将输出重定向至文件（如 `我的私钥.asc`）。省略此参数将直接输出至终端。

#### 分步使用示例
1. **列出您的私钥**以确定密钥标识：
   ```
   gpg --list-secret-keys
   ```
   示例输出：
   ```
   sec   rsa3072/ABC12345 2023-01-01 [SC] [expires: 2025-01-01]
         密钥指纹 = 1234 5678 ABCD EF01 2345 6789 ABCD EF01 2345 6789
   uid                 [ultimate] 您的姓名 <your@email.com>
   ```

   此处 `ABC12345` 为短密钥标识，也可使用完整指纹 `ABCDEF0123456789ABCDEF0123456789` 确保精确匹配。

2. **导出私钥**：
   ```
   gpg --export-secret-keys --armor ABC12345 > 我的私钥.asc
   ```

3. **验证导出文件**（可选）：
   ```
   cat 我的私钥.asc
   ```
   文件应以 `-----BEGIN PGP PRIVATE KEY BLOCK-----` 开头，以 `-----END PGP PRIVATE KEY BLOCK-----` 结尾。

#### 附加选项
- **导出所有私钥**：省略密钥标识即可导出全部：
  ```
  gpg --export-secret-keys --armor > 所有私钥.asc
  ```
- **设置密码保护**：若密钥已加密（默认配置），GPG 将提示输入密码。
- **如需导出公钥**：请使用 `--export` 命令（仅导出公钥）。

完整文档请参阅 GPG 手册页：`man gpg`。若您是 GPG 新手，请先使用 `gpg --gen-key` 生成密钥。
