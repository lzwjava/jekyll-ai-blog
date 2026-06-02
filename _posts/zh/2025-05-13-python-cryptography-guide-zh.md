---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python密码学指南
translated: true
type: note
---

### 密码学包简介
`cryptography` 是一个流行的 Python 库，提供密码学原语和安全协议实现方案。该库注重易用性和安全性，实现了 AES、RSA 等标准。它并非用于直接实现 SSH 或 TLS 等高级协议——请将其作为基础构建模块使用。务必确保及时更新以获取安全补丁。

### 安装
通过 pip 安装：
```bash
pip install cryptography
```
如需更好性能（特别是处理大密钥或频繁操作），可安装 OpenSSL 支持：
```bash
pip install cryptography[openssl]
```
注意：在某些系统上可能需要单独安装 OpenSSL 头文件（例如 Ubuntu 系统使用 `apt install libssl-dev`）。

### 基本概念
- **原语**：加密/解密等底层操作
- **方案**：高级封装函数（如用于对称加密的 Fernet）
- **风险警告**：库会针对不安全使用发出警告——请务必关注

导入库：
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes, asyncioc as a
from cryptography.hazmat.primitives.asymmetric import rsa, padding
```

### 示例

#### 1. 使用 Fernet 进行对称加密（最适合初学者）
Fernet 采用 AES-128 CBC 模式配合 HMAC 确保完整性，非常适合加密存储数据。

```python
from cryptography.fernet import Fernet

# 生成密钥（请安全存储，如环境变量）
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
plaintext = b"这是秘密信息"
token = cipher.encrypt(plaintext)
print("加密结果:", token)

# 解密
decrypted = cipher.decrypt(token)
print("解密结果:", decrypted)
```
- **注意**：密钥为 URL 安全的 base64 格式（44 字符）。切勿硬编码密钥，需定期轮换。

#### 2. 使用 RSA 进行非对称加密
生成公私钥对，加密数据后仅私钥持有者可解密。

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# 生成私钥
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# 序列化存储
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()  # 密码保护请使用 BestAvailableEncryption()
)

# 获取并序列化公钥
public_key = private_key.public_key()
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 使用公钥加密
plaintext = b"秘密信息"
ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# 使用私钥解密
decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print("解密结果:", decrypted)
```
- **注意**：RSA 处理大数据较慢，建议用于密钥交换或小消息。OAEP 填充可防范攻击。

#### 3. 生成和使用哈希
用于完整性校验或密码哈希。

```python
from cryptography.hazmat.primitives import hashes

# 哈希计算
digest = hashes.Hash(hashes.SHA256())
digest.update(b"待处理数据")
hash_result = digest.finalize()
print("SHA256 哈希:", hash_result.hex())
```

密码处理请使用 `cryptography.hazmat.primitives.kdf.pbkdf2` 进行密钥派生（例如使用 PBKDF2 进行加盐慢哈希）。

#### 4. 使用 RSA 进行数字签名
对数据签名以验证真实性。

```python
# 使用前述 RSA 密钥
message = b"待签名数据"
signature = private_key.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# 使用公钥验证
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("签名有效")
except Exception:
    print("签名无效")
```

### 最佳实践
- **密钥管理**：安全存储密钥（如使用 AWS KMS、硬件安全模块）。切勿重复使用密钥。
- **填充和模式**：始终使用安全填充（如 RSA 用 OAEP，AES 用 GCM）。
- **随机性**：使用 `os.urandom()` 或 `secrets` 模块生成随机数，避免使用 `random`。
- **更新**：密码学技术持续演进——定期检查使用方式是否存在漏洞。
- **避免自造轮子**：复杂需求请使用现成方案或集成高级库（如 `pyjwt` 或 `boto3`）。
- **测试**：使用库提供的常量和异常进行错误处理。

### 扩展阅读
- [官方文档](https://cryptography.io/en/latest/)——详细 API 参考和教程
- [PyPI 页面](https://pypi.org/project/cryptography/)——版本历史和集成信息
- 高级主题可查阅 `cryptography` Wiki 或 RFC 文档（如 PKCS#1 的 RFC 8017）

如有具体使用场景（如文件加密或 API 安全），提供详细信息可获取针对性示例。
