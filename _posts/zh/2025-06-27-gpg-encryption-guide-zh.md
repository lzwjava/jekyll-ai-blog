---
audio: false
generated: true
lang: zh
layout: post
title: 理解GPG：安全通信工具详解
translated: true
type: note
---

## 什么是 GPG？

GPG（GNU Privacy Guard）是 OpenPGP 标准（Pretty Good Privacy）的开源实现。作为安全通信工具，它提供加密、解密、数字签名和密钥管理功能。GPG 被广泛用于保护电子邮件、文件及其他数据的安全，确保机密性、完整性和真实性。

GPG 支持大多数操作系统，包括 Linux、macOS 和 Windows。它基于命令行操作，但可通过图形界面工具或 Thunderbird 等邮件客户端集成使用。

---

## GPG 工作原理

GPG 采用**对称密钥加密**与**非对称密钥加密**相结合的方式来保护数据安全：

1. **对称密钥加密**：
   - 使用单一密钥进行加密和解密
   - GPG 采用对称加密算法（如 AES）处理实际数据，因其对大容量数据集处理速度更快
   - 每次加密操作都会生成随机会话密钥

2. **非对称密钥加密**：
   - 使用密钥对：**公钥**用于加密，**私钥**用于解密
   - GPG 支持 RSA 或 ECDSA 等算法生成密钥对
   - 公钥加密会话密钥，再用会话密钥加密数据。接收方使用私钥解密会话密钥后，即可解密数据

3. **数字签名**：
   - 用户可使用私钥对数据签名，以证明真实性和完整性
   - 接收方通过发送方公钥验证签名

4. **密钥管理**：
   - GPG 在密钥环中管理公钥和私钥
   - 支持密钥的生成、导入、导出及发布至密钥服务器

### GPG 加密流程

加密文件或消息时：

1. GPG 生成随机会话密钥用于对称加密
2. 使用对称算法（如 AES-256）通过会话密钥加密数据
3. 使用接收方公钥通过非对称算法（如 RSA）加密会话密钥
4. 将加密后的会话密钥与数据合并为单个输出文件或消息

解密时：

1. 接收方使用私钥解密会话密钥
2. 通过会话密钥使用对称算法解密数据

这种混合方案兼具对称加密的速度优势与非对称加密的安全特性。

---

## 安装 GPG

GPG 已预装在多数 Linux 发行版中。其他系统安装方式：

- **Linux**：通过包管理器安装

  ```bash
  sudo apt install gnupg  # Debian/Ubuntu
  sudo yum install gnupg  # CentOS/RHEL
  ```

- **macOS**：通过 Homebrew 安装

  ```bash
  brew install gnupg
  ```

- **Windows**：从 [gpg4win.org](https://gpg4win.org/) 下载 Gpg4win

验证安装：

```bash
gpg --version
```

---

## 生成 GPG 密钥

使用 GPG 需要生成密钥对（公钥和私钥）。

### 密钥生成步骤

执行以下命令生成密钥对：

```bash
gpg --full-generate-key
```

1. **选择密钥类型**：
   - 默认选项为 RSA and RSA（选项1）
   - RSA 算法通用性强，能满足多数安全需求

2. **密钥长度**：
   - 推荐 2048 或 4096 位（4096 位更安全但速度稍慢）
   - 示例：选择 4096

3. **密钥有效期**：
   - 设置到期时间（如 1 年）或选择 0（永不过期）
   - 设置有效期可通过限制密钥生命周期提升安全性

4. **用户标识**：
   - 输入姓名、邮箱及可选注释
   - 示例：`John Doe <john.doe@example.com>`

5. **密码短语**：
   - 设置高强度密码短语保护私钥
   - 执行解密和签名操作时需要输入此密码短语

命令执行示例输出：

```
gpg: key 0x1234567890ABCDEF marked as ultimately trusted
gpg: generated key pair
```

### 导出密钥

- **导出公钥**：

  ```bash
  gpg --armor --output public-key.asc --export john.doe@example.com
  ```

  生成包含公钥的 ASCII 格式文件 `public-key.asc`

- **导出私钥**（注意：需严格保管）：

  ```bash
  gpg --armor --output private-key.asc --export-secret-keys john.doe@example.com
  ```

---

## 文件加密与解密

### 加密文件

为接收方加密文件：

1. 确保密钥环中已导入接收方公钥：

   ```bash
   gpg --import recipient-public-key.asc
   ```

2. 执行加密：

   ```bash
   gpg --encrypt --recipient john.doe@example.com --output encrypted-file.gpg input-file.txt
   ```

   - `--recipient`：指定接收方邮箱或密钥 ID
   - `--output`：指定输出文件
   - 生成仅接收方可解密的 `encrypted-file.gpg`

### 解密文件

解密发送给您的加密文件：

```bash
gpg --decrypt --output decrypted-file.txt encrypted-file.gpg
```

- 根据提示输入密码短语
- 解密内容将保存至 `decrypted-file.txt`

---

## 数据签名与验证

### 文件签名

签名可验证数据真实性与完整性：

- **明文签名**（包含可读签名）：

  ```bash
  gpg --clearsign input-file.txt
  ```

  输出：包含文件内容与签名的 `input-file.txt.asc`

- **分离签名**（独立签名文件）：

  ```bash
  gpg --detach-sign input-file.txt
  ```

  输出：`input-file.txt.sig`

### 验证签名

验证已签名文件：

```bash
gpg --verify input-file.txt.asc
```

验证分离签名：

```bash
gpg --verify input-file.txt.sig input-file.txt
```

需在密钥环中存有签名者的公钥

---

## 使用 GPG 生成密码

GPG 可生成随机数据用于创建安全密码。虽然 GPG 并非专业密码生成器，但其随机数生成器符合密码学安全标准。

### 生成密码命令

```bash
gpg --gen-random --armor 1 32
```

- `--gen-random`：生成随机字节
- `--armor`：输出 ASCII 格式
- `1`：质量等级（1 适用于密码学用途）
- `32`：字节数（根据所需密码长度调整）

示例输出：

```
4eX9j2kPqW8mZ3rT5vY7nL9xF2bC6dA8
```

可通过 base64 或十六进制转换，或截取指定长度来优化密码格式

### 示例：生成 20 位密码

```bash
gpg --gen-random --armor 1 15 | head -c 20
```

此命令将生成 20 位随机字符串

---

## 密钥管理

### 查看密钥

- 列出公钥：

  ```bash
  gpg --list-keys
  ```

- 列出私钥：

  ```bash
  gpg --list-secret-keys
  ```

### 发布公钥

通过密钥服务器共享公钥：

```bash
gpg --keyserver hkps://keys.openpgp.org --send-keys 0x1234567890ABCDEF
```

将 `0x1234567890ABCDEF` 替换为您的密钥 ID

### 导入密钥

从文件导入公钥：

```bash
gpg --import public-key.asc
```

从密钥服务器导入：

```bash
gpg --keyserver hkps://keys.openpgp.org --recv-keys 0x1234567890ABCDEF
```

### 撤销密钥

当密钥泄露或到期时：

1. 生成撤销证书（建议创建密钥时立即生成）：

   ```bash
   gpg --output revoke.asc --gen-revoke john.doe@example.com
   ```

2. 导入并发布撤销声明：

   ```bash
   gpg --import revoke.asc
   gpg --keyserver hkps://keys.openpgp.org --send-keys john.doe@example.com
   ```

---

## 最佳实践

1. **密钥备份**：
   - 将私钥和撤销证书存储在加密 USB 驱动器等安全位置
   - 严禁共享私钥

2. **使用强密码短语**：
   - 为私钥设置长且唯一的密码短语

3. **定期更新密钥**：
   - 设置有效期并定期轮换密钥

4. **验证密钥指纹**：
   - 信任公钥前需与持有者核实指纹：

     ```bash
     gpg --fingerprint john.doe@example.com
     ```

5. **安全使用密钥服务器**：
   - 选用可信密钥服务器如 `hkps://keys.openpgp.org`

6. **仅签名可信密钥**：
   - 为他人密钥签名前，需通过线下或可信渠道验证其身份

---

## 常用 GPG 命令速查

常用 GPG 命令快速参考：

- 生成密钥对：`gpg --full-generate-key`
- 加密文件：`gpg --encrypt --recipient <邮箱> --output <输出.gpg> <输入.txt>`
- 解密文件：`gpg --decrypt --output <输出.txt> <输入.gpg>`
- 文件签名：`gpg --clearsign <输入.txt>` 或 `gpg --detach-sign <输入.txt>`
- 验证签名：`gpg --verify <文件.asc>` 或 `gpg --verify <文件.sig> <文件>`
- 导出公钥：`gpg --armor --output public-key.asc --export <邮箱>`
- 导入密钥：`gpg --import <密钥.asc>`
- 生成随机密码：`gpg --gen-random --armor 1 <字节数>`

---

## 故障排除

- **“No secret key”错误**：确认私钥已存在于密钥环（`gpg --list-secret-keys`）且与接收方公钥匹配
- **忘记密码短语**：需撤销原密钥并生成新密钥对
- **密钥未找到**：导入接收方公钥或检查密钥服务器
- **GPG 版本问题**：确保所有参与方使用兼容版本（通过 `gpg --version` 检查）

---

## 高级功能

1. **邮件集成**：
   - 通过 Enigmail 等插件或内置 OpenPGP 功能与 Thunderbird 等邮件客户端配合使用
