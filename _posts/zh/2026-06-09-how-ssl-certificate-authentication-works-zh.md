---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSL证书认证的工作原理
translated: true
type: note
---

**问题：** SSL/TLS 证书认证是如何工作的？

## 答案

SSL 证书解决了一个根本问题：客户端如何信任一个它从未通信过的服务器？解决方案链包含了非对称加密、数字签名和可信中介。

### 核心机制：数字签名

基础是 **asymmetric cryptography（非对称加密）**，它使用一对密钥：

- **Private key（私钥）**（保密，由服务器持有）：用于签名数据
- **Public key（公钥）**（自由分发）：用于验证签名

数字签名证明三件事：

1. 服务器拥有私钥（身份证明）
2. 数据未被篡改
3. 服务器在握手过程中是真实存在的（防止重放攻击）

以下是一个展示原理的最小化 Python 示例：

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# 服务器生成密钥对
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# 服务器用私钥签名数据
data = b"hello from server"
signature = private_key.sign(data, padding.PSS(...), hashes.SHA256())

# 客户端用公钥验证签名
public_key.verify(signature, data, padding.PSS(...), hashes.SHA256())
# ✓ 签名有效——服务器拥有该私钥
```

### 证书结构：身份与公钥绑定

证书是一个数字文档，它将以下内容绑定在一起：

- 服务器的 **public key（公钥）**
- 服务器的 **identity（身份）**（域名、组织）
- **元数据**（有效期、预期用途）

所有内容均由 Certificate Authority（CA）签名。

证书结构（X.509）：

```
Certificate {
  tbsCertificate {  // "to be signed"
    version: 3
    serialNumber: 01A2B3
    signature: sha256WithRSAEncryption
    issuer: CN=Let's Encrypt, O=Internet Security Research Group
    subject: CN=example.com, O=Example Inc
    validity: notBefore=2024-01-01, notAfter=2025-01-01
    subjectPublicKeyInfo: <服务器的公钥>
    extensions: {
      subjectAltName: example.com, www.example.com
      keyUsage: digitalSignature, keyEncipherment
    }
  }
  signatureAlgorithm: sha256WithRSAEncryption
  signature: <CA 对 tbsCertificate 的数字签名>
}
```

**CA 的签名** 是关键部分——它以加密方式断言：“我，一个受信任的权威机构，验证该公钥属于 example.com。”

### 信任链：PKI 模型

客户端无法直接验证每个证书。相反，证书链的信任关系会被回溯到一个受信任的根 CA。典型结构：

```
终端实体证书 (example.com)
  ↑ 由以下签发
中间 CA 证书
  ↑ 由以下签发
根 CA 证书
  ↑ 自签名（客户端默认信任此证书）
```

操作系统/浏览器预装了根 CA。验证证书时：

```python
# 客户端拥有证书和 CA 的公钥
cert = load_certificate("example.com.pem")
ca_public_key = load_public_key("letsencrypt-root.pem")

# 验证 CA 对证书的签名
ca_public_key.verify(cert.signature, cert.tbs_certificate, ...)
# ✓ 该证书由受信任的 CA 签发
```

### 验证检查清单：客户端实际检查的内容

在密钥交换之前，客户端检查：

1. 使用 CA 的公钥验证 CA 的数字签名（确保真实性）
2. 证书未过期
3. 证书未被吊销（CRL 或 OCSP）
4. 证书中的 Subject Alternative Name（SAN）或 Common Name（CN）中的域名与请求的域名匹配

以下是简化的验证逻辑：

```python
def verify_certificate(cert, trusted_ca_certs, requested_domain):
    # 1. 验证 CA 签名
    for ca_cert in trusted_ca_certs:
        try:
            ca_cert.public_key.verify(cert.signature, cert.tbs_certificate)
            issuer_found = True
            break
        except:
            pass
    assert issuer_found, "未找到受信任的签发者"

    # 2. 检查过期
    now = datetime.now()
    assert cert.notBefore < now < cert.notAfter, "证书已过期"

    # 3. 检查吊销 (CRL/OCSP)
    assert not is_revoked(cert.serialNumber, cert.issuer), "证书已被吊销"

    # 4. 检查域名匹配
    san = cert.extensions.get('subjectAltName')
    domains = san.split(',') if san else [cert.subject.commonName]
    assert requested_domain in domains, "域名不匹配"

    return True
```

### 握手流程 (TLS 1.3)

1. **Client Hello** → 发送支持的 TLS 版本、密码套件、随机随机数
2. **Server Hello** → 选择密码，发送服务器随机数，发送证书链
3. **Certificate Verification** → 客户端按上述方式验证证书
4. **Key Exchange** → 使用非对称加密（Diffie-Hellman 变体如 ECDHE），客户端和服务器安全地建立共享的对称会话密钥
5. **CertificateVerify** → 服务器用私钥对整个握手记录签名，证明它拥有私钥，证明服务器的真实存在并防止 MITM 攻击
6. **Finished** → 双方验证握手完整性，切换到对称加密

关键点：**身份认证使用非对称加密，高效通信使用对称加密**。公钥操作较慢，因此一旦信任建立，双方会派生出快速的对称密钥，并用于所有应用数据。

### 为何这能防止 MITM

攻击者无法在不被检测的情况下拦截，因为：

- 要伪造证书，他们需要 CA 的私钥（全局秘密）
- 要完成握手，他们需要服务器的私钥（服务器的秘密）
- 即使使用伪造的证书，域名验证也会失败
- 服务器通过 CertificateVerify 证明密钥所有权——没有私钥无法伪造

---

参考资料：

- Practical Foundations in Cybersecurity - The SSL/TLS Handshake
- Encryption Consulting - Practical Guide to SSL/TLS Certificates
- RFC 5280 (X.509 certificates)
- RFC 8446 (TLS 1.3)
